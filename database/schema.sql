PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS eras (
  year INTEGER PRIMARY KEY CHECK (year IN (1939,1940,1964,1965,2026)),
  label TEXT NOT NULL,
  scene_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS places (
  place_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  zone TEXT NOT NULL,
  year_scope TEXT NOT NULL,
  identity_status TEXT NOT NULL,
  geometry_status TEXT NOT NULL,
  site_registration TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS sources (
  source_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  repository TEXT,
  url TEXT,
  source_type TEXT,
  access_status TEXT NOT NULL,
  rights_status TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS evidence_claims (
  claim_id TEXT PRIMARY KEY,
  place_id TEXT REFERENCES places(place_id),
  source_id TEXT REFERENCES sources(source_id),
  claim_type TEXT NOT NULL,
  property TEXT NOT NULL,
  value_text TEXT,
  numeric_value REAL,
  units TEXT,
  year INTEGER REFERENCES eras(year),
  evidence_class TEXT NOT NULL CHECK(evidence_class IN
    ('DOCUMENTED_BUILT','DOCUMENTED_PROPOSED','PHOTO_INFERRED','REGISTERED_CONTEXT',
     'UNREGISTERED_CONTEXT','INTERPRETIVE','UNKNOWN')),
  uncertainty TEXT,
  verification_status TEXT NOT NULL DEFAULT 'PENDING',
  notes TEXT
);

CREATE TABLE IF NOT EXISTS surveys (
  survey_id TEXT PRIMARY KEY,
  source_id TEXT REFERENCES sources(source_id),
  date_surveyed TEXT,
  date_published TEXT,
  horizontal_crs TEXT,
  vertical_datum TEXT,
  geoid_model TEXT,
  resolution REAL,
  units TEXT,
  error_estimate TEXT,
  acquisition_status TEXT NOT NULL DEFAULT 'CATALOG_LEAD',
  archive_uri TEXT,
  sha256 TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS control_points (
  control_id TEXT PRIMARY KEY,
  survey_id TEXT REFERENCES surveys(survey_id),
  x REAL, y REAL, z REAL,
  units TEXT,
  horizontal_crs TEXT,
  vertical_datum TEXT,
  source_id TEXT REFERENCES sources(source_id),
  uncertainty TEXT,
  verified INTEGER NOT NULL DEFAULT 0 CHECK (verified IN (0,1))
);

CREATE TABLE IF NOT EXISTS era_presence (
  place_id TEXT NOT NULL REFERENCES places(place_id),
  year INTEGER NOT NULL REFERENCES eras(year),
  state TEXT NOT NULL CHECK(state IN ('PRESENT','ABSENT','ALTERED','UNKNOWN')),
  source_id TEXT REFERENCES sources(source_id),
  notes TEXT,
  PRIMARY KEY(place_id,year)
);

CREATE TABLE IF NOT EXISTS archive_assets (
  asset_id TEXT PRIMARY KEY,
  source_id TEXT REFERENCES sources(source_id),
  title TEXT NOT NULL,
  original_uri TEXT,
  drive_uri TEXT,
  sha256 TEXT,
  media_type TEXT,
  access_status TEXT NOT NULL,
  rights_status TEXT NOT NULL,
  acquired_utc TEXT,
  source_date TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS transit_links (
  link_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  transport_type TEXT NOT NULL,
  year INTEGER REFERENCES eras(year),
  source_id TEXT REFERENCES sources(source_id),
  alignment_status TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS geometry_assets (
  geometry_id TEXT PRIMARY KEY,
  place_id TEXT REFERENCES places(place_id),
  year INTEGER REFERENCES eras(year),
  repository_path TEXT,
  archive_uri TEXT,
  model_version TEXT,
  geometry_status TEXT NOT NULL,
  source_registration TEXT,
  qa_status TEXT DEFAULT 'UNTESTED',
  notes TEXT
);

CREATE TABLE IF NOT EXISTS releases (
  release_id TEXT PRIMARY KEY,
  component TEXT NOT NULL,
  version TEXT NOT NULL,
  drive_url TEXT,
  status TEXT NOT NULL,
  notes TEXT
);

CREATE INDEX IF NOT EXISTS ix_claim_place ON evidence_claims(place_id);
CREATE INDEX IF NOT EXISTS ix_claim_source ON evidence_claims(source_id);
CREATE INDEX IF NOT EXISTS ix_era_presence_year ON era_presence(year);
CREATE INDEX IF NOT EXISTS ix_geometry_year ON geometry_assets(year);
