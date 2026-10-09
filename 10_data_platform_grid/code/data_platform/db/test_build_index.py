#!/usr/bin/env python3
"""Unit tests of build_index.py over a tiny synthetic layout (no grid, no network). Python 3.6+, standard library.

    python3 data_platform/db/test_build_index.py -v
"""
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "lib"))
import build_index  # noqa: E402
import mini_yaml    # noqa: E402

SOURCES = os.path.join(os.path.dirname(HERE), "sources.json")


def w(path, data=b"x" * 64):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if isinstance(data, bytes) else "w") as fh:
        fh.write(data)


def readme(root, folder, ids, adapter, restricted=False):
    w(os.path.join(root, folder, "README.yaml"),
      mini_yaml.dumps(dict(folder=folder, source_ids=ids, index_adapter=adapter, restricted=restricted)))


def make_tree(root):
    # CTSpinoPelvic1K release working copy
    base = os.path.join(root, "ctspinopelvic1k", "converted", "CTSpinoPelvic1K")
    recs = [dict(volume_id="0007", token="5", position="prone", sex="male", age_band="60-69", manufacturer="SIEMENS",
                 manufacturer_model="Sensation 16", prov_spine="manual", prov_pelvis="manual", castellvi_type="IIa",
                 castellvi_agreement=True, spine_series_uid="1.2.3", ct_file="ct/0007_ct.nii.gz", label_file="labels/0007_label.nii.gz"),
            dict(volume_id="0008", token="6", position="decubitus_right", sex="female", age_band="50-59", manufacturer="GE",
                 prov_spine="pseudo", prov_pelvis="pseudo", castellvi_type=None, spine_series_uid="1.2.4",
                 ct_file="ct/0008_ct.nii.gz", label_file="labels/0008_label.nii.gz")]
    w(os.path.join(base, "manifest.json"), json.dumps(recs))
    w(os.path.join(base, "splits_5fold.json"), json.dumps(dict(folds=[dict(fold=0, train=["5"], val=["6"])])))
    for v in ("0007", "0008"):
        w(os.path.join(base, "ct", v + "_ct.nii.gz"))
        w(os.path.join(base, "labels", v + "_label.nii.gz"))
    w(os.path.join(base, "labels_v10", "0007_label.nii.gz"))
    w(os.path.join(root, "ctspinopelvic1k", "derived", "ctsp_drr", "ann", "CTSP_COLONOG_5.json"), json.dumps(dict(levels={"20": {}}, view="lateral")))
    w(os.path.join(root, "ctspinopelvic1k", "derived", "ctsp_drr", "img", "CTSP_COLONOG_5.npy"))
    readme(root, "ctspinopelvic1k", ["ctspinopelvic1k", "ctsp_drr"], "ctsp_manifest")
    # VinDr
    v = os.path.join(root, "vindr_spinexr", "raw", "vindr", "1.0.0")
    w(os.path.join(v, "train_images", "aaaa1111.dicom"))
    w(os.path.join(v, "test_images", "bbbb2222.dicom"))
    w(os.path.join(v, "annotations", "train.csv"), "image_id,study_id,series_id,lesion_type\naaaa1111,deadbeef01,s1,Osteophytes\n")
    w(os.path.join(v, "annotations", "test.csv"), "image_id,study_id,series_id,lesion_type\nbbbb2222,deadbeef02,s2,No finding\n")
    readme(root, "vindr_spinexr", ["vindr_spinexr"], "vindr_csv", restricted=True)
    # BUU
    b = os.path.join(root, "buu_lspine_3600", "raw", "buu_full", "BUU-LSPINEv1")
    w(os.path.join(b, "AP", "0001-F-037Y0.jpg"))
    w(os.path.join(b, "AP", "0001-F-037Y0.csv"), "x\n")
    w(os.path.join(b, "LA", "0001-F-037Y1.jpg"))
    readme(root, "buu_lspine_3600", ["buu_lspine_3600"], "buu", restricted=True)
    # NHANES films
    for f in ("C00160.tiff", "L00160.tiff"):
        w(os.path.join(root, "nhanes2_cdc_films", "raw", "nhanes_full", f))
    readme(root, "nhanes2_cdc_films", ["nhanes2_cdc_films"], "nhanes_tiff")
    # realxray banks
    rx = os.path.join(root, "realxray")
    w(os.path.join(rx, "carmlspine", "images", "train", "case1_AP.png"))
    w(os.path.join(rx, "carmlspine", "labels", "train", "case1_AP.txt"), "0 0.5 0.5 0.1 0.1\n")
    w(os.path.join(rx, "carmlspine", "meta", "case1_AP.json"), json.dumps(dict(case="case1", split="train", px_mm=0.19,
      device=dict(make="FIRST", model="Surgio-B51", kvp=80), view=dict(lat_from_ap_deg=0.5), boxes=[dict(cls=0, level="L4")])))
    w(os.path.join(rx, "deepfluoro", "images", "test", "17-1882_000.png"))
    w(os.path.join(rx, "deepfluoro", "meta", "17-1882_000.json"), json.dumps(dict(case="17-1882", split="test", view=dict(lat_from_ap_deg=30))))
    readme(root, "realxray", ["carmlspine", "deepfluoro_h5", "cobra2026", "geneva_hip", "realxray_layout"], "realxray_meta")
    # an acquisition collection with its screen
    ct = os.path.join(root, "csi2014", "nifti", "csi_01_ct.nii.gz")
    w(ct)
    w(os.path.join(root, "anomaly_harvest", "csi2014", "cases.csv"),
      "case,ct,source,patient_key,extent_mm,dz_mm,pixel_sha1\ncsi_01,%s,csi2014,csi2014:01,400,1.0,abc\n" % ct)
    w(os.path.join(root, "anomaly_harvest", "csi2014", "rows.csv"),
      "source,case,patient_key,subtype,labeller_a,labeller_b,agree,truth_tier,n_lumbar\ncsi2014,csi_01,csi2014:01,ordinary,LS ordinary,LS no count,,single-labeller,5\n")
    w(os.path.join(root, "csi2014", "fetch", "verified.jsonl"),
      json.dumps(dict(unit="csi_01_image.mha", t="x")) + "\n" + json.dumps(dict(unit="csi_02_image.mha", t="x")) + "\n")
    w(os.path.join(root, "csi2014", "fetch", "FETCH_STATUS.json"), json.dumps(dict(verified_units=2, unresolved_failures=0)))
    readme(root, "csi2014", ["csi2014"], "acquisition")
    # banks of several sources
    mb = os.path.join(root, "multisource_banks", "derived")
    w(os.path.join(mb, "films_drr", "ann", "CSXA_csxa_0001035.json"), json.dumps(dict(levels={"3": {}}, view="LAT")))
    w(os.path.join(mb, "films_drr", "img", "CSXA_csxa_0001035.npy"))
    w(os.path.join(mb, "allspine_v9_fov96_ctx", "rung_1.npz"))
    w(os.path.join(mb, "allspine_v9_fov96_ctx", "meta.json"), "{}")
    readme(root, "multisource_banks", ["multisource_banks"], "render_bank")
    # TotalSegmentator
    ts = os.path.join(root, "totalsegmentator_v201", "raw", "TotalSegmentator")
    w(os.path.join(ts, "meta.csv"), "image_id;age;gender;split;study_type\ns0001;61;m;train;ct abdomen-pelvis\n")
    w(os.path.join(ts, "s0001", "ct.nii.gz"))
    w(os.path.join(ts, "s0001", "segmentations", "vertebrae_L1.nii.gz"))
    readme(root, "totalsegmentator_v201", ["totalsegmentator_v201", "ts_drr"], "totalsegmentator")
    # generic
    w(os.path.join(root, "spinesac", "drive", "a", "frame.png"))
    readme(root, "spinesac", ["spinesac"], "generic")
    # a DICOM tree (no pydicom needed: per-file projections, a CBCT series directory, a converted NIfTI)
    c = os.path.join(root, "carmlspine")
    w(os.path.join(c, "raw", "C-ArmLSpine", "case1", "C-arm", "a.dcm"))
    w(os.path.join(c, "raw", "C-ArmLSpine", "case1", "C-arm", "b.dcm"))
    for i in range(3):
        w(os.path.join(c, "raw", "C-ArmLSpine", "case1", "CBCT", "%d.dcm" % i))
    w(os.path.join(c, "nifti", "case1_cbct.nii.gz"))
    readme(root, "carmlspine", ["carmlspine"], "dicom_tree")
    # a folder without README.yaml is ignored
    w(os.path.join(root, "no_readme", "x.png"))
    # --- folders the 2026-10-08 verifiers probed --------------------------------------------------------------------
    # CTSpine1K (generic): the _seg mask attaches to its image; the duplicate HOME copy is skipped by index_skip
    cs = os.path.join(root, "ctspine1k", "raw", "raw_data", "rawdata")
    w(os.path.join(cs, "data", "COLONOG", "1.3.6_ct.nii.gz"))
    w(os.path.join(cs, "labels", "COLONOG", "1.3.6_seg.nii.gz"))
    w(os.path.join(cs, "data", "COLONOG", "1.3.7_ct.nii.gz"))                # no mask in a folder that has masks
    w(os.path.join(root, "ctspine1k", "raw", "home_copy", "COLONOG", "1.3.6_ct.nii.gz"))
    w(os.path.join(root, "ctspine1k", "README.yaml"),
      mini_yaml.dumps(dict(folder="ctspine1k", source_ids=["ctspine1k"], index_adapter="generic", index_skip=["raw/home_copy"])))
    # AASCE and FluoroCap films (generic): the release's status applies, marked per-release
    w(os.path.join(root, "aasce2019_boostnet", "raw", "aasce", "data", "training", "sunhl-1th-01.jpg"))
    w(os.path.join(root, "aasce2019_boostnet", "raw", "aasce", "labels", "training", "sunhl-1th-01.jpg.mat"))
    readme(root, "aasce2019_boostnet", ["aasce2019_boostnet"], "generic")
    w(os.path.join(root, "fluorocap", "raw", "FluoroCap", "panels", "p1.png"))
    readme(root, "fluorocap", ["fluorocap"], "generic")
    # TCIA (dicom_tree): one series under raw/, its dcm2niix conversion under tcia_nifti/ is kept but not counted
    for i in range(3):
        w(os.path.join(root, "tcia_ct_colonography", "raw", "tcia", "1.2.840.1", "%d.dcm" % i))
    w(os.path.join(root, "tcia_ct_colonography", "converted", "tcia_nifti", "1.2.840.1.nii.gz"))
    readme(root, "tcia_ct_colonography", ["tcia_ct_colonography"], "dicom_tree")
    # VerSeFusion as the layout maps it: raw/ (verse19_20), canonical/ (versefusion), unified/ (links, not indexed)
    vd = os.path.join(root, "versefusion", "raw", "VerSeFusion_data")
    w(os.path.join(vd, "raw", "sub-gl003", "sub-gl003_ct.nii.gz"))
    w(os.path.join(vd, "raw", "sub-gl003", "sub-gl003_seg-vert_msk.nii.gz"))
    w(os.path.join(vd, "canonical", "gl003", "gl003_ct.nii.gz"))
    w(os.path.join(vd, "canonical", "gl003", "gl003_seg.nii.gz"))
    w(os.path.join(vd, "unified", "gl003", "gl003_ct.nii.gz"))            # a copy where the layout keeps links
    readme(root, "versefusion", ["verse19_20", "versefusion"], "verse")
    # a hard link inside a release folder counts once
    rf = os.path.join(root, "ribfrac", "raw")
    w(os.path.join(rf, "RibFrac1-image.nii.gz"))
    os.makedirs(os.path.join(rf, "dup"), exist_ok=True)
    try:
        os.link(os.path.join(rf, "RibFrac1-image.nii.gz"), os.path.join(rf, "dup", "RibFrac1-image.nii.gz"))
    except OSError:
        pass
    readme(root, "ribfrac", ["ribfrac"], "generic")
    # an acquisition collection whose DICOM states the position; the CTSP harvest call attaches to its item
    ct2 = os.path.join(root, "nlst_pilot", "nifti", "nlst_100_ct.nii.gz")
    w(ct2)
    w(os.path.join(root, "anomaly_harvest", "nlst_pilot", "cases.csv"),
      "case,ct,source,patient_key,extent_mm,dz_mm,pixel_sha1\nnlst_100,%s,nlst,nlst:100,500,1.0,def\n" % ct2)
    w(os.path.join(root, "anomaly_harvest", "nlst_pilot", "convert", "shard0.jsonl"), json.dumps(dict(item="9.9.9", case="nlst_100")) + "\n")
    w(os.path.join(root, "nlst_pilot", "fetch", "verified.jsonl"), json.dumps(dict(unit="9.9.9", patient="100", dir="raw/100/9.9.9")) + "\n")
    write_dicom(os.path.join(root, "nlst_pilot", "raw", "100", "9.9.9", "1.dcm"))
    readme(root, "nlst_pilot", ["nlst_pilot"], "acquisition")
    w(os.path.join(root, "anomaly_harvest", "ctsp", "rows.csv"),
      "source,case,patient_key,subtype,labeller_a,labeller_b,agree,truth_tier\nctsp,ctsp_0007,ctsp:0007,sacralization,LS sac,LS sac,1,two-labeller\n")


def write_dicom(path):
    """A header-only DICOM stating PatientPosition HFS (skipped when pydicom is absent)."""
    if build_index.pydicom is None:
        return
    from pydicom.dataset import Dataset, FileMetaDataset
    from pydicom.uid import ExplicitVRLittleEndian, generate_uid
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ds = Dataset()
    ds.PatientPosition, ds.StudyDate, ds.Manufacturer, ds.SeriesInstanceUID, ds.Modality = "HFS", "20020101", "GE", "9.9.9", "CT"
    ds.file_meta = FileMetaDataset()
    ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    ds.file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.2"
    ds.file_meta.MediaStorageSOPInstanceUID = generate_uid()
    try:
        ds.save_as(path, enforce_file_format=True)
    except TypeError:                     # pydicom 2
        ds.is_little_endian, ds.is_implicit_VR = True, False
        ds.save_as(path, write_like_original=False)


class BuildIndexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="dp_index_")
        cls.root = os.path.join(cls.tmp, "data")
        make_tree(cls.root)
        cls.db = os.path.join(cls.tmp, "holding.sqlite")
        rc = build_index.main(["--root", cls.root, "--db", cls.db, "--sources", SOURCES, "--allow-local"])
        assert rc == 0
        cls.con = sqlite3.connect(cls.db)

    @classmethod
    def tearDownClass(cls):
        cls.con.close()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def q(self, sql, *a):
        return self.con.execute(sql, a).fetchall()

    def test_sources_loaded(self):
        n = self.q("SELECT COUNT(*) FROM source")[0][0]
        self.assertGreaterEqual(n, 200)
        self.assertEqual(self.q("SELECT restricted FROM source WHERE source_id='vindr_spinexr'")[0][0], 1)

    def test_ctsp_manifest(self):
        rows = dict(self.q("SELECT case_id, position FROM item WHERE source_id='ctspinopelvic1k'"))
        self.assertEqual(rows, {"0007": "prone", "0008": "decubitus"})
        kinds = sorted(r[0] for r in self.q("SELECT a.kind FROM annotation a JOIN item i USING(item_id) WHERE i.case_id='0007' AND i.source_id='ctspinopelvic1k'"))
        self.assertEqual(kinds, ["expert", "expert", "expert", "release_labels", "reviewed", "two_labeller"])   # + the harvest call
        self.assertEqual(self.q("SELECT part FROM split s JOIN item i USING(item_id) WHERE i.case_id='0008'")[0][0], "val")
        self.assertEqual(self.q("SELECT sex FROM subject WHERE subject_key='ctsp:0007'")[0][0], "male")

    def test_render_bank_inside_a_source_folder(self):
        r = self.q("SELECT source_id, modality, view FROM item WHERE path LIKE '%ctsp_drr%'")
        self.assertEqual(r, [("ctsp_drr", "RENDER", "LAT")])

    def test_vindr(self):
        r = dict(self.q("SELECT i.case_id, a.kind FROM item i JOIN annotation a USING(item_id) WHERE i.source_id='vindr_spinexr'"))
        self.assertEqual(r, {"aaaa1111": "release_labels", "bbbb2222": "none"})
        self.assertEqual(len(self.q("SELECT 1 FROM split WHERE experiment='vindr_release'")), 2)

    def test_buu_view_and_position(self):
        r = sorted(self.q("SELECT view, position, subject_key FROM item WHERE source_id='buu_lspine_3600'"))
        self.assertEqual(r, [("AP", "standing", "buu:0001"), ("LAT", "standing", "buu:0001")])

    def test_nhanes_one_subject_two_films(self):
        r = self.q("SELECT subject_key, COUNT(*) FROM item WHERE source_id='nhanes2_cdc_films' GROUP BY subject_key")
        self.assertEqual(r, [("nhanes:00160", 2)])

    def test_realxray(self):
        r = sorted(self.q("SELECT source_id, modality, view, subject_key FROM item WHERE adapter='realxray_meta'"))
        self.assertEqual(r, [("carmlspine", "XA", "AP", "carmlspine:case1"), ("deepfluoro_h5", "RF", "OBL", "deepfluoro:17-1882")])

    def test_acquisition(self):
        r = self.q("SELECT i.subject_key, a.kind, a.status FROM item i JOIN annotation a USING(item_id) WHERE i.source_id='csi2014'")
        self.assertEqual(r, [("csi2014:01", "two_labeller", "ordinary")])

    def test_fetch_state_recorded(self):
        st = json.loads(self.q("SELECT fetch_status FROM folder WHERE folder LIKE '%csi2014'")[0][0])
        self.assertEqual((st["verified_jsonl_units"], st["unresolved_failures"]), (2, 0))

    def test_multisource_and_crop_bank(self):
        r = sorted(self.q("SELECT format, modality FROM item WHERE source_id='multisource_banks'"))
        self.assertEqual(r, [("crop_bank", "OTHER"), ("npy", "DX")])

    def test_totalsegmentator(self):
        r = self.q("SELECT i.subject_key, s.part FROM item i JOIN split s USING(item_id) WHERE i.source_id='totalsegmentator_v201'")
        self.assertEqual(r, [("ts:s0001", "train")])

    def test_generic_and_no_readme(self):
        self.assertEqual(len(self.q("SELECT 1 FROM item WHERE source_id='spinesac'")), 1)
        self.assertEqual(len(self.q("SELECT 1 FROM item WHERE path LIKE '%no_readme%'")), 0)

    def test_dicom_tree(self):
        r = sorted(self.q("SELECT modality, format, view, subject_key FROM item WHERE source_id='carmlspine' AND adapter IN ('dicom_tree', 'generic')"))
        if build_index.pydicom is None:
            self.assertEqual(r, [("CBCT", "dicom_series", "volume", "carmlspine:case1"), ("CBCT", "nifti", "volume", None),
                                 ("XA", "dicom", "unknown", "carmlspine:case1"), ("XA", "dicom", "unknown", "carmlspine:case1")])
        else:
            self.assertEqual(len(r), 4)

    def test_views(self):
        v1 = self.q("SELECT modality, position, annotation_kind FROM v_annotated_ct_by_modality_position")
        self.assertIn(("CT", "prone", "expert"), v1)
        v2 = dict(((s, v), n) for s, v, n, _ in self.q("SELECT * FROM v_unannotated_films_by_view"))
        self.assertEqual(v2.get(("buu_lspine_3600", "LAT")), 1)
        self.assertEqual(v2.get(("nhanes2_cdc_films", "LAT")), 2)
        self.assertGreaterEqual(len(self.q("SELECT * FROM v_subject_items WHERE subject_key='ctsp:0007'")), 1)
        self.assertGreaterEqual(len(self.q("SELECT * FROM v_source_summary")), 200)

    def test_masks_attach_to_their_image(self):
        r = self.q("SELECT i.case_id, i.role, i.counted, a.kind, a.path FROM item i JOIN annotation a USING(item_id) "
                   "WHERE i.source_id='ctspine1k' ORDER BY i.path")
        names = [(os.path.basename(x[4]) if x[4] else "", x[3], x[1], x[2]) for x in r]
        self.assertEqual(names, [("1.3.6_seg.nii.gz", "expert", "raw", 1), ("", "none", "raw", 1)])
        self.assertEqual(self.q("SELECT COUNT(*) FROM item WHERE path LIKE '%_seg.nii.gz'")[0][0], 0, "a mask is not an item")
        self.assertEqual(self.q("SELECT COUNT(*) FROM item WHERE path LIKE '%home_copy%'")[0][0], 0, "index_skip honoured")

    def test_release_status_applies_per_release(self):
        r = dict((s, (k, json.loads(d).get("scope"))) for s, k, d in self.q(
            "SELECT i.source_id, a.kind, a.detail FROM item i JOIN annotation a USING(item_id) WHERE i.source_id IN ('aasce2019_boostnet','fluorocap')"))
        self.assertEqual(r["aasce2019_boostnet"], ("release_labels", "per-release, not read from the file"))
        self.assertEqual(r["fluorocap"][0], "pseudo")
        films = dict(((s, v), n) for s, v, n, _ in self.q("SELECT * FROM v_unannotated_films_by_view"))
        self.assertNotIn(("aasce2019_boostnet", "unknown"), films)

    def test_conversions_kept_not_counted(self):
        r = sorted(self.q("SELECT format, role, counted FROM item WHERE source_id='tcia_ct_colonography'"))
        self.assertEqual(r, [("dicom_series", "raw", 1), ("nifti", "converted", 0)])

    def test_verse_roles_from_the_path(self):
        r = sorted(self.q("SELECT source_id, role, case_id FROM item WHERE adapter='verse'"))
        self.assertEqual(r, [("verse19_20", "raw", "gl003"), ("versefusion", "converted", "gl003")])

    def test_hard_link_counted_once(self):
        r = self.q("SELECT counted, duplicate_of IS NOT NULL FROM item WHERE source_id='ribfrac' ORDER BY path")
        if len(r) == 2:
            self.assertEqual(sorted(r), [(0, 1), (1, 0)])
            self.assertEqual(len(self.q("SELECT 1 FROM lineage WHERE relation='copy_of'")), 1)

    def test_acquisition_position_from_dicom(self):
        if build_index.pydicom is None:
            self.skipTest("pydicom absent")
        r = self.q("SELECT position, acquisition_date, device, series_uid FROM item WHERE source_id='nlst_pilot'")
        self.assertEqual(r, [("supine", "20020101", "GE", "9.9.9")])

    def test_harvest_calls_on_ctsp(self):
        r = self.q("SELECT a.status FROM annotation a JOIN item i USING(item_id) WHERE i.case_id='0007' AND a.kind='two_labeller'")
        self.assertEqual(r, [("sacralization",)])

    def test_source_table_carries_annotation_and_position(self):
        a, p = self.q("SELECT annotation_status, position FROM source WHERE source_id='buu_lspine_3600'")[0]
        self.assertTrue(json.loads(a))
        self.assertIsInstance(json.loads(p), list)

    def test_zz_incremental(self):
        total = self.q("SELECT COUNT(*) FROM item")[0][0]
        rc = build_index.main(["--root", self.root, "--db", self.db, "--sources", SOURCES, "--allow-local"])
        self.assertEqual(rc, 0)
        run = self.q("SELECT n_new, n_updated, n_unchanged, n_removed FROM index_run ORDER BY run_id DESC LIMIT 1")[0]
        self.assertEqual(run, (0, 0, total, 0))
        # change one file, delete another
        w(os.path.join(self.root, "nhanes2_cdc_films", "raw", "nhanes_full", "C00160.tiff"), b"y" * 99)
        os.remove(os.path.join(self.root, "spinesac", "drive", "a", "frame.png"))
        build_index.main(["--root", self.root, "--db", self.db, "--sources", SOURCES, "--allow-local"])
        run = self.q("SELECT n_new, n_updated, n_removed FROM index_run ORDER BY run_id DESC LIMIT 1")[0]
        self.assertEqual(run, (0, 1, 1))
        self.assertEqual(self.q("SELECT COUNT(*) FROM item")[0][0], total - 1)

    def test_refuses_outside_slurm(self):
        old = os.environ.pop("SLURM_JOB_ID", None)
        try:
            self.assertEqual(build_index.main(["--root", self.root, "--db", self.db + ".x", "--sources", SOURCES]), 2)
        finally:
            if old is not None:
                os.environ["SLURM_JOB_ID"] = old


if __name__ == "__main__":
    unittest.main()
