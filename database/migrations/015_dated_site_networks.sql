-- FMP 015 - Historical fairground circulation and infrastructure.
-- A record with no geometry is a source-backed RESEARCH PLACEHOLDER, not a mapped line.
-- Historical years are separate; later geometry NEVER backfills an earlier era.
CREATE TABLE IF NOT EXISTS site_network_sheets (
  sheet_id TEXT PRIMARY KEY,
  era_year INTEGER NOT NULL CHECK(era_year IN (1939,1940,1964,1965,2026)),
  sheet_title TEXT NOT NULL,
  sheet_number TEXT,
  archive_collection TEXT NOT NULL,
  archive_url TEXT NOT NULL,
  primary_layer TEXT NOT NULL,
  availability TEXT NOT NULL CHECK(availability IN
    ('CATALOG_ONLY','VIEWABLE','ACQUIRED','GEOREGISTERED','TRACED')),
  status_note TEXT
);
CREATE TABLE IF NOT EXISTS site_network_layers (
  layer_id TEXT PRIMARY KEY,
  family TEXT NOT NULL CHECK(family IN ('ACCESS','UTILITY','TOPOGRAPHY','CONTROL')),
  medium TEXT NOT NULL,
  walkable INTEGER NOT NULL DEFAULT 0 CHECK(walkable IN (0,1)),
  typically_buried INTEGER NOT NULL DEFAULT 0 CHECK(typically_buried IN (0,1)),
  description TEXT
);
CREATE TABLE IF NOT EXISTS site_network_features (
  feature_id TEXT PRIMARY KEY,
  canonical_name TEXT NOT NULL,
  feature_kind TEXT NOT NULL CHECK(feature_kind IN
   ('NAMED_STREET','PEDESTRIAN_PATH','SERVICE_ALLEY','PLAZA','BRIDGE',
    'GATE','JUNCTION','PIPE','MANHOLE','CONDUIT','PUMP','UTILITY_NODE',
    'CANAL','OTHER')),
  identity_status TEXT NOT NULL CHECK(identity_status IN
   ('DOCUMENTED_NAMED','CATALOG_LEAD','WORKING_LABEL','UNCERTAIN')),
  comment TEXT
);
CREATE TABLE IF NOT EXISTS site_network_nodes (
  node_id TEXT PRIMARY KEY,
  era_year INTEGER NOT NULL CHECK(era_year IN (1939,1940,1964,1965,2026)),
  layer_id TEXT NOT NULL REFERENCES site_network_layers(layer_id),
  name TEXT NOT NULL,
  x_m REAL,y_m REAL,z_m REAL,
  coordinate_frame TEXT NOT NULL DEFAULT 'UNREGISTERED',
  horizontal_crs TEXT,
  vertical_datum TEXT,
  location_status TEXT NOT NULL CHECK(location_status IN
   ('UNLOCATED','PHOTO_APPROXIMATE','MAP_TRACED','REGISTERED')),
  source_sheet_id TEXT REFERENCES site_network_sheets(sheet_id),
  CHECK((x_m IS NULL AND y_m IS NULL AND z_m IS NULL) OR
        (x_m IS NOT NULL AND y_m IS NOT NULL AND z_m IS NOT NULL)),
  CHECK(location_status!='REGISTERED' OR
        (x_m IS NOT NULL AND horizontal_crs IS NOT NULL AND vertical_datum IS NOT NULL))
);
CREATE TABLE IF NOT EXISTS site_network_segments (
  segment_id TEXT PRIMARY KEY,
  feature_id TEXT NOT NULL REFERENCES site_network_features(feature_id),
  era_year INTEGER NOT NULL CHECK(era_year IN (1939,1940,1964,1965,2026)),
  layer_id TEXT NOT NULL REFERENCES site_network_layers(layer_id),
  historical_name TEXT,
  from_node_id TEXT REFERENCES site_network_nodes(node_id),
  to_node_id TEXT REFERENCES site_network_nodes(node_id),
  geojson_geometry TEXT,
  source_sheet_id TEXT REFERENCES site_network_sheets(sheet_id),
  alignment_status TEXT NOT NULL CHECK(alignment_status IN
   ('UNTRACED','INTERPRETIVE','PLAN_TRACED','GEOREGISTERED')),
  width_m REAL CHECK(width_m IS NULL OR width_m>0),
  depth_m REAL CHECK(depth_m IS NULL OR depth_m>=0),
  invert_elevation_m REAL,
  flow_direction TEXT CHECK(flow_direction IN ('A_TO_B','B_TO_A','BIDIRECTIONAL','UNKNOWN') OR flow_direction IS NULL),
  access_class TEXT NOT NULL CHECK(access_class IN
   ('PUBLIC','STAFF_ONLY','VEHICLES_ONLY','RESTRICTED','NOT_APPLICABLE','UNKNOWN')),
  navigable INTEGER NOT NULL DEFAULT 0 CHECK(navigable IN(0,1)),
  estimated_accuracy_m REAL,
  note TEXT,
  CHECK(from_node_id IS NULL OR to_node_id IS NULL OR from_node_id!=to_node_id),
  CHECK(navigable=0 OR
    (alignment_status IN ('PLAN_TRACED','GEOREGISTERED')
     AND from_node_id IS NOT NULL AND to_node_id IS NOT NULL
     AND geojson_geometry IS NOT NULL AND access_class='PUBLIC'))
);
CREATE INDEX IF NOT EXISTS ix_network_segments_layer ON site_network_segments(era_year,layer_id);
CREATE INDEX IF NOT EXISTS ix_network_segments_feature ON site_network_segments(feature_id,era_year);
CREATE TABLE IF NOT EXISTS site_network_era_relations (
  relation_id TEXT PRIMARY KEY,
  earlier_segment_id TEXT NOT NULL REFERENCES site_network_segments(segment_id),
  later_segment_id TEXT NOT NULL REFERENCES site_network_segments(segment_id),
  relation_type TEXT NOT NULL CHECK(relation_type IN
    ('ALIGNMENT_PERSISTED','REALIGNED','REPLACED','REUSED_RIGHT_OF_WAY','POSSIBLE_LINK')),
  evidence_sheet_id TEXT REFERENCES site_network_sheets(sheet_id),
  confidence TEXT NOT NULL CHECK(confidence IN ('VERIFIED','LIKELY','UNVERIFIED')),
  note TEXT,
  CHECK(earlier_segment_id!=later_segment_id)
);
-- Only historically traced and deliberately enabled PUBLIC routes enter the walk graph.
CREATE VIEW IF NOT EXISTS site_walkable_edges AS
 SELECT s.* FROM site_network_segments s
 JOIN site_network_layers l ON l.layer_id=s.layer_id
 WHERE l.walkable=1 AND s.navigable=1 AND s.access_class='PUBLIC';
-- All utility lines retain exact source references and dated visibility.
CREATE VIEW IF NOT EXISTS site_utility_segments AS
 SELECT s.*,l.medium,l.typically_buried FROM site_network_segments s
 JOIN site_network_layers l ON l.layer_id=s.layer_id WHERE l.family='UTILITY';
-- Dashboard distinguishes cataloged sheets, traced geometry, and walkable graph coverage.
CREATE VIEW IF NOT EXISTS site_network_progress AS
 SELECT e.year AS era_year,
 (SELECT COUNT(*) FROM site_network_sheets sh WHERE sh.era_year=e.year) AS cataloged_sheets,
 (SELECT COUNT(*) FROM site_network_segments s WHERE s.era_year=e.year) AS candidate_segments,
 (SELECT COUNT(*) FROM site_network_segments s WHERE s.era_year=e.year AND s.geojson_geometry IS NOT NULL) AS mapped_segments,
 (SELECT COUNT(*) FROM site_walkable_edges w WHERE w.era_year=e.year) AS walkable_edges
 FROM eras e;

-- Reject connections between mismatched historical years and utility layers.
CREATE TRIGGER IF NOT EXISTS site_segment_node_era_gate
BEFORE INSERT ON site_network_segments
WHEN (NEW.from_node_id IS NOT NULL AND EXISTS (
   SELECT 1 FROM site_network_nodes n WHERE n.node_id=NEW.from_node_id
       AND (n.era_year!=NEW.era_year OR n.layer_id!=NEW.layer_id)))
 OR (NEW.to_node_id IS NOT NULL AND EXISTS (
   SELECT 1 FROM site_network_nodes n WHERE n.node_id=NEW.to_node_id
       AND (n.era_year!=NEW.era_year OR n.layer_id!=NEW.layer_id)))
BEGIN
 SELECT RAISE(ABORT,'Site network node era/layer mismatch');
END;
CREATE TRIGGER IF NOT EXISTS site_segment_node_era_update_gate
BEFORE UPDATE OF from_node_id,to_node_id,era_year,layer_id ON site_network_segments
WHEN (NEW.from_node_id IS NOT NULL AND EXISTS (
   SELECT 1 FROM site_network_nodes n WHERE n.node_id=NEW.from_node_id
       AND (n.era_year!=NEW.era_year OR n.layer_id!=NEW.layer_id)))
 OR (NEW.to_node_id IS NOT NULL AND EXISTS (
   SELECT 1 FROM site_network_nodes n WHERE n.node_id=NEW.to_node_id
       AND (n.era_year!=NEW.era_year OR n.layer_id!=NEW.layer_id)))
BEGIN
 SELECT RAISE(ABORT,'Site network node era/layer mismatch');
END;
-- Linking segments across periods is explicit and cannot be asserted by a
-- similar line appearing on two maps. Earlier must precede later.
CREATE TRIGGER IF NOT EXISTS site_network_temporal_relation_gate
BEFORE INSERT ON site_network_era_relations
WHEN (SELECT era_year FROM site_network_segments WHERE segment_id=NEW.earlier_segment_id)
   >= (SELECT era_year FROM site_network_segments WHERE segment_id=NEW.later_segment_id)
 OR (NEW.confidence='VERIFIED' AND NEW.evidence_sheet_id IS NULL)
BEGIN
 SELECT RAISE(ABORT,'Temporal relation requires earlier year and source evidence');
END;
