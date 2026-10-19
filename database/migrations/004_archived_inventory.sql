-- Archived candidates and leads; not verified places or era presence.
CREATE TABLE archive_inventory_candidates (inventory_id TEXT PRIMARY KEY,label TEXT NOT NULL,year_candidates TEXT,category TEXT,zone TEXT,evidence_status TEXT,identity_status TEXT,is_verified_structure TEXT,physical_structure_state TEXT,plans_status TEXT,geometry_status TEXT,gameplay_scope TEXT,source_id TEXT,source_url TEXT,archive_status TEXT,notes TEXT);

CREATE TABLE archive_source_catalog_v2 (source_id TEXT PRIMARY KEY,title TEXT NOT NULL,repository TEXT,source_kind TEXT,catalog_url TEXT,year_scope TEXT,date_on_source TEXT,access_status TEXT,full_source_downloaded TEXT,local_or_drive_location TEXT,sha256 TEXT,rights_status TEXT,priority TEXT,notes TEXT);

CREATE TABLE archive_operations_manual_sheets (sheet_id TEXT PRIMARY KEY,sheet_number INTEGER UNIQUE,title TEXT,year_scope TEXT,source_id TEXT,sheet_catalog_url TEXT,drawing_direct_url TEXT,downloaded TEXT,registered_to_site TEXT,reconstruction_value TEXT,notes TEXT);

CREATE TABLE archive_production_availability (inventory_id TEXT PRIMARY KEY,label TEXT,year_candidates TEXT,priority TEXT,identity TEXT,map_footprint TEXT,floorplan TEXT,elevations_sections TEXT,period_photographs TEXT,terrain_elevation TEXT,exterior_model TEXT,interior_model TEXT,historical_show TEXT,gameplay TEXT,testing TEXT,next_research TEXT);
