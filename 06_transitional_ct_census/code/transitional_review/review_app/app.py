# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/review_app/app.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""review_app/app.py -- FastAPI layer: identity, the HTML pages, the JSON API, audit.csv. All state changes go
through one process-wide lock (single-worker deployment, as the CTSpinoPelvic1K review_service does).

Endpoints
    GET  /                 dashboard (counts; user names only with --public-names)
    GET  /login  POST /login  POST /logout        cookie session
    GET  /work             claim (or re-serve) the caller's next case for their role and show it
    GET  /case/{id}        the case page (claim holder only)
    GET  /case/{id}/preview/{name}   PNG preview (claim holder only)
    POST /submit           form: claim_token, verdict, reason  -> redirect to /work
    POST /release          form: claim_token                   -> redirect to /work
    GET  /audit  GET /audit.csv      admin only
    JSON: POST /api/claim, POST /api/submit, POST /api/release, GET /api/case/{id}, GET /api/status,
          GET /api/me, GET /api/audit (admin)   -- `Authorization: Bearer <token>`
    GET  /health

Run: built by __main__.py via create_app(cfg); not a script.
"""
from __future__ import annotations

import csv
import hashlib
import io
import secrets
import sys
import threading
import time
from typing import Optional

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, Response

from . import manifest as mf
from . import render
from .config import Config, build_meta
from .ledger import HFMirror, Ledger, LocalBackend
from .service import ReviewError, Service

COOKIE = "rv_session"


def _resolve_hf(token: str) -> Optional[str]:
    try:
        from huggingface_hub import whoami
        return whoami(token=token).get("name")
    except Exception:                                           # noqa: BLE001
        return None


class Identity:
    """token/cookie -> (user, role). Static tokens from REVIEW_USERS, dev tokens (token == name) when none are
    configured, and `hf_` tokens through whoami (cached by sha256 of the token, never the token itself)."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.sessions: dict = {}                                 # session id -> (user, role)
        self._hf_cache: dict = {}                                # sha256(token) -> (name, ts)

    def by_token(self, token: str, user_hint: str = "") -> Optional[tuple]:
        token = (token or "").strip()
        if not token:
            return None
        for name, rec in self.cfg.users.items():
            if secrets.compare_digest(rec["token"], token):
                if user_hint and user_hint.strip().lower() != name.lower():
                    return None
                return name, rec["role"]
        if self.cfg.dev_tokens:
            role = self.cfg.role_of(token)
            if role and (not user_hint or user_hint.strip().lower() == token.lower()):
                return token, role
        if token.startswith("hf_"):
            h = hashlib.sha256(token.encode()).hexdigest()
            hit = self._hf_cache.get(h)
            name = hit[0] if hit and time.time() - hit[1] < 600 else _resolve_hf(token)
            if name:
                self._hf_cache[h] = (name, time.time())
                role = self.cfg.role_of(name)
                if role and (not user_hint or user_hint.strip().lower() == name.lower()):
                    return name, role
        return None

    def new_session(self, user: str, role: str) -> str:
        sid = secrets.token_urlsafe(24)
        self.sessions[sid] = (user, role)
        return sid


def create_app(cfg: Config) -> FastAPI:
    meta = build_meta(cfg.prereg_path)
    man = mf.load_manifest(cfg.root, cfg.hidden_prefixes)
    backend = LocalBackend(cfg.ledger_dir)
    mirror = None
    if cfg.ledger_repo:
        if not cfg.hf_token:
            raise SystemExit("REVIEW_LEDGER_REPO set but no HF_TOKEN: refusing to run with a mirror that cannot write")
        mirror = HFMirror(cfg.ledger_repo, cfg.hf_token, backend)
        n = mirror.pull()
        print(f"[ledger] pulled {n} record(s) from {cfg.ledger_repo}")
    svc = Service(cfg, meta, man, Ledger(backend, mirror))
    rep = svc.sync()
    print(f"[startup] tree {cfg.root}: {rep}", file=sys.stderr)
    for line in mf.check_tree(man):
        print(f"[tree] {line}", file=sys.stderr)
    if meta.git_sha is None:
        print(f"[startup] WARNING git sha unknown: {meta.git_sha_error}", file=sys.stderr)
    if cfg.dev_tokens:
        print("[startup] WARNING dev tokens: no REVIEW_USERS configured; token == user name", file=sys.stderr)

    app = FastAPI(title=cfg.title)
    app.state.service = svc
    app.state.cfg = cfg
    ident = Identity(cfg)
    lock = threading.Lock()

    # ── identity ────────────────────────────────────────────────────────────
    def who(request: Request) -> Optional[tuple]:
        auth = request.headers.get("authorization", "")
        if auth:
            tok = auth[7:] if auth.lower().startswith("bearer ") else auth
            hit = ident.by_token(tok)
            if hit:
                return hit
        sid = request.cookies.get(COOKIE)
        if sid and sid in ident.sessions:
            return ident.sessions[sid]
        return None

    def need_user(request: Request) -> tuple:
        w = who(request)
        if not w:
            raise HTTPException(401, "log in first (cookie) or send Authorization: Bearer <token>")
        return w

    def need_admin(w: tuple):
        if w[1] != "admin":
            raise HTTPException(403, "admin role required")

    def wants_html(request: Request) -> bool:
        return "text/html" in request.headers.get("accept", "")

    def http(exc: ReviewError) -> HTTPException:
        return HTTPException(exc.status, str(exc))

    # ── pages ───────────────────────────────────────────────────────────────
    @app.get("/", response_class=HTMLResponse)
    def dashboard(request: Request):
        w = who(request)
        with lock:
            s = svc.status()
        return render.dashboard(s, cfg.public_names, cfg.title, w[0] if w else None, w[1] if w else None)

    @app.get("/health")
    def health():
        return {"ok": True, "tool": meta.tool, "tool_version": meta.tool_version, "prereg_status": meta.prereg_status}

    @app.get("/login", response_class=HTMLResponse)
    def login_form():
        return render.login_page(cfg.title, dev=cfg.dev_tokens)

    @app.post("/login")
    def login(user: str = Form(""), token: str = Form("")):
        hit = ident.by_token(token, user_hint=user)
        if not hit:
            return HTMLResponse(render.login_page(cfg.title, "unknown user or wrong token", dev=cfg.dev_tokens),
                                status_code=401)
        sid = ident.new_session(*hit)
        resp = RedirectResponse("/work", status_code=303)
        resp.set_cookie(COOKIE, sid, httponly=True, samesite="lax")
        return resp

    @app.post("/logout")
    @app.get("/logout")
    def logout(request: Request):
        sid = request.cookies.get(COOKIE)
        ident.sessions.pop(sid, None)
        resp = RedirectResponse("/", status_code=303)
        resp.delete_cookie(COOKIE)
        return resp

    @app.get("/work", response_class=HTMLResponse)
    def work(request: Request, msg: str = ""):
        w = who(request)
        if not w:
            return RedirectResponse("/login", status_code=303)
        user, role = w
        if role == "admin":
            return RedirectResponse("/audit", status_code=303)
        try:
            with lock:
                p = svc.claim(user, role)
        except ReviewError as exc:
            raise http(exc)
        if p is None:
            body = (f"<div class=card><h1>Queue empty</h1><p>Nothing left for stage "
                    f"{1 if role == 'screener' else 2} right now. Thank you.</p></div>")
            return render.page("Queue empty", body, user, role, cfg.title)
        return render.case_page(p, user, role, cfg.title, message=msg)

    @app.get("/case/{case_id}", response_class=HTMLResponse)
    def case_page(case_id: str, request: Request):
        user, role = need_user(request)
        try:
            with lock:
                p = svc.view(case_id, user, role)
        except ReviewError as exc:
            raise http(exc)
        return render.case_page(p, user, role, cfg.title)

    @app.get("/case/{case_id}/preview/{name}")
    def preview(case_id: str, name: str, request: Request):
        user, role = need_user(request)
        try:
            with lock:
                p = svc.preview_path(case_id, name, user, role)
        except ReviewError as exc:
            raise http(exc)
        return FileResponse(str(p))

    @app.post("/submit")
    def submit_form(request: Request, claim_token: str = Form(...), verdict: str = Form(...),
                    reason: str = Form("")):
        user, role = need_user(request)
        try:
            with lock:
                out = svc.submit(user, role, claim_token, verdict, reason)
        except ReviewError as exc:
            if wants_html(request):
                return HTMLResponse(render.page("Not recorded", f"<div class=card><div class=err>{render.esc(exc)}"
                                                f"</div><p><a href=/work>back to your case</a></p></div>",
                                                user, role, cfg.title), status_code=exc.status)
            raise http(exc)
        if wants_html(request):
            return RedirectResponse(f"/work?msg=Recorded+{out['verdict']}+for+{out['case_id']}", status_code=303)
        return out

    @app.post("/release")
    def release_form(request: Request, claim_token: str = Form(...)):
        user, role = need_user(request)
        try:
            with lock:
                out = svc.release(user, claim_token)
        except ReviewError as exc:
            raise http(exc)
        if wants_html(request):
            return RedirectResponse("/work?msg=Case+released", status_code=303)
        return out

    @app.get("/audit", response_class=HTMLResponse)
    def audit_html(request: Request):
        w = need_user(request)
        need_admin(w)
        with lock:
            rows = svc.audit_rows()
        return render.audit_page(rows, cfg.title, *w)

    @app.get("/audit.csv")
    def audit_csv(request: Request):
        w = need_user(request)
        need_admin(w)
        with lock:
            rows = svc.audit_rows()
        buf = io.StringIO()
        if rows:
            wr = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator="\n")
            wr.writeheader()
            wr.writerows(rows)
        return Response(buf.getvalue(), media_type="text/csv",
                        headers={"Content-Disposition": "attachment; filename=audit.csv"})

    # ── JSON API ────────────────────────────────────────────────────────────
    @app.get("/api/me")
    def api_me(w: tuple = Depends(need_user)):
        return {"user": w[0], "role": w[1]}

    @app.post("/api/claim")
    def api_claim(w: tuple = Depends(need_user)):
        try:
            with lock:
                p = svc.claim(*w)
        except ReviewError as exc:
            raise http(exc)
        if p is None:
            return Response(status_code=204)                     # queue empty: no body on a 204
        return p

    @app.post("/api/submit")
    def api_submit(claim_token: str = Form(...), verdict: str = Form(...), reason: str = Form(""),
                   w: tuple = Depends(need_user)):
        try:
            with lock:
                return svc.submit(w[0], w[1], claim_token, verdict, reason)
        except ReviewError as exc:
            raise http(exc)

    @app.post("/api/release")
    def api_release(claim_token: str = Form(...), w: tuple = Depends(need_user)):
        try:
            with lock:
                return svc.release(w[0], claim_token)
        except ReviewError as exc:
            raise http(exc)

    @app.get("/api/case/{case_id}")
    def api_case(case_id: str, w: tuple = Depends(need_user)):
        try:
            with lock:
                return svc.view(case_id, *w)
        except ReviewError as exc:
            raise http(exc)

    @app.get("/api/status")
    def api_status():
        with lock:
            return svc.status()

    @app.get("/api/audit")
    def api_audit(w: tuple = Depends(need_user)):
        need_admin(w)
        with lock:
            return svc.audit_rows()

    return app
