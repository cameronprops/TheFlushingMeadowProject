-- FMP 005: Reconstruction census, source evidence, entrances/interiors and two material skins.
-- The archive is a candidate register. Classification does NOT assert a verified building.
CREATE TABLE IF NOT EXISTS reconstruction_subjects (
 subject_id TEXT PRIMARY KEY REFERENCES archive_inventory_candidates(inventory_id),
 display_name TEXT NOT NULL,
 candidate_category TEXT NOT NULL,
 year_candidates TEXT NOT NULL,
 subject_status TEXT NOT NULL DEFAULT 'UNREVIEWED',
 parent_building_id TEXT REFERENCES reconstruction_subjects(subject_id),
 notes TEXT
);
CREATE TABLE IF NOT EXISTS building_dossiers (
 building_id TEXT PRIMARY KEY REFERENCES reconstruction_subjects(subject_id),
 classification TEXT NOT NULL CHECK(classification IN
 ('ARCHITECTURE_LISTED','PAVILION_OR_EXHIBIT_UNRESOLVED','VENUE_UNRESOLVED','RELIGIOUS_SUBJECT_UNRESOLVED','CONCESSION_UNRESOLVED','CONFIRMED_BUILDING','NOT_A_SEPARATE_BUILDING')),
 zone TEXT,
 architecture_status TEXT NOT NULL DEFAULT 'CANDIDATE_NOT_CERTIFIED',
 site_position_status TEXT NOT NULL DEFAULT 'UNREGISTERED',
 footprint_status TEXT NOT NULL DEFAULT 'NOT_TRACED',
 baseline_model_status TEXT NOT NULL DEFAULT 'NOT_STARTED',
 public_access_status TEXT NOT NULL DEFAULT 'NOT_TESTED',
 realistic_skin_status TEXT NOT NULL DEFAULT 'NOT_STARTED',
 stylized_skin_status TEXT NOT NULL DEFAULT 'NOT_STARTED',
 production_priority TEXT NOT NULL DEFAULT 'P3',
 last_reviewed TEXT,
 notes TEXT
);
CREATE TABLE IF NOT EXISTS building_details (
 building_id TEXT PRIMARY KEY REFERENCES building_dossiers(building_id),
 architectural_attribution TEXT,
 architectural_form TEXT,
 known_dimensions TEXT,
 structural_materials TEXT,
 facade_roof TEXT,
 site_orientation TEXT,
 documented_interiors TEXT,
 interaction_points TEXT,
 exact_dimensions_status TEXT NOT NULL DEFAULT 'UNVERIFIED',
 year_variant_notes TEXT,
 workflow_notes TEXT,
 details_status TEXT NOT NULL DEFAULT 'RESEARCH_PENDING'
);
CREATE TABLE IF NOT EXISTS building_evidence (
 evidence_id TEXT PRIMARY KEY,
 building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
 year INTEGER CHECK(year IN (1939,1940,1964,1965,2026)),
 document_title TEXT NOT NULL,
 repository TEXT NOT NULL,
 document_url TEXT,
 archive_locator TEXT,
 document_type TEXT NOT NULL,
 evidence_scope TEXT NOT NULL,
 claim_or_research_value TEXT NOT NULL,
 evidence_status TEXT NOT NULL CHECK(evidence_status IN
 ('CATALOG_LEAD','VIEWED_CATALOG','PERIOD_PHOTO','CONTEMPORARY_DOCUMENT','DRAWINGS_CATALOGED','SOURCE_ACQUIRED','TRACED_VERIFIED','HYPOTHESIS')),
 rights_status TEXT NOT NULL DEFAULT 'REVIEW_REQUIRED',
 local_or_drive_uri TEXT,
 sha256 TEXT,
 revision_date TEXT,
 reviewer_note TEXT
);
CREATE TABLE IF NOT EXISTS building_spaces (
 space_id TEXT PRIMARY KEY,
 building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
 year INTEGER NOT NULL CHECK(year IN (1939,1940,1964,1965,2026)),
 space_name TEXT NOT NULL,
 space_type TEXT NOT NULL,
 access_intent TEXT NOT NULL CHECK(access_intent IN ('PUBLIC','RESTRICTED','UNKNOWN')),
 evidence_status TEXT NOT NULL,
 floor_level TEXT,
 plan_reference TEXT,
 entrance_geometry_status TEXT NOT NULL DEFAULT 'NOT_LOCATED',
 interior_model_status TEXT NOT NULL DEFAULT 'NOT_STARTED',
 collision_status TEXT NOT NULL DEFAULT 'NOT_TESTED',
 navigation_status TEXT NOT NULL DEFAULT 'NOT_TESTED',
 notes TEXT
);
CREATE TABLE IF NOT EXISTS building_appearance (
 building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
 variant TEXT NOT NULL CHECK(variant IN ('REALISTIC','STYLIZED')),
 status TEXT NOT NULL DEFAULT 'NOT_STARTED',
 shared_geometry_contract TEXT NOT NULL DEFAULT 'SAME_FOOTPRINT_DOORS_COLLISION',
 material_package TEXT,
 notes TEXT,
 PRIMARY KEY(building_id,variant)
);
CREATE TABLE IF NOT EXISTS building_worklog (
 log_id TEXT PRIMARY KEY,
 building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
 period_year INTEGER,
 build_stage TEXT NOT NULL,
 status TEXT NOT NULL,
 asset_uri TEXT,
 test_evidence_uri TEXT,
 notes TEXT,
 changed_utc TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_building_evidence_id ON building_evidence(building_id);
CREATE INDEX IF NOT EXISTS ix_building_rooms_id ON building_spaces(building_id,year);
CREATE INDEX IF NOT EXISTS ix_building_status ON building_dossiers(classification,production_priority);

-- Archive rows are imported after CREATEs. Trigger creates stable one-to-one
-- subject records for EVERY archived candidate, and building records only
-- for plausible physical building subjects. No year is marked verified.
CREATE TRIGGER IF NOT EXISTS trg_fmp_subject_from_archive
AFTER INSERT ON archive_inventory_candidates
BEGIN
 INSERT INTO reconstruction_subjects(subject_id,display_name,candidate_category,year_candidates,subject_status,notes)
 VALUES (NEW.inventory_id,NEW.label,NEW.category,NEW.year_candidates,'CLASSIFICATION_PENDING',NEW.notes);
 INSERT INTO building_dossiers(building_id,classification,zone,notes)
 SELECT NEW.inventory_id,
  CASE NEW.category
   WHEN 'architecture' THEN 'ARCHITECTURE_LISTED'
   WHEN 'pavilion_or_exhibition_subject' THEN 'PAVILION_OR_EXHIBIT_UNRESOLVED'
   WHEN 'attraction_or_venue' THEN 'VENUE_UNRESOLVED'
   WHEN 'religious_pavilion_or_program' THEN 'RELIGIOUS_SUBJECT_UNRESOLVED'
   WHEN 'food_or_concession' THEN 'CONCESSION_UNRESOLVED'
  END, NEW.zone, NEW.notes
 WHERE NEW.category IN ('architecture','pavilion_or_exhibition_subject','attraction_or_venue','religious_pavilion_or_program','food_or_concession');
END;
CREATE TRIGGER IF NOT EXISTS trg_fmp_building_skin_rows
AFTER INSERT ON building_dossiers
BEGIN
 INSERT INTO building_appearance(building_id,variant) VALUES (NEW.building_id,'REALISTIC');
 INSERT INTO building_appearance(building_id,variant) VALUES (NEW.building_id,'STYLIZED');
END;
CREATE VIEW IF NOT EXISTS building_production_view AS
SELECT b.building_id, r.display_name, r.year_candidates, b.classification,
 b.zone,b.production_priority,b.site_position_status,b.footprint_status,
 b.baseline_model_status,b.public_access_status,b.realistic_skin_status,
 b.stylized_skin_status,COUNT(DISTINCT e.evidence_id) AS evidence_count,
 COUNT(DISTINCT s.space_id) AS space_count
FROM building_dossiers b
JOIN reconstruction_subjects r ON r.subject_id=b.building_id
LEFT JOIN building_evidence e ON e.building_id=b.building_id
LEFT JOIN building_spaces s ON s.building_id=b.building_id
GROUP BY b.building_id;
