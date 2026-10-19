-- FMP 007. Procedural reconstruction facts, multi-view estimates and surface research.
-- Append-only physical evidence; content never implies historical certification.
CREATE TABLE IF NOT EXISTS building_geometry_parameters (
  parameter_id TEXT PRIMARY KEY,
  building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
  period_year INTEGER NOT NULL CHECK(period_year IN (1939,1940,1964,1965,2026)),
  component_id TEXT NOT NULL,
  parameter_key TEXT NOT NULL,
  value_si REAL,
  units_si TEXT,
  period_source_value TEXT,
  source_evidence_id TEXT REFERENCES building_evidence(evidence_id),
  evidence_class TEXT NOT NULL CHECK(evidence_class IN
    ('DOCUMENTED_BUILT','DOCUMENTED_PROPOSED','PERIOD_PRINTED',
     'PHOTO_INFERRED','INTERPRETIVE','UNKNOWN')),
  tolerance_si REAL,
  adjustment_status TEXT NOT NULL DEFAULT 'EDITABLE',
  notes TEXT,
  UNIQUE(building_id,period_year,component_id,parameter_key)
);
CREATE TABLE IF NOT EXISTS building_surface_research (
  surface_id TEXT PRIMARY KEY,
  building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
  period_year INTEGER NOT NULL CHECK(period_year IN (1939,1940,1964,1965,2026)),
  component_selector TEXT NOT NULL,
  material_family TEXT NOT NULL,
  finish_description TEXT,
  substrate TEXT,
  glass_transmission TEXT,
  measured_color TEXT,
  metallic REAL CHECK(metallic IS NULL OR metallic BETWEEN 0 AND 1),
  roughness REAL CHECK(roughness IS NULL OR roughness BETWEEN 0 AND 1),
  texture_asset_uri TEXT,
  evidence_id TEXT REFERENCES building_evidence(evidence_id),
  certainty TEXT NOT NULL CHECK(certainty IN
    ('PERIOD_DOCUMENTED','PHOTO_ESTIMATED','PROVISIONAL','UNRESEARCHED')),
  skin_policy TEXT NOT NULL DEFAULT 'REALISTIC_AND_STYLIZED_SHARE_GEOMETRY',
  notes TEXT
);
CREATE TABLE IF NOT EXISTS building_view_observations (
  view_id TEXT PRIMARY KEY,
  building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
  period_year INTEGER NOT NULL CHECK(period_year IN (1939,1940,1964,1965,2026)),
  evidence_id TEXT REFERENCES building_evidence(evidence_id),
  image_uri TEXT,
  view_direction TEXT,
  lens_perspective TEXT,
  visible_components TEXT,
  fixed_points TEXT,
  estimated_dimensions TEXT,
  mesh_reference_uri TEXT,
  geometry_use TEXT NOT NULL DEFAULT 'REFERENCE_ONLY',
  confidence TEXT NOT NULL DEFAULT 'UNASSESSED',
  notes TEXT
);
CREATE TABLE IF NOT EXISTS unidentified_visual_leads (
  lead_id TEXT PRIMARY KEY,
  working_description TEXT NOT NULL,
  requested_by TEXT NOT NULL DEFAULT 'project_owner',
  status TEXT NOT NULL CHECK(status IN ('UNIDENTIFIED','HYPOTHESIS','MATCH_CONFIRMED','REJECTED')),
  candidate_building_id TEXT REFERENCES building_dossiers(building_id),
  reference_url TEXT,
  feature_motion TEXT,
  notes TEXT
);
CREATE INDEX IF NOT EXISTS ix_fmp_build_params ON building_geometry_parameters(building_id,period_year);
CREATE INDEX IF NOT EXISTS ix_fmp_surfaces ON building_surface_research(building_id,period_year);
CREATE INDEX IF NOT EXISTS ix_fmp_views ON building_view_observations(building_id,period_year);
