-- FMP 016 / Small things make a living fair: dated furniture, fixtures, facilities, art.
-- Source claims are not georegistered sites; 1964 cannot be copied into 1939.
CREATE TABLE IF NOT EXISTS site_amenity_categories (
 category_id TEXT PRIMARY KEY,
 category_family TEXT NOT NULL CHECK(category_family IN (
  'CLEANLINESS','SEATING','DRINKING_WATER','LIGHTING','WAYFINDING',
  'PUBLIC_SERVICE','CIVIC_ART','WATER_FEATURE','LANDSCAPE_FIXTURE',
  'OPERATIONS','SECURITY','OTHER')),
 display_name TEXT NOT NULL,
 suggested_layer TEXT NOT NULL,
 visible_in_unreal INTEGER NOT NULL DEFAULT 1 CHECK(visible_in_unreal IN(0,1)),
 note TEXT
);
CREATE TABLE IF NOT EXISTS site_amenity_types (
 type_id TEXT PRIMARY KEY,
 category_id TEXT NOT NULL REFERENCES site_amenity_categories(category_id),
 era_year INTEGER NOT NULL CHECK(era_year IN(1939,1940,1964,1965,2026)),
 historical_label TEXT NOT NULL,
 type_status TEXT NOT NULL CHECK(type_status IN
  ('HISTORICALLY_DOCUMENTED','DESIGN_REFERENCE_ONLY','ARCHIVE_LEAD','UNCERTAIN')),
 period_quantity INTEGER CHECK(period_quantity IS NULL OR period_quantity >= 0),
 measured_height_m REAL CHECK(measured_height_m IS NULL OR measured_height_m>0),
 measured_width_m REAL CHECK(measured_width_m IS NULL OR measured_width_m>0),
 measured_depth_m REAL CHECK(measured_depth_m IS NULL OR measured_depth_m>0),
 material_note TEXT,
 source_sheet_id TEXT REFERENCES site_network_sheets(sheet_id),
 linked_model_uri TEXT,
 evidence_note TEXT
);
CREATE INDEX IF NOT EXISTS ix_site_amenity_type_category
 ON site_amenity_types(era_year,category_id);

CREATE TABLE IF NOT EXISTS site_amenity_evidence (
 observation_id TEXT PRIMARY KEY,
 type_id TEXT NOT NULL REFERENCES site_amenity_types(type_id),
 era_year INTEGER NOT NULL CHECK(era_year IN(1939,1940,1964,1965,2026)),
 source_sheet_id TEXT REFERENCES site_network_sheets(sheet_id),
 source_url TEXT NOT NULL,
 source_locator TEXT,
 observation_kind TEXT NOT NULL CHECK(observation_kind IN
  ('LOCATIONS_SHEET','PHOTO','COLLECTION_FINDING_AID','PERIOD_GUIDE',
   'INSTITUTIONAL_RESEARCH','ART_PLAN','OTHER')),
 observation_status TEXT NOT NULL CHECK(observation_status IN
  ('CATALOGED_UNREAD','SOURCE_VIEWED','SOURCE_ACQUIRED','GEOREGISTERED','TRACED')),
 claim TEXT NOT NULL,
 approximate_named_context TEXT,
 observed_quantity INTEGER CHECK(observed_quantity IS NULL OR observed_quantity>=0),
 rights_status TEXT NOT NULL DEFAULT 'REVIEW_REQUIRED',
 notes TEXT
);
CREATE INDEX IF NOT EXISTS ix_site_amenity_observation ON site_amenity_evidence(type_id,era_year);

-- A type is one recurring design family. An instance is one actual item.
-- Do NOT create one row per supposed bench/bin unless a sheet or photo supports it.
CREATE TABLE IF NOT EXISTS site_amenity_instances (
 instance_id TEXT PRIMARY KEY,
 type_id TEXT NOT NULL REFERENCES site_amenity_types(type_id),
 era_year INTEGER NOT NULL CHECK(era_year IN(1939,1940,1964,1965,2026)),
 location_label TEXT,
 nearby_building_id TEXT REFERENCES building_dossiers(building_id),
 nearby_route_segment_id TEXT REFERENCES site_network_segments(segment_id),
 source_observation_id TEXT REFERENCES site_amenity_evidence(observation_id),
 position_status TEXT NOT NULL CHECK(position_status IN
  ('UNLOCATED','NAMED_AREA_ONLY','PHOTO_ESTIMATE','MAP_TRACED','SITE_REGISTERED')),
 coordinate_frame TEXT NOT NULL DEFAULT 'UNREGISTERED',
 x_m REAL,y_m REAL,z_m REAL,
 longitude REAL,latitude REAL,
 horizontal_crs TEXT,vertical_datum TEXT,
 yaw_deg REAL,
 placement_uncertainty_m REAL CHECK(placement_uncertainty_m IS NULL OR placement_uncertainty_m>=0),
 historical_visibility TEXT NOT NULL DEFAULT 'UNVERIFIED' CHECK(historical_visibility IN
  ('DOCUMENTED_INSTALLED','DOCUMENTED_PROPOSED','INFERRED','UNVERIFIED')),
 model_asset_uri TEXT,
 unreal_scene_object_id TEXT,
 print_component_id TEXT,
 notes TEXT,
 CHECK((x_m IS NULL AND y_m IS NULL AND z_m IS NULL) OR
       (x_m IS NOT NULL AND y_m IS NOT NULL AND z_m IS NOT NULL)),
 CHECK((longitude IS NULL AND latitude IS NULL) OR
       (longitude IS NOT NULL AND latitude IS NOT NULL
        AND longitude BETWEEN -180 AND 180 AND latitude BETWEEN -90 AND 90)),
 CHECK(position_status NOT IN ('MAP_TRACED','SITE_REGISTERED') OR
       (x_m IS NOT NULL AND source_observation_id IS NOT NULL)),
 CHECK(position_status!='SITE_REGISTERED' OR
       (horizontal_crs IS NOT NULL AND vertical_datum IS NOT NULL)),
 CHECK(position_status!='UNLOCATED' OR
       (x_m IS NULL AND longitude IS NULL))
);
CREATE INDEX IF NOT EXISTS ix_site_amenity_location ON site_amenity_instances(era_year,position_status,type_id);

CREATE TABLE IF NOT EXISTS site_amenity_service_links (
 service_link_id TEXT PRIMARY KEY,
 instance_id TEXT NOT NULL REFERENCES site_amenity_instances(instance_id),
 network_layer_id TEXT NOT NULL REFERENCES site_network_layers(layer_id),
 segment_id TEXT REFERENCES site_network_segments(segment_id),
 service_kind TEXT NOT NULL,
 linkage_status TEXT NOT NULL CHECK(linkage_status IN
  ('REQUIRED_IN_PRINCIPLE','HYPOTHESIS','DOCUMENTED','GEOREGISTERED')),
 source_observation_id TEXT REFERENCES site_amenity_evidence(observation_id),
 notes TEXT
);
CREATE TABLE IF NOT EXISTS site_amenity_era_relations (
 relation_id TEXT PRIMARY KEY,
 earlier_instance_id TEXT NOT NULL REFERENCES site_amenity_instances(instance_id),
 later_instance_id TEXT NOT NULL REFERENCES site_amenity_instances(instance_id),
 relation_type TEXT NOT NULL CHECK(relation_type IN
  ('SAME_PHYSICAL_OBJECT','MOVED','REPLACED','SAME_TYPE_ONLY','POSSIBLE_RELATION')),
 evidence_observation_id TEXT REFERENCES site_amenity_evidence(observation_id),
 certainty TEXT NOT NULL CHECK(certainty IN('VERIFIED','LIKELY','UNVERIFIED')),
 notes TEXT,
 CHECK(earlier_instance_id!=later_instance_id)
);
CREATE VIEW IF NOT EXISTS site_amenity_research_queue AS
SELECT t.type_id,t.era_year,t.historical_label,c.category_family,
 t.type_status,t.source_sheet_id,
 (SELECT COUNT(*) FROM site_amenity_evidence e WHERE e.type_id=t.type_id) AS evidence_records,
 (SELECT COUNT(*) FROM site_amenity_instances a WHERE a.type_id=t.type_id) AS located_or_unlocated_instances,
 (SELECT COUNT(*) FROM site_amenity_instances a WHERE a.type_id=t.type_id
 AND a.position_status IN ('MAP_TRACED','SITE_REGISTERED')) AS spatially_traced_instances
FROM site_amenity_types t JOIN site_amenity_categories c ON c.category_id=t.category_id;
-- Safe geometry feed: verified spatial claims only. No fabricated distributions.
CREATE VIEW IF NOT EXISTS site_amenity_map_points AS
SELECT a.instance_id,a.era_year,t.historical_label,t.category_id,c.category_family,
 a.x_m,a.y_m,a.z_m,a.coordinate_frame,a.position_status,
 a.location_label,a.source_observation_id,a.placement_uncertainty_m,
 a.model_asset_uri
FROM site_amenity_instances a
JOIN site_amenity_types t ON t.type_id=a.type_id
JOIN site_amenity_categories c ON c.category_id=t.category_id
WHERE a.position_status IN ('MAP_TRACED','SITE_REGISTERED')
AND a.x_m IS NOT NULL AND a.source_observation_id IS NOT NULL;

-- Reject impossible time transfers or deceptively certain imported locations.
CREATE TRIGGER IF NOT EXISTS trg_amenity_type_source_era
BEFORE INSERT ON site_amenity_types
WHEN NEW.source_sheet_id IS NOT NULL
 AND (SELECT era_year FROM site_network_sheets WHERE sheet_id=NEW.source_sheet_id)!=NEW.era_year
BEGIN SELECT RAISE(ABORT,'Amenity type and source sheet years disagree'); END;
CREATE TRIGGER IF NOT EXISTS trg_amenity_evidence_era
BEFORE INSERT ON site_amenity_evidence
WHEN (SELECT era_year FROM site_amenity_types WHERE type_id=NEW.type_id)!=NEW.era_year
 OR (NEW.source_sheet_id IS NOT NULL AND
 (SELECT era_year FROM site_network_sheets WHERE sheet_id=NEW.source_sheet_id)!=NEW.era_year)
BEGIN SELECT RAISE(ABORT,'Amenity evidence year does not match type and source'); END;
CREATE TRIGGER IF NOT EXISTS trg_amenity_instance_era
BEFORE INSERT ON site_amenity_instances
WHEN (SELECT era_year FROM site_amenity_types WHERE type_id=NEW.type_id)!=NEW.era_year
 OR (NEW.source_observation_id IS NOT NULL AND NOT EXISTS(
 SELECT 1 FROM site_amenity_evidence e WHERE e.observation_id=NEW.source_observation_id
 AND e.type_id=NEW.type_id AND e.era_year=NEW.era_year))
 OR (NEW.longitude IS NOT NULL AND NEW.position_status!='SITE_REGISTERED')
BEGIN SELECT RAISE(ABORT,'Amenity instance type, evidence, era, or geodetic status mismatch'); END;
CREATE TRIGGER IF NOT EXISTS trg_amenity_service_certification
BEFORE INSERT ON site_amenity_service_links
WHEN (NEW.linkage_status='DOCUMENTED' AND NEW.source_observation_id IS NULL)
 OR (NEW.linkage_status='GEOREGISTERED' AND
     (NEW.segment_id IS NULL OR NEW.source_observation_id IS NULL))
BEGIN SELECT RAISE(ABORT,'Service connection cannot be certified without documents'); END;
CREATE TRIGGER IF NOT EXISTS trg_amenity_era_relation
BEFORE INSERT ON site_amenity_era_relations
WHEN (SELECT era_year FROM site_amenity_instances WHERE instance_id=NEW.earlier_instance_id)
  >= (SELECT era_year FROM site_amenity_instances WHERE instance_id=NEW.later_instance_id)
 OR (NEW.certainty='VERIFIED' AND NEW.evidence_observation_id IS NULL)
 OR (NEW.relation_type='SAME_PHYSICAL_OBJECT' AND NEW.certainty!='VERIFIED')
BEGIN SELECT RAISE(ABORT,'Chronology/evidence of reused street furnishing not established'); END;
