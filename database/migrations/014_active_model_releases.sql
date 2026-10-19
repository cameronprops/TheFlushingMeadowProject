-- FMP 014: one active release pointer per building/year/role.
-- No deletion of source-version assets or individual mesh observations.
CREATE TABLE IF NOT EXISTS master_active_model_releases (
  release_key TEXT PRIMARY KEY,
  building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
  period_year INTEGER NOT NULL CHECK(period_year IN (1939,1940,1964,1965,2026)),
  logical_role TEXT NOT NULL,
  active_media_id TEXT NOT NULL REFERENCES master_media_assets(media_id),
  source_path TEXT NOT NULL,
  source_sha256 TEXT NOT NULL,
  up_axis TEXT NOT NULL CHECK(up_axis IN ('X','Y','Z')),
  selected_nodes TEXT,
  observed_utc TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'MODEL_OBSERVED_NOT_HISTORIC_CERTIFIED',
  UNIQUE(building_id,period_year,logical_role)
);
CREATE VIEW IF NOT EXISTS master_active_model_components AS
 SELECT p.* FROM master_model_components p
 JOIN master_active_model_releases r
 ON p.model_asset_id=r.active_media_id
 AND p.building_id=r.building_id AND p.period_year=r.period_year;
CREATE VIEW IF NOT EXISTS master_active_model_summary AS
 SELECT r.release_key,r.building_id,r.period_year,r.logical_role,
 r.active_media_id,r.source_path,r.source_sha256,r.observed_utc,
 COUNT(p.component_id) AS parts,
 SUM(CASE WHEN p.watertight=1 THEN 1 ELSE 0 END) AS closed_parts,
 COUNT(DISTINCT p.material_name) AS material_groups,
 MIN(p.min_x_m) AS min_x_m, MIN(p.min_y_m) AS min_y_m,
 MIN(p.min_z_m) AS min_z_m, MAX(p.max_x_m) AS max_x_m,
 MAX(p.max_y_m) AS max_y_m, MAX(p.max_z_m) AS max_z_m
 FROM master_active_model_releases r
 LEFT JOIN master_model_components p ON p.model_asset_id=r.active_media_id
 GROUP BY r.release_key;
