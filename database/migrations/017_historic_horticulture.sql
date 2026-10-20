-- Dated horticulture, integrated with site amenity and network research.
CREATE TABLE IF NOT EXISTS site_plant_sources (
 source_id TEXT PRIMARY KEY, era_year INTEGER NOT NULL,
 title TEXT NOT NULL, institution TEXT NOT NULL, locator TEXT,
 url TEXT NOT NULL, status TEXT NOT NULL, notes TEXT
);
CREATE TABLE IF NOT EXISTS site_plant_taxa (
 taxon_id TEXT PRIMARY KEY, common_name TEXT NOT NULL,
 botanical_name TEXT, botanical_id_status TEXT NOT NULL DEFAULT 'UNVERIFIED',
 form TEXT NOT NULL, notes TEXT
);
CREATE TABLE IF NOT EXISTS site_planting_beds (
 bed_id TEXT PRIMARY KEY, era_year INTEGER NOT NULL,
 name TEXT NOT NULL, garden_or_zone TEXT, nearby_building_id TEXT REFERENCES building_dossiers(building_id),
 planting_role TEXT NOT NULL, soil_or_hardscape TEXT,
 source_id TEXT REFERENCES site_plant_sources(source_id),
 geometry_geojson TEXT, coordinate_frame TEXT NOT NULL DEFAULT 'UNREGISTERED',
 geometry_status TEXT NOT NULL CHECK (geometry_status IN
 ('NOT_LOCATED','NAMED_AREA','PHOTO_INFERRED','PLAN_TRACED','SITE_REGISTERED')),
 season TEXT, notes TEXT,
 CHECK(geometry_geojson IS NULL OR geometry_status IN ('PLAN_TRACED','SITE_REGISTERED'))
);
CREATE TABLE IF NOT EXISTS site_planting_schedules (
 schedule_id TEXT PRIMARY KEY,
 bed_id TEXT NOT NULL REFERENCES site_planting_beds(bed_id),
 taxon_id TEXT NOT NULL REFERENCES site_plant_taxa(taxon_id),
 quantity INTEGER CHECK(quantity IS NULL OR quantity>=0),
 spacing_m REAL CHECK(spacing_m IS NULL OR spacing_m>0),
 planting_pattern TEXT, seasonal_phase TEXT,
 evidence_class TEXT NOT NULL CHECK(evidence_class IN
 ('DRAWING_SPECIFIED','CONTRACT_SPECIFIED','PERIOD_TEXT','PHOTO_INFERRED','UNVERIFIED')),
 source_id TEXT REFERENCES site_plant_sources(source_id), notes TEXT,
 UNIQUE(bed_id,taxon_id,seasonal_phase)
);
CREATE TABLE IF NOT EXISTS site_individual_plants (
 plant_id TEXT PRIMARY KEY, bed_id TEXT REFERENCES site_planting_beds(bed_id),
 taxon_id TEXT REFERENCES site_plant_taxa(taxon_id),
 era_year INTEGER NOT NULL, planting_status TEXT NOT NULL,
 x_m REAL,y_m REAL,z_m REAL, coordinate_frame TEXT NOT NULL DEFAULT 'UNREGISTERED',
 location_status TEXT NOT NULL CHECK(location_status IN
 ('UNLOCATED','PHOTO_ESTIMATED','PLAN_TRACED','SITE_REGISTERED')),
 source_id TEXT REFERENCES site_plant_sources(source_id),
 model_asset_uri TEXT, notes TEXT,
 CHECK ((x_m IS NULL AND y_m IS NULL AND z_m IS NULL) OR
 (x_m IS NOT NULL AND y_m IS NOT NULL AND z_m IS NOT NULL)),
 CHECK (location_status NOT IN ('PLAN_TRACED','SITE_REGISTERED') OR
 (x_m IS NOT NULL AND source_id IS NOT NULL))
);
CREATE TABLE IF NOT EXISTS site_plant_era_relations (
 relation_id TEXT PRIMARY KEY,
 earlier_plant_id TEXT NOT NULL REFERENCES site_individual_plants(plant_id),
 later_plant_id TEXT NOT NULL REFERENCES site_individual_plants(plant_id),
 relationship TEXT NOT NULL CHECK(relationship IN
 ('SAME_TREE','TRANSPLANTED','REPLACED','POSSIBLE_RELATION')),
 source_id TEXT REFERENCES site_plant_sources(source_id),
 certainty TEXT NOT NULL, notes TEXT
);
CREATE VIEW IF NOT EXISTS site_horticulture_progress AS
 SELECT b.era_year, COUNT(*) AS beds,
 SUM(CASE WHEN b.geometry_geojson IS NOT NULL THEN 1 ELSE 0 END) AS traced_beds,
 (SELECT COUNT(*) FROM site_planting_schedules s JOIN site_planting_beds x ON s.bed_id=x.bed_id WHERE x.era_year=b.era_year) AS plant_schedule_rows
 FROM site_planting_beds b GROUP BY b.era_year;
