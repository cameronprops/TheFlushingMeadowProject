-- FMP 012 / One Database to Rule Them All.
-- Canonical CSV/research datasets -> reproducible SQLite index.
-- Distinguishes model-space BBOX estimates from measured historical envelopes.
-- Run BEFORE importing catalog/master_*.csv in tools/build_db.py.

CREATE TABLE IF NOT EXISTS master_building_envelopes (
  envelope_id TEXT PRIMARY KEY,
  building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
  period_year INTEGER NOT NULL CHECK(period_year IN (1939,1940,1964,1965,2026)),
  envelope_scope TEXT NOT NULL,
  coordinate_frame TEXT NOT NULL,
  min_x_m REAL, min_y_m REAL, min_z_m REAL,
  max_x_m REAL, max_y_m REAL, max_z_m REAL,
  source_geometry_node TEXT,
  source_asset_id TEXT,
  evidence_status TEXT NOT NULL CHECK(evidence_status IN
    ('SOURCE_MODEL_MEASURED','PERIOD_PLAN_TRACED','PHOTO_ESTIMATED','DESIGN_PREVIEW','NOT_MEASURED')),
  uncertainty_m REAL,
  site_registered INTEGER NOT NULL DEFAULT 0 CHECK(site_registered IN (0,1)),
  notes TEXT,
  CHECK (
    ((min_x_m IS NULL AND min_y_m IS NULL AND min_z_m IS NULL AND
      max_x_m IS NULL AND max_y_m IS NULL AND max_z_m IS NULL))
    OR
    (min_x_m<=max_x_m AND min_y_m<=max_y_m AND min_z_m<=max_z_m))
);
CREATE INDEX IF NOT EXISTS ix_master_envelope ON master_building_envelopes(building_id,period_year);

CREATE TABLE IF NOT EXISTS master_interactive_points (
  point_id TEXT PRIMARY KEY,
  building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
  period_year INTEGER NOT NULL CHECK(period_year IN (1939,1940,1964,1965,2026)),
  space_id TEXT REFERENCES building_spaces(space_id),
  label TEXT NOT NULL,
  interaction_type TEXT NOT NULL,
  public_access TEXT NOT NULL,
  coordinate_frame TEXT NOT NULL,
  x_m REAL, y_m REAL, z_m REAL,
  position_status TEXT NOT NULL CHECK(position_status IN
    ('UNLOCATED','INTERPRETIVE','MODEL_LOCAL','REGISTERED')),
  requested_behavior TEXT,
  trigger_or_scene_key TEXT,
  implementation_status TEXT NOT NULL DEFAULT 'NOT_BUILT',
  native_unreal_tested INTEGER NOT NULL DEFAULT 0 CHECK(native_unreal_tested IN(0,1)),
  notes TEXT,
  CHECK ((x_m IS NULL AND y_m IS NULL AND z_m IS NULL)
         OR (x_m IS NOT NULL AND y_m IS NOT NULL AND z_m IS NOT NULL)),
  CHECK(position_status!='REGISTERED' OR x_m IS NOT NULL)
);
CREATE INDEX IF NOT EXISTS ix_master_interactions ON master_interactive_points(building_id,period_year);

CREATE TABLE IF NOT EXISTS master_media_assets (
  media_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  kind TEXT NOT NULL,
  period_year INTEGER CHECK(period_year IS NULL OR period_year IN (1939,1940,1964,1965,2026)),
  uri TEXT,
  repo_path TEXT,
  mime_type TEXT,
  sha256 TEXT,
  rights_status TEXT NOT NULL,
  acquisition_status TEXT NOT NULL,
  notes TEXT
);
CREATE TABLE IF NOT EXISTS master_building_media (
  link_id TEXT PRIMARY KEY,
  building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
  media_id TEXT NOT NULL REFERENCES master_media_assets(media_id),
  period_year INTEGER CHECK(period_year IS NULL OR period_year IN (1939,1940,1964,1965,2026)),
  role TEXT NOT NULL,
  component_id TEXT,
  notes TEXT
);
CREATE INDEX IF NOT EXISTS ix_master_media_links ON master_building_media(building_id,role);
CREATE INDEX IF NOT EXISTS ix_master_media_asset ON master_building_media(media_id);

-- Existing building evidence, model components, and explicitly registered
-- project files become one media inventory without duplicating source data.
-- ARCHIVE_REFERENCE is *not* proof a photo/plan is downloaded or rights-cleared.
CREATE VIEW IF NOT EXISTS master_all_media AS
SELECT 'EVIDENCE:'||e.evidence_id AS media_ref, e.building_id,
       e.year AS period_year, 'ARCHIVE_REFERENCE' AS record_type,
       e.document_title AS title, e.document_type AS media_kind,
       e.document_url AS uri, e.local_or_drive_uri AS project_uri,
       e.sha256 AS sha256, e.rights_status,
       e.evidence_status AS acquisition_status,
       e.evidence_scope AS role
FROM building_evidence e
UNION ALL
SELECT 'FILE:'||m.link_id, m.building_id, m.period_year,
       'REGISTERED_FILE', a.title, a.kind, a.uri, a.repo_path,
       a.sha256, a.rights_status, a.acquisition_status, m.role
FROM master_building_media m JOIN master_media_assets a ON m.media_id=a.media_id
UNION ALL
SELECT 'SHELL:'||s.part_id, s.building_id, s.period_year,
       'SOURCE_GEOMETRY_PART', s.exact_source_node, s.role,
       s.source_model_uri, NULL, s.source_sha256,
       'PROJECT_SOURCE_RIGHTS_TO_REVIEW', s.construction_status, s.role
FROM building_shell_parts s
UNION ALL
SELECT 'PHOTO_VIEW:'||v.view_id,v.building_id,v.period_year,
       'IMAGE_OBSERVATION',v.view_id,'PHOTOGRAPH',v.image_uri,
       v.mesh_reference_uri,NULL,'SEE_EVIDENCE_RECORD',v.confidence,'PHOTOMATCH_REFERENCE'
FROM building_view_observations v;

CREATE VIEW IF NOT EXISTS master_building_overview AS
SELECT d.building_id, s.display_name, s.year_candidates, s.candidate_category,
       d.classification, d.zone, d.production_priority,
       d.site_position_status, d.footprint_status,
       d.baseline_model_status, d.public_access_status,
       d.realistic_skin_status, d.stylized_skin_status,
       COALESCE((SELECT COUNT(*) FROM building_geometry_parameters p WHERE p.building_id=d.building_id),0) AS dimension_count,
       COALESCE((SELECT COUNT(*) FROM master_building_envelopes x WHERE x.building_id=d.building_id),0) AS envelope_count,
       COALESCE((SELECT COUNT(*) FROM master_interactive_points i WHERE i.building_id=d.building_id),0) AS interaction_count,
       COALESCE((SELECT COUNT(*) FROM building_spaces r WHERE r.building_id=d.building_id),0) AS room_count,
       COALESCE((SELECT COUNT(*) FROM master_all_media m WHERE m.building_id=d.building_id),0) AS media_count,
       COALESCE((SELECT COUNT(*) FROM building_evidence e WHERE e.building_id=d.building_id),0) AS historical_reference_count,
       COALESCE((SELECT COUNT(*) FROM building_shell_parts p WHERE p.building_id=d.building_id AND p.role='EXTERIOR_SHELL'),0) AS exterior_shell_count,
       'NOT_NATIVE_ENGINE_CERTIFIED' AS release_certification
FROM building_dossiers d JOIN reconstruction_subjects s ON d.building_id=s.subject_id;
