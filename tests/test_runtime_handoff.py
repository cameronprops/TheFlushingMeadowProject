"""Portable tests: python3 -m unittest -v tests.test_runtime_handoff."""
import hashlib, json, sqlite3, tempfile, unittest
from pathlib import Path
from tools.building_program.export_runtime_handoff import bundle, export, unreal_transform

CREATE='''
CREATE TABLE building_dossiers(building_id TEXT PRIMARY KEY,classification TEXT,site_position_status TEXT,footprint_status TEXT,public_access_status TEXT);
CREATE TABLE master_active_model_releases(release_key TEXT PRIMARY KEY,building_id TEXT,period_year INTEGER,logical_role TEXT,active_media_id TEXT,source_path TEXT,source_sha256 TEXT,up_axis TEXT);
CREATE TABLE master_model_components(component_id TEXT PRIMARY KEY,building_id TEXT,period_year INTEGER,model_asset_id TEXT,source_node TEXT,mesh_key TEXT,role TEXT,source_sha256 TEXT,min_x_m REAL,min_y_m REAL,min_z_m REAL,max_x_m REAL,max_y_m REAL,max_z_m REAL,vertices INTEGER,faces INTEGER,watertight INTEGER,material_name TEXT,roughness REAL,metallic REAL);
CREATE TABLE master_interactive_points(point_id TEXT PRIMARY KEY,building_id TEXT,period_year INTEGER,label TEXT,interaction_type TEXT,trigger_or_scene_key TEXT,requested_behavior TEXT,x_m REAL,y_m REAL,z_m REAL,position_status TEXT,coordinate_frame TEXT,native_unreal_tested INTEGER);
CREATE TABLE building_spaces(space_id TEXT,building_id TEXT,year INTEGER,space_name TEXT,access_intent TEXT,collision_status TEXT,navigation_status TEXT);
CREATE TABLE master_building_envelopes(envelope_id TEXT,source_asset_id TEXT,coordinate_frame TEXT,evidence_status TEXT,site_registered INTEGER,building_id TEXT,period_year INTEGER);
CREATE VIEW master_all_media AS SELECT '' AS media_ref,'' AS record_type,'' AS title,'' AS media_kind,'' AS uri,'' AS project_uri,'' AS rights_status,'' AS acquisition_status,'' AS building_id,NULL AS period_year WHERE 0;
'''
class TestHandoff(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.dir=Path(self.tmp.name)
        self.db=sqlite3.connect(':memory:');self.db.row_factory=sqlite3.Row;self.db.executescript(CREATE)
        self.db.execute("INSERT INTO building_dossiers VALUES ('WF0002','ARCHITECTURE_LISTED','UNREGISTERED','NOT_TRACED','NOT_TESTED')")
        self.db.execute("INSERT INTO master_active_model_releases VALUES ('r','WF0002',1939,'EXTERIOR_SHELL','source','thing.glb','abc','Y')")
        self.db.execute("INSERT INTO master_model_components VALUES ('mesh1','WF0002',1939,'source','Sphere','s1','MODEL_PART','abc',-1,0,-1,1,2,1,99,99,1,'white',0.7,0.0)")
        self.db.execute("INSERT INTO master_interactive_points VALUES ('entry','WF0002',1939,'Arrival','ENTRY','ENT','Enter',NULL,NULL,NULL,'UNLOCATED','UNREGISTERED',0)")
    def tearDown(self):self.db.close();self.tmp.cleanup()
    def test_manifest_has_models_materials_hotspots(self):
        obj=bundle(self.db,'WF0002',1939,250)
        self.assertEqual(len(obj['models']),1)
        self.assertEqual(obj['models'][0]['preview_print_size_mm'],[8,8,8])
        self.assertEqual(obj['models'][0]['watertight_mesh_count'],1)
        self.assertEqual(obj['material_slots'][0]['source_material_name'],'white')
        self.assertIsNone(obj['interactive_points'][0]['position_xyz_m'])
        self.assertFalse(obj['geometry_registration']['site_registered'])
        self.assertIsNone(obj['geometry_registration']['projector_intrinsics'])
    def test_unreal_frame_correct_handedness(self):
        y=unreal_transform('Y');z=unreal_transform('Z')
        self.assertEqual([sum(y[i][j]*[1,2,3][j] for j in range(3)) for i in range(3)],[100,300,200])
        self.assertEqual([sum(z[i][j]*[1,2,3][j] for j in range(3)) for i in range(3)],[100,-200,300])
        with self.assertRaises(ValueError):unreal_transform('X')
    def test_stable_export_bytes(self):
        a=export(self.db,self.dir,denominator=200)
        raw=(self.dir/'WF0002_1939_handoff.json').read_bytes()
        b=export(self.db,self.dir,denominator=200)
        self.assertEqual(a,b);self.assertEqual(raw,(self.dir/'WF0002_1939_handoff.json').read_bytes())
        self.assertEqual(a['buildings'][0]['sha256'],hashlib.sha256(raw).hexdigest())
    def test_rejects_mismatched_model_hash(self):
        self.db.execute("UPDATE master_active_model_releases SET source_sha256='bad'")
        with self.assertRaisesRegex(ValueError,'Hash mismatch'):bundle(self.db,'WF0002',1939,250)
    def test_incomplete_hotspot_fails(self):
        self.db.execute("UPDATE master_interactive_points SET x_m=2")
        with self.assertRaisesRegex(ValueError,'Partial'):bundle(self.db,'WF0002',1939,250)
    def test_unlocated_hotspot_never_faked(self):
        self.db.execute("UPDATE master_interactive_points SET x_m=1,y_m=2,z_m=3")
        with self.assertRaisesRegex(ValueError,'Unlocated'):bundle(self.db,'WF0002',1939,250)
    def test_invalid_print_scale(self):
        with self.assertRaises(ValueError):bundle(self.db,'WF0002',1939,0)
    def test_read_only(self):
        before=self.db.total_changes
        bundle(self.db,'WF0002',1939,250)
        self.assertEqual(before,self.db.total_changes)
if __name__=='__main__':unittest.main()
