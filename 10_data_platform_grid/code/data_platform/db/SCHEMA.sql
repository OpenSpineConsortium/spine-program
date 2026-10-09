-- SCHEMA.sql: the index of the imaging holding on /rs/rs_grp_oschome/go2432/data (SQLite 3; also loads in DuckDB).
-- Built by data_platform/db/build_index.py, which walks the layout in data_platform/LAYOUT.md one source folder at a
-- time (each folder's README.yaml names its source ids and the adapter that reads it). Nothing here is truth that a
-- file does not hold: every row points at a path, and every annotation row says who or what produced it.
--
-- Conventions
--   subject_key   '<corpus>:<person>' in the spelling of tools/patient_keys.py canon_key (ctsp ids zero-padded to 4,
--                 NHANES to 5, C-ArmLSpine 'case<N>', VinDr the study_id); NULL when the source has no person key
--                 (FluoroCap, Spinal-AI2024, phantoms keyed by phantom).
--   modality      what one item is: CT volume, CBCT volume or projection sweep, CR/DX plain film, RF fluoroscopy frame
--                 or clip, XA angiographic/C-arm spot frame (DICOM XA), RENDER (synthetic DRR or generated image).
--   position      patient position at acquisition where a file states it (DICOM 0018,5100, a release manifest);
--                 'unknown' otherwise. Never inferred from the anatomy.
--   view          AP / PA / LAT / OBL for a projection, 'sweep' for a rotational series, 'volume' for a 3-D image.
--   annotation.kind
--                 none            the file has no labels
--                 release_labels  labels shipped by the upstream release (as the release describes them)
--                 pseudo          produced by a model or a projection of another label, not checked by a person
--                 two_labeller    two independent model labellers, level kept only where they agree
--                 expert          drawn or corrected by a radiologist or trained annotator (per the release or our ledgers)
--                 reviewed        a person looked at a model output and accepted or corrected it
--                 unknown         the release's annotation status is not recorded (sources.json says unknown)
--                 A row whose detail says scope "per-release" carries the release's status from sources.json; it was
--                 not read from a label file beside the item.
--   counted       1 for one acquisition of a source; 0 for a hard-link copy of another item (duplicate_of), a
--                 conversion or derived output kept beside a release, an orphan mask, or a release archive whose
--                 unpacked files are the items. The views count counted = 1 only.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS source (
    source_id        TEXT PRIMARY KEY,           -- sources.yaml id
    name             TEXT NOT NULL,
    kind             TEXT,                       -- upstream_release | project_release | derived | derived_root | request | unknown
    status           TEXT,                       -- on_disk | planned | gated | excluded | ...
    family           TEXT,                       -- A..E (DATA_MANIFEST.md)
    modality         TEXT,                       -- JSON list
    anatomy          TEXT,                       -- JSON list
    licence          TEXT,
    access           TEXT,
    restricted       INTEGER NOT NULL DEFAULT 0, -- 1 = DUA or EULA: never group-readable, never redistributed
    layout_path      TEXT,                       -- $RS/data/<folder>[/subpath]
    doi_or_url       TEXT,                       -- JSON list
    manifest_anchor  TEXT,
    reacquire_route  TEXT,
    annotation_status TEXT,                      -- JSON list: sources.json annotation.status (per release)
    annotation_kinds TEXT,                       -- JSON list: sources.json annotation.kinds
    position         TEXT,                       -- JSON list: sources.json position_view.position (per release)
    view             TEXT,                       -- JSON list: sources.json position_view.view
    loaded_from      TEXT                        -- sources.json sha256 at load time
);

CREATE TABLE IF NOT EXISTS subject (
    subject_key  TEXT PRIMARY KEY,
    corpus       TEXT NOT NULL,
    person       TEXT NOT NULL,
    key_rule     TEXT,                           -- how the key was read (file name, manifest field, DICOM tag)
    sex          TEXT,
    age_band     TEXT,
    notes        TEXT
);

CREATE TABLE IF NOT EXISTS item (
    item_id          INTEGER PRIMARY KEY,
    source_id        TEXT NOT NULL REFERENCES source(source_id),
    subject_key      TEXT REFERENCES subject(subject_key),
    case_id          TEXT,                       -- the release's own case / volume / image id
    modality         TEXT NOT NULL CHECK (modality IN ('CT','CBCT','CR','DX','RF','XA','MR','RENDER','OTHER')),
    body_region      TEXT,                       -- cervical | thoracic | lumbar | pelvis | whole_spine | ... (as stated)
    position         TEXT NOT NULL DEFAULT 'unknown'
                     CHECK (position IN ('supine','prone','standing','decubitus','unknown')),
    view             TEXT NOT NULL DEFAULT 'unknown'
                     CHECK (view IN ('AP','PA','LAT','OBL','sweep','volume','unknown')),
    device           TEXT,
    px_mm            REAL,                       -- projection pixel size at the detector or object plane (as stated)
    spacing          TEXT,                       -- volume voxel spacing 'x,y,z' mm when read
    extent           TEXT,                       -- 'rows x cols' or 'x,y,z' when read
    acquisition_date TEXT,                       -- only when the release ships it (DICOM StudyDate, metadata.yaml)
    path             TEXT NOT NULL UNIQUE,       -- absolute path (a file, or a DICOM series directory)
    role             TEXT CHECK (role IN ('raw','converted','derived','labels','meta')),
    format           TEXT,                       -- nifti | dicom_series | dicom | png | jpg | tiff | mha | h5 | npy | pkl | archive | crop_bank
    bytes            INTEGER,
    mtime            REAL,
    sha256           TEXT,                       -- filled only by --hash
    series_uid       TEXT,
    adapter          TEXT,
    extra            TEXT,                       -- JSON: anything else the adapter read (kVp, split, study_type, ...)
    inode            TEXT,                       -- 'dev:ino' of a file with more than one hard link
    duplicate_of     INTEGER,                    -- the item this file is a hard link of (counted = 0)
    counted          INTEGER NOT NULL DEFAULT 1, -- see Conventions
    run_id           INTEGER                     -- the index_run that last wrote this row
);
CREATE INDEX IF NOT EXISTS item_source   ON item(source_id);
CREATE INDEX IF NOT EXISTS item_subject  ON item(subject_key);
CREATE INDEX IF NOT EXISTS item_modality ON item(modality, position, view);
CREATE INDEX IF NOT EXISTS item_inode    ON item(inode);

CREATE TABLE IF NOT EXISTS annotation (
    annotation_id INTEGER PRIMARY KEY,
    item_id       INTEGER NOT NULL REFERENCES item(item_id) ON DELETE CASCADE,
    kind          TEXT NOT NULL CHECK (kind IN ('none','release_labels','pseudo','two_labeller','expert','reviewed','unknown')),
    labeller      TEXT NOT NULL DEFAULT '',      -- e.g. 'CTSpine1K radiologists', 'TotalSegmentator 2.18', 'SPINEPS+VERIDAH'
    version       TEXT NOT NULL DEFAULT '',      -- e.g. 'CTSP v11', 'labels_v10'
    path          TEXT NOT NULL DEFAULT '',      -- the label file, when it is a file
    status        TEXT,                          -- e.g. 'agree', 'disagree', 'needs_review', a call
    detail        TEXT,                          -- JSON
    UNIQUE (item_id, kind, labeller, version, path)
);
CREATE INDEX IF NOT EXISTS annotation_kind ON annotation(kind);

CREATE TABLE IF NOT EXISTS split (
    experiment   TEXT NOT NULL,                  -- e.g. 'ctsp_splits_5fold', 'realxray:carmlspine', 'vindr_release'
    item_id      INTEGER NOT NULL REFERENCES item(item_id) ON DELETE CASCADE,
    part         TEXT NOT NULL,                  -- train | val | test | fold<k>
    source_file  TEXT,
    PRIMARY KEY (experiment, item_id)
);

CREATE TABLE IF NOT EXISTS lineage (
    derived_item_id INTEGER NOT NULL REFERENCES item(item_id) ON DELETE CASCADE,
    source_ref      TEXT NOT NULL,               -- a source item path or a case id the derived file names
    source_item_id  INTEGER REFERENCES item(item_id) ON DELETE SET NULL,
    relation        TEXT,                        -- rendered_from | converted_from | crop_of | symlink_to | copy_of
    tool            TEXT,
    PRIMARY KEY (derived_item_id, source_ref)
);

-- bookkeeping for incremental runs
CREATE TABLE IF NOT EXISTS index_run (
    run_id      INTEGER PRIMARY KEY,
    started     TEXT, finished TEXT, root TEXT, host TEXT, slurm_job TEXT,
    n_new INTEGER DEFAULT 0, n_updated INTEGER DEFAULT 0, n_unchanged INTEGER DEFAULT 0, n_removed INTEGER DEFAULT 0,
    notes TEXT
);
CREATE TABLE IF NOT EXISTS folder (
    folder        TEXT PRIMARY KEY,              -- $RS/data/<folder>
    readme_sha256 TEXT,
    adapter       TEXT,
    source_ids    TEXT,                          -- JSON list
    restricted    INTEGER DEFAULT 0,
    last_run      INTEGER,
    n_items       INTEGER,
    fetch_status  TEXT                           -- JSON: fetch/FETCH_STATUS.json + the count of fetch/verified.jsonl units, when present
);

-- ------------------------------------------------------------------------------------------------ views
-- Annotated CT and CBCT by modality, position and annotation kind
CREATE VIEW IF NOT EXISTS v_annotated_ct_by_modality_position AS
SELECT i.modality, i.position, a.kind AS annotation_kind,
       COUNT(DISTINCT i.item_id) AS n_items, COUNT(DISTINCT i.subject_key) AS n_subjects,
       COUNT(DISTINCT i.source_id) AS n_sources
FROM item i JOIN annotation a ON a.item_id = i.item_id
WHERE i.counted = 1 AND i.modality IN ('CT', 'CBCT') AND a.kind NOT IN ('none', 'unknown')
GROUP BY i.modality, i.position, a.kind;

-- Plain films without any annotation beyond 'none', by source and view
CREATE VIEW IF NOT EXISTS v_unannotated_films_by_view AS
SELECT i.source_id, i.view, COUNT(*) AS n_films, COUNT(DISTINCT i.subject_key) AS n_subjects
FROM item i
WHERE i.counted = 1 AND i.modality IN ('CR', 'DX')
  AND NOT EXISTS (SELECT 1 FROM annotation a WHERE a.item_id = i.item_id AND a.kind NOT IN ('none', 'unknown'))
GROUP BY i.source_id, i.view;

-- Everything held for one subject: SELECT * FROM v_subject_items WHERE subject_key = 'ctsp:0007';
CREATE VIEW IF NOT EXISTS v_subject_items AS
SELECT i.subject_key, i.source_id, i.item_id, i.modality, i.view, i.position, i.role, i.counted, i.path,
       (SELECT group_concat(DISTINCT a.kind) FROM annotation a WHERE a.item_id = i.item_id) AS annotation_kinds,
       (SELECT group_concat(s.experiment || '=' || s.part) FROM split s WHERE s.item_id = i.item_id) AS splits
FROM item i WHERE i.subject_key IS NOT NULL;

-- One row per source: items by modality and annotation coverage
CREATE VIEW IF NOT EXISTS v_source_summary AS
SELECT s.source_id, s.kind, s.status, s.restricted, s.annotation_status,
       COUNT(i.item_id) AS n_items, COUNT(DISTINCT i.subject_key) AS n_subjects,
       SUM(CASE WHEN EXISTS (SELECT 1 FROM annotation a WHERE a.item_id = i.item_id AND a.kind NOT IN ('none', 'unknown')) THEN 1 ELSE 0 END) AS n_annotated,
       group_concat(DISTINCT i.modality) AS modalities, SUM(i.bytes) AS bytes
FROM source s LEFT JOIN item i ON i.source_id = s.source_id AND i.counted = 1
GROUP BY s.source_id;

-- Subjects that occur in more than one source (the cross-naming leaks of docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md)
CREATE VIEW IF NOT EXISTS v_subjects_in_several_sources AS
SELECT subject_key, COUNT(DISTINCT source_id) AS n_sources, group_concat(DISTINCT source_id) AS sources
FROM item WHERE subject_key IS NOT NULL AND counted = 1 GROUP BY subject_key HAVING COUNT(DISTINCT source_id) > 1;
