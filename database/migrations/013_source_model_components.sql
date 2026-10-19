-- FMP 013: source-mesh inventory from existing GLB releases.
-- This is observed geometry (NOT historic certification, footprint registration or printed part QA).
CREATE TABLE IF NOT EXISTS master_model_components(
 component_id TEXT PRIMARY KEY,
 building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
 period_year INTEGER NOT NULL CHECK(period_year IN (1939,1940,1964,1965,2026)),
 model_asset_id TEXT NOT NULL REFERENCES master_media_assets(media_id),
 source_node TEXT NOT NULL,
 mesh_key TEXT NOT NULL,
 role TEXT NOT NULL,
 coordinate_frame TEXT NOT NULL,
 min_x_m REAL NOT NULL,min_y_m REAL NOT NULL,min_z_m REAL NOT NULL,
 max_x_m REAL NOT NULL,max_y_m REAL NOT NULL,max_z_m REAL NOT NULL,
 vertices INTEGER NOT NULL CHECK(vertices>0),
 faces INTEGER NOT NULL CHECK(faces>0),
 watertight INTEGER NOT NULL CHECK(watertight IN (0,1)),
 material_name TEXT,
 roughness REAL,
 metallic REAL,
 source_sha256 TEXT NOT NULL,
 verification_status TEXT NOT NULL,
 CHECK(min_x_m<=max_x_m AND min_y_m<=max_y_m AND min_z_m<=max_z_m),
 UNIQUE(building_id,period_year,model_asset_id,source_node)
);
CREATE INDEX IF NOT EXISTS ix_master_model_components_building ON master_model_components(building_id,period_year,role);
CREATE VIEW IF NOT EXISTS master_model_materials AS
SELECT building_id,period_year,model_asset_id,material_name,
 COUNT(*) AS mesh_parts,SUM(faces) AS face_count,
 SUM(CASE WHEN watertight=1 THEN 1 ELSE 0 END) AS watertight_meshes,
 MIN(roughness) AS roughness_min,MAX(roughness) AS roughness_max
FROM master_model_components
GROUP BY building_id,period_year,model_asset_id,material_name;
