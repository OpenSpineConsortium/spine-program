// Content of the inventor's responses to counsel, WSU 26-1902 / FS 66174-0372.
// Inline markup: **bold**, *italic*, [text](url). Status tags: SHOWN, RENDER, INFERRED, NOTREC, DESIGN.

const SP = "https://github.com/OpenSpineConsortium/spine-program/blob/240cabc/";
const SS = "https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet/blob/0ab783f/";
const SC = "https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet/commit/";

const L = {
  spec: [`SPECIFICATION.md`, SP + "provisional_patent/provisional/SPECIFICATION.md"],
  claims: [`CLAIMS.md`, SP + "provisional_patent/provisional/CLAIMS.md"],
  readme: [`00_README_for_TTO.md`, SP + "provisional_patent/wsu_tto/TTO_package_2026-09-25/00_README_for_TTO.md"],
  timeline: [`06_disclosure_timeline.md`, SP + "provisional_patent/wsu_tto/TTO_package_2026-09-25/06_disclosure_timeline.md"],
  scrub: [`SCRUB_PLAN.md`, SP + "provisional_patent/wsu_tto/TTO_package_2026-09-25/SCRUB_PLAN.md"],
  memo: [`DISCLOSURE_MEMO.md`, SP + "provisional_patent/DISCLOSURE_MEMO.md"],
  guidedP: [`GUIDED_ACQUISITION.md`, SP + "provisional_patent/GUIDED_ACQUISITION.md"],
  idfP: [`INVENTION_DISCLOSURE.md`, SP + "provisional_patent/INVENTION_DISCLOSURE.md"],
  status01: [`01 STATUS.md`, SP + "01_carm_level_detection/STATUS.md"],
  todo01: [`01 TODO.md`, SP + "01_carm_level_detection/TODO.md"],
  catalog: [`RESULTS_CATALOG.md, rows C3`, SP + "01_carm_level_detection/docs/handoff/RESULTS_CATALOG.md"],
  sweepmem: [`sweep-map-replaces-registration.md`, SP + "01_carm_level_detection/docs/handoff/context/sweep-map-replaces-registration.md"],
  spacing: [`drr-row-spacing-defect.md`, SP + "01_carm_level_detection/docs/handoff/context/drr-row-spacing-defect.md"],
  selmem: [`selective-prediction-the-honest-99.md`, SP + "01_carm_level_detection/docs/handoff/context/selective-prediction-the-honest-99.md"],
  partA: [`CT_LSTV_CLASSIFIER_PLAN.md`, SP + "06_transitional_ct_census/docs/CT_LSTV_CLASSIFIER_PLAN.md"],
  r33: [`CLASSIFIERS.md (R33)`, SP + "06_transitional_ct_census/docs/ruleclass/CLASSIFIERS.md"],
  cost: [`WRONG_LEVEL_COST_EVIDENCE.md, lines 69-75`, SP + "09_wrong_level_clinical_qi/docs/WRONG_LEVEL_COST_EVIDENCE.md#L69-L75"],
  counting: [`COUNTING_EVIDENCE.md`, SS + "docs/COUNTING_EVIDENCE.md"],
  physics: [`HANDOFF_PHYSICS.md`, SS + "docs/HANDOFF_PHYSICS.md"],
  card: [`MODEL_CARD.md`, SS + "docs/MODEL_CARD.md"],
  card63: [`MODEL_CARD.md section 6.3`, SS + "docs/MODEL_CARD.md#63-what-it-measures-on-the-workstation-2026-09-22"],
  card3: [`MODEL_CARD.md section 3`, SS + "docs/MODEL_CARD.md#3-training-data"],
  protocol: [`SWEEP_PROTOCOL.md`, SS + "docs/SWEEP_PROTOCOL.md"],
  guided: [`GUIDED_ACQUISITION.md (code repository)`, SS + "docs/GUIDED_ACQUISITION.md"],
  priorart: [`PRIOR_ART_LEVEL_ID_XRAY.md`, SS + "docs/PRIOR_ART_LEVEL_ID_XRAY.md"],
  idfS: [`INVENTION_DISCLOSURE.md, freedom-to-operate table`, SS + "docs/INVENTION_DISCLOSURE.md#L250-L262"],
  sxreq: [`SX-Stitch_request.md (draft, not sent)`, SS + "docs/data_requests/SX-Stitch_request.md"],
  pitch: [`sweep_map.py L103-104 (spacing constants, field presets)`, SS + "tools/sweep_map.py#L103-L104"],
  endrule: [`sweep_map.py L401 (end rule)`, SS + "tools/sweep_map.py#L401"],
  repair: [`sweep_map.py L682 repair_boxes`, SS + "tools/sweep_map.py#L682"],
  ncc: [`sweep_map.py L952 ncc_shift`, SS + "tools/sweep_map.py#L952"],
  link: [`sweep_map.py L1065 link_pair`, SS + "tools/sweep_map.py#L1065"],
  global: [`sweep_map.py L1177 build_chain_global`, SS + "tools/sweep_map.py#L1177"],
  jitter: [`sweep_map.py L1320-1325 (window, jitter)`, SS + "tools/sweep_map.py#L1320-L1325"],
  alpha: [`sweep_map.py L1387 alphabet, L1436 decode_alphabets`, SS + "tools/sweep_map.py#L1387"],
  pano: [`sweep_map.py L1535-1538 map_query_panorama`, SS + "tools/sweep_map.py#L1535-L1538"],
  emb: [`sweep_map.py L1636 map_query_emb`, SS + "tools/sweep_map.py#L1636"],
  tau: [`acquisition.py L65 (tau)`, SS + "tools/acquisition.py#L65"],
  plan: [`acquisition.py L229 plan_run`, SS + "tools/acquisition.py#L229"],
  conf: [`acquisition.py L500 _confidence`, SS + "tools/acquisition.py#L500"],
  seam: [`acquisition.py L523 offset_to_seam`, SS + "tools/acquisition.py#L523"],
  decide: [`acquisition.py L649 _decide`, SS + "tools/acquisition.py#L649"],
  board: [`acquisition.py L855 FiducialBoard`, SS + "tools/acquisition.py#L855"],
  console: [`guided_console.py (operator console)`, SS + "tools/guided_console.py"],
  selective: [`level_selective.py`, SS + "tools/level_selective.py"],
  tests: [`tests/test_acquisition.py`, SS + "tests/test_acquisition.py"],
};

const c = (sha, what) => [`commit ${sha} (${what})`, SC + sha];

module.exports = { SP, SS, SC, L, c };

// Where each linked file sits in the package sent to counsel.
function packagePath(url) {
  if (url.startsWith(SC)) return "05_Evidence/CONCEPTION_RECORD.txt";
  const clean = url.split("#")[0];
  if (clean.startsWith(SP)) {
    const p = clean.slice(SP.length);
    if (p.startsWith("provisional_patent/provisional/")) return "02_Draft_Provisional/" + p.split("/").pop();
    if (p.startsWith("provisional_patent/wsu_tto/TTO_package_2026-09-25/SCRUB_PLAN.md")) return "03_Disclosure_Records/SCRUB_PLAN.md";
    if (p.startsWith("provisional_patent/wsu_tto/TTO_package_2026-09-25/")) return "04_WSU_TTO_Package/" + p.split("/").pop();
    if (p.startsWith("provisional_patent/")) return "03_Disclosure_Records/" + p.split("/").pop();
    return "05_Evidence/spine-program/" + p;
  }
  if (clean.startsWith(SS)) return "05_Evidence/spinesurg-ct-nnunet/" + clean.slice(SS.length);
  return null;
}
module.exports.packagePath = packagePath;
