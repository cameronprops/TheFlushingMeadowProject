-- FMP 017 | Plants, gardens, trees, lawns, beds and horticultural change over time.
-- Source plans and botanical accounts do NOT become site-registered geometry automatically.
-- This is ONE extension of the existing master SQLite database.

CREATE TABLE IF NOT EXISTS horticulture_sources (
 source_id TEXT PRIMARY KEY,
 era_year INTEGER NOT NULL CHECK(era_year IN (1939,1940,1964,1965,2026)),
 title TEXT NOT NULL,
 repository TEXT NOT NULL,
 source_url TEXT NOT NULL,
 archive_locator TEXT,
 document_date TEXT,
 source_class TEXT NOT NULL CHECK(source_class IN
  ('ORIGINAL_PLANTING_PLAN','ARCHIVAL_SPECIFICATION','ORIGINAL_RECORD_FINDING_AID',
   'PERIOD_PUBLICATION','HISTORICAL_RESEARCH','HISTORIC_SITE_MAP',
   'INSTITUTIONAL_ARCHIVE','SURVEY_MAP')),
 access_status TEXT NOT NULL CHECK(access_status IN
  ('CATALOG_ONLY','AVAILABLE_TEXT','IMAGES_AVAILABLE','SOURCE_ACQUIRED',
   'TRACED_TO_PLAN','SITE_REGISTERED')),
 historical_status TEXT NOT NULL CHECK(historical_status IN
  ('PROPOSAL','AS_BUILT_REFERENCE','PLANTING_CONTRACT','SUBJECT_FILE','LATER_RESEARCH','UNKNOWN')),
 rights_status TEXT NOT NULL DEFAULT 'REVIEW_REQUIRED',
 notes TEXT
);
CREATE TABLE IF NOT EXISTS horticulture_taxa (
 taxon_id TEXT PRIMARY KEY,
 display_name TEXT NOT NULL,
 scientific_name TEXT,
 taxonomic_precision TEXT NOT NULL CHECK(taxonomic_precision IN
  ('SPECIES','GENUS','COMMON_GROUP','CULTIVAR','UNKNOWN')),
 growth_form TEXT NOT NULL CHECK(growth_form IN
  ('TREE','SHRUB','ROSE','ANNUAL','PERENNIAL','BULB','GROUNDCOVER',
   'TURF','VINE','AQUATIC','MIXED','UNKNOWN')),
 notes TEXT
);
CREATE TABLE IF NOT EXISTS horticulture_areas (
 area_id TEXT PRIMARY KEY,
 era_year INTEGER NOT NULL CHECK(era_year IN (1939,1940,1964,1965,2026)),
 historical_name TEXT NOT NULL,
 area_kind TEXT NOT NULL CHECK(area_kind IN
  ('HORTICULTURE_EXHIBIT','NAMED_GARDEN','GARDEN_BED','ROSE_DISPLAY',
   'WOODLAND','FORMAL_LAWN','STREET_TREE_CORRIDOR','PAVILION_LANDSCAPE',
   'GENERAL_FAIRGROUND','GREENHOUSE','BORDER','OTHER')),
 parent_area_id TEXT REFERENCES horticulture_areas(area_id),
 associated_building_id TEXT REFERENCES building_dossiers(building_id),
 associated_route_segment_id TEXT REFERENCES site_network_segments(segment_id),
 source_id TEXT NOT NULL REFERENCES horticulture_sources(source_id),
 named_context TEXT,
 approximate_area_m2 REAL CHECK(approximate_area_m2 IS NULL OR approximate_area_m2>0),
 area_measurement_status TEXT NOT NULL CHECK(area_measurement_status IN
   ('PERIOD_PUBLISHED','PLAN_MEASURED','ESTIMATED','NOT_MEASURED')),
 location_status TEXT NOT NULL CHECK(location_status IN
   ('UNLOCATED','NAMED_AREA_ONLY','PHOTO_ESTIMATE','MAP_TRACED','SITE_REGISTERED')),
 local_polygon_geojson TEXT,
 coordinate_frame TEXT NOT NULL DEFAULT 'UNREGISTERED',
 horizontal_crs TEXT,
 vertical_datum TEXT,
 notes TEXT,
 CHECK(location_status NOT IN ('MAP_TRACED','SITE_REGISTERED') OR local_polygon_geojson IS NOT NULL),
 CHECK(location_status!='SITE_REGISTERED' OR
       (horizontal_crs IS NOT NULL AND vertical_datum IS NOT NULL))
);
CREATE INDEX IF NOT EXISTS ix_horticulture_areas_era ON horticulture_areas(era_year,location_status);
CREATE TABLE IF NOT EXISTS horticulture_plantings (
 planting_id TEXT PRIMARY KEY,
 era_year INTEGER NOT NULL CHECK(era_year IN (1939,1940,1964,1965,2026)),
 area_id TEXT NOT NULL REFERENCES horticulture_areas(area_id),
 taxon_id TEXT REFERENCES horticulture_taxa(taxon_id),
 source_id TEXT NOT NULL REFERENCES horticulture_sources(source_id),
 display_label TEXT NOT NULL,
 planting_role TEXT NOT NULL CHECK(planting_role IN
  ('CANOPY','UNDERSTORY','HEDGE','SHRUB_MASS','BEDDING','BULB_DISPLAY',
   'ROSE_DISPLAY','LAWN','SCULPTURAL_PLANTING','GROUND_COVER',
   'GARDEN_PALETTE','OTHER')),
 installation_status TEXT NOT NULL CHECK(installation_status IN
  ('INSTALLED_DESCRIBED','CONTRACTED_NOT_VERIFIED_INSTALLED',
   'PROPOSED_ONLY','PHOTO_INFERRED','SPECIES_UNVERIFIED')),
 quantity INTEGER CHECK(quantity IS NULL OR quantity>=0),
 quantity_basis TEXT NOT NULL CHECK(quantity_basis IN
  ('PLANTS_IN_THIS_AREA','PROJECT_WIDE_CONTRACT','VARIETIES_NOT_PLANTS',
   'DESCRIPTIVE_ONLY','UNKNOWN')),
 variety_count INTEGER CHECK(variety_count IS NULL OR variety_count>=0),
 cultivar_name TEXT,
 seasonal_window TEXT,
 growing_pattern TEXT,
 evidence_excerpt TEXT,
 estimated_height_m REAL CHECK(estimated_height_m IS NULL OR estimated_height_m>0),
 model_asset_uri TEXT,
 unreal_layer TEXT NOT NULL DEFAULT 'FMP_HORTICULTURE',
 note TEXT
);
CREATE INDEX IF NOT EXISTS ix_horticulture_plantings ON horticulture_plantings(era_year,area_id,taxon_id);

CREATE TABLE IF NOT EXISTS horticulture_seasonal_events (
 event_id TEXT PRIMARY KEY,
 era_year INTEGER NOT NULL CHECK(era_year IN(1939,1940,1964,1965,2026)),
 area_id TEXT NOT NULL REFERENCES horticulture_areas(area_id),
 planting_id TEXT REFERENCES horticulture_plantings(planting_id),
 source_id TEXT NOT NULL REFERENCES horticulture_sources(source_id),
 event_type TEXT NOT NULL CHECK(event_type IN
  ('PLANTED','BLOOM_REPORTED','PLANTING_REPLACED','WEATHER_DAMAGE','RECOVERY',
   'TRANSPLANTED','MAINTENANCE','MOWING','REMOVAL','SITE_CHANGE','OTHER')),
 date_start TEXT,
 date_end TEXT,
 date_precision TEXT NOT NULL CHECK(date_precision IN('DAY','MONTH','SEASON','YEAR','UNKNOWN')),
 event_status TEXT NOT NULL CHECK(event_status IN('DOCUMENTED','CONTRACTED','RESEARCH_HYPOTHESIS')),
 notes TEXT
);
CREATE TABLE IF NOT EXISTS horticulture_era_links (
 link_id TEXT PRIMARY KEY,
 earlier_area_id TEXT NOT NULL REFERENCES horticulture_areas(area_id),
 later_area_id TEXT NOT NULL REFERENCES horticulture_areas(area_id),
 relation_type TEXT NOT NULL CHECK(relation_type IN
  ('SAME_AREA_REPLANTED','PLANTING_CONTINUED','TREES_RETAINED',
   'TREES_TRANSPLANTED','LANDSCAPE_REDONE','POSSIBLE_ALIGNMENT')),
 source_id TEXT NOT NULL REFERENCES horticulture_sources(source_id),
 certainty TEXT NOT NULL CHECK(certainty IN('VERIFIED','RESEARCH_SUPPORTED','HYPOTHESIS')),
 notes TEXT,
 CHECK(earlier_area_id!=later_area_id)
);
CREATE VIEW IF NOT EXISTS horticulture_research_queue AS
 SELECT a.area_id,a.era_year,a.historical_name,a.area_kind,a.location_status,
 a.source_id,COUNT(p.planting_id) AS planting_records,
 SUM(CASE WHEN p.taxon_id IS NOT NULL THEN 1 ELSE 0 END) AS identified_planting_records,
 SUM(CASE WHEN p.installation_status='INSTALLED_DESCRIBED' THEN 1 ELSE 0 END) AS installed_description_count
 FROM horticulture_areas a LEFT JOIN horticulture_plantings p ON a.area_id=p.area_id
 GROUP BY a.area_id;
CREATE VIEW IF NOT EXISTS horticulture_mapped_areas AS
 SELECT a.* FROM horticulture_areas a
 WHERE a.location_status IN('MAP_TRACED','SITE_REGISTERED')
 AND a.local_polygon_geojson IS NOT NULL;
CREATE TRIGGER IF NOT EXISTS trg_horticulture_area_year
 BEFORE INSERT ON horticulture_areas
 WHEN (SELECT era_year FROM horticulture_sources WHERE source_id=NEW.source_id)!=NEW.era_year
 OR (NEW.parent_area_id IS NOT NULL AND
 (SELECT era_year FROM horticulture_areas WHERE area_id=NEW.parent_area_id)!=NEW.era_year)
 BEGIN SELECT RAISE(ABORT,'Horticulture area source/parent era mismatch'); END;
CREATE TRIGGER IF NOT EXISTS trg_horticulture_planting_year
 BEFORE INSERT ON horticulture_plantings
 WHEN (SELECT era_year FROM horticulture_areas WHERE area_id=NEW.area_id)!=NEW.era_year
 OR (SELECT era_year FROM horticulture_sources WHERE source_id=NEW.source_id)!=NEW.era_year
 BEGIN SELECT RAISE(ABORT,'Planting source/area year mismatch'); END;
CREATE TRIGGER IF NOT EXISTS trg_horticulture_event_year
 BEFORE INSERT ON horticulture_seasonal_events
 WHEN (SELECT era_year FROM horticulture_areas WHERE area_id=NEW.area_id)!=NEW.era_year
 OR (SELECT era_year FROM horticulture_sources WHERE source_id=NEW.source_id)!=NEW.era_year
 OR (NEW.planting_id IS NOT NULL AND
 (SELECT area_id FROM horticulture_plantings WHERE planting_id=NEW.planting_id)!=NEW.area_id)
 BEGIN SELECT RAISE(ABORT,'Horticulture event year/planting mismatch'); END;
CREATE TRIGGER IF NOT EXISTS trg_horticulture_era_link
 BEFORE INSERT ON horticulture_era_links
 WHEN (SELECT era_year FROM horticulture_areas WHERE area_id=NEW.earlier_area_id)
   >=(SELECT era_year FROM horticulture_areas WHERE area_id=NEW.later_area_id)
 OR (NEW.certainty='VERIFIED' AND (SELECT historical_status FROM horticulture_sources
 WHERE source_id=NEW.source_id)='UNKNOWN')
 BEGIN SELECT RAISE(ABORT,'Horticulture time link cannot invert chronology or lack evidence'); END;
