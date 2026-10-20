-- FMP 018 / FAIRGROUND ATLAS: evidence-gated site staging and coordinate handoff.
-- Pixel traces are NOT projected coordinates. One shared record links all world objects.
-- Geometry rows are authored in catalog/atlas_placements.csv, not managed separately.
CREATE TABLE IF NOT EXISTS atlas_reference_maps (
 map_id TEXT PRIMARY KEY,
 era_year INTEGER NOT NULL CHECK(era_year IN(1939,1940,1964,1965,2026)),
 title TEXT NOT NULL,
 source_uri TEXT NOT NULL,
 linked_sheet_id TEXT REFERENCES site_network_sheets(sheet_id),
 access_status TEXT NOT NULL CHECK(access_status IN
   ('REFERENCE_ONLY','RASTER_ACQUIRED','CONTROL_POINTS_SET','AFFINE_FITTED','INDEPENDENTLY_REVIEWED')),
 raster_file TEXT, raster_sha256 TEXT, image_width_px INTEGER, image_height_px INTEGER,
 projected_crs TEXT, vertical_datum TEXT, affine_json TEXT,
 control_rmse_m REAL, holdout_rmse_m REAL,
 status TEXT NOT NULL CHECK(status IN('UNALIGNED','CALIBRATED_PREVIEW','REGISTERED_REVIEWED')),
 provenance_note TEXT,
 CHECK(status!='REGISTERED_REVIEWED' OR
   (projected_crs IS NOT NULL AND vertical_datum IS NOT NULL AND
    affine_json IS NOT NULL AND holdout_rmse_m IS NOT NULL)),
 CHECK(image_width_px IS NULL OR image_width_px>0),
 CHECK(image_height_px IS NULL OR image_height_px>0)
);
CREATE TABLE IF NOT EXISTS atlas_world_frames (
 frame_id TEXT PRIMARY KEY,
 era_year INTEGER NOT NULL CHECK(era_year IN(1939,1940,1964,1965,2026)),
 projected_crs TEXT NOT NULL,
 origin_e_m REAL NOT NULL, origin_n_m REAL NOT NULL,
 origin_z_m REAL NOT NULL,
 vertical_datum TEXT,
 xy_unit TEXT NOT NULL DEFAULT 'metres' CHECK(xy_unit='metres'),
 z_unit TEXT NOT NULL DEFAULT 'metres' CHECK(z_unit='metres'),
 unreal_axis TEXT NOT NULL DEFAULT 'X_EAST_Y_NORTH_Z_UP',
 status TEXT NOT NULL CHECK(status IN('DRAFT','REVIEWED')),
 control_source_uri TEXT,
 note TEXT,
 CHECK(status!='REVIEWED' OR vertical_datum IS NOT NULL)
);
CREATE TABLE IF NOT EXISTS atlas_placements (
 placement_id TEXT PRIMARY KEY,
 era_year INTEGER NOT NULL CHECK(era_year IN(1939,1940,1964,1965,2026)),
 entity_type TEXT NOT NULL CHECK(entity_type IN
  ('BUILDING','EXHIBIT','FOUNTAIN','WATER','GARDEN','TREE','FURNISHING',
   'SCULPTURE','STREET','PATH','SERVICE','UTILITY','SITE_FEATURE','OTHER')),
 entity_id TEXT NOT NULL,
 display_name TEXT NOT NULL,
 layer_id TEXT NOT NULL,
 source_map_id TEXT NOT NULL REFERENCES atlas_reference_maps(map_id),
 source_uri TEXT NOT NULL,
 geometry_kind TEXT NOT NULL CHECK(geometry_kind IN('POINT','LINE','POLYGON')),
 pixel_vertices_json TEXT,
 projected_vertices_json TEXT,
 frame_id TEXT REFERENCES atlas_world_frames(frame_id),
 placement_status TEXT NOT NULL CHECK(placement_status IN
  ('UNPLACED','RASTER_TRACE','PROJECTED_PREVIEW','REGISTERED_REVIEWED')),
 historical_evidence TEXT NOT NULL CHECK(historical_evidence IN
  ('PERIOD_PLAN','PERIOD_PHOTO','CONTRACT_PLAN','SECONDARY_REFERENCE',
   'INTERPRETIVE','NOT_YET_REVIEWED')),
 uncertainty_m REAL CHECK(uncertainty_m IS NULL OR uncertainty_m>=0),
 variant TEXT NOT NULL DEFAULT 'AS_RESEARCHED',
 rotation_deg REAL,
 height_offset_m REAL,
 asset_role TEXT,
 note TEXT,
 CHECK((placement_status='UNPLACED' AND pixel_vertices_json IS NULL AND projected_vertices_json IS NULL)
 OR (placement_status='RASTER_TRACE' AND pixel_vertices_json IS NOT NULL AND projected_vertices_json IS NULL)
 OR (placement_status='PROJECTED_PREVIEW' AND pixel_vertices_json IS NOT NULL AND projected_vertices_json IS NOT NULL)
 OR (placement_status='REGISTERED_REVIEWED' AND projected_vertices_json IS NOT NULL AND frame_id IS NOT NULL
      AND uncertainty_m IS NOT NULL)),
 CHECK(placement_status!='REGISTERED_REVIEWED'
    OR historical_evidence IN('PERIOD_PLAN','PERIOD_PHOTO','CONTRACT_PLAN')),
 UNIQUE(era_year,entity_type,entity_id,variant)
);
CREATE INDEX IF NOT EXISTS ix_atlas_placement_year ON atlas_placements(era_year,layer_id,placement_status);
CREATE TABLE IF NOT EXISTS atlas_placement_reviews (
 review_id TEXT PRIMARY KEY,
 placement_id TEXT NOT NULL REFERENCES atlas_placements(placement_id),
 decision TEXT NOT NULL CHECK(decision IN('APPROVED','REJECTED','NEEDS_REVISION','QUESTION')),
 reviewer TEXT NOT NULL,
 review_date TEXT NOT NULL,
 evidence_uri TEXT,
 note TEXT
);
CREATE VIEW IF NOT EXISTS atlas_unreal_ready AS
 SELECT p.*,f.projected_crs,f.origin_e_m,f.origin_n_m,f.origin_z_m
 FROM atlas_placements p
 JOIN atlas_world_frames f ON p.frame_id=f.frame_id
 JOIN atlas_reference_maps m ON p.source_map_id=m.map_id
 WHERE p.placement_status='REGISTERED_REVIEWED'
 AND m.status='REGISTERED_REVIEWED'
 AND f.status='REVIEWED'
 AND EXISTS (SELECT 1 FROM atlas_placement_reviews r
  WHERE r.placement_id=p.placement_id AND r.decision='APPROVED');
CREATE VIEW IF NOT EXISTS atlas_review_queue AS
 SELECT p.placement_id,p.era_year,p.display_name,p.entity_type,p.layer_id,
 p.placement_status,p.historical_evidence,p.source_map_id,p.source_uri
 FROM atlas_placements p WHERE p.placement_status!='REGISTERED_REVIEWED';
CREATE TRIGGER IF NOT EXISTS trg_atlas_placement_era
 BEFORE INSERT ON atlas_placements
 WHEN (SELECT era_year FROM atlas_reference_maps WHERE map_id=NEW.source_map_id)!=NEW.era_year
 OR (NEW.frame_id IS NOT NULL AND
 (SELECT era_year FROM atlas_world_frames WHERE frame_id=NEW.frame_id)!=NEW.era_year)
 BEGIN SELECT RAISE(ABORT,'Atlas placement map or frame belongs to another era'); END;
CREATE TRIGGER IF NOT EXISTS trg_atlas_map_no_direct_approval
 BEFORE INSERT ON atlas_placements
 WHEN NEW.placement_status='REGISTERED_REVIEWED' AND
 (SELECT status FROM atlas_reference_maps WHERE map_id=NEW.source_map_id)!='REGISTERED_REVIEWED'
 BEGIN SELECT RAISE(ABORT,'Cannot approve placement on unreviewed map'); END;
