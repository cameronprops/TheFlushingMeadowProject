"""Standalone synthetic tests: run python3 -m unittest -v test_audit_archival_glb.
Actual original 510-node scene is intentionally NOT stored in Git.
"""
import hashlib, json, tempfile, unittest
from pathlib import Path
import trimesh
from audit_archival_glb import audit

class GLBEvidenceAuditTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        scene=trimesh.Scene()
        scene.add_geometry(trimesh.creation.box(extents=(2,3,4)),node_name='TEST_BUILDING')
        self.model=self.root/'synthetic.glb'
        self.model.write_bytes(scene.export(file_type='glb'))
        self.profile=self.root/'constraints.json'
        self.data={
            'schema':'fmp.architecture.constraints.v1',
            'assembly_id':'SYNTHETIC_BUILDING','period_year':1939,
            'base_model':{'sha256':hashlib.sha256(self.model.read_bytes()).hexdigest()},
            'constraints':[{'id':'SYN-001','place_id':'SYNTHETIC_BUILDING',
                            'component':'TEST_BUILDING','key':'height',
                            'si_value':3.0,'audit_axis':'height_y',
                            'tolerance_m':.00001,'source':'SYNTHETIC',
                            'evidence_status':'SYNTHETIC_FIXTURE'}],
            'rejected_as_built':[],'unresolved':['synthetic'],
        }
        self.profile.write_text(json.dumps(self.data))
    def tearDown(self):
        self.tmp.cleanup()
    def test_height_and_same_geometry_preserved(self):
        old=hashlib.sha256(self.model.read_bytes()).hexdigest()
        result=audit(self.model,self.profile,self.root/'audit',drawings=False)
        self.assertEqual(result['checks'][0]['status'],'MODEL_NUMERIC_PASS_NOT_CERTIFIED')
        self.assertEqual(result['group_counts']['SYNTHETIC_BUILDING'],1)
        self.assertFalse(result['site_registered'])
        self.assertFalse(result['historically_certified'])
        self.assertEqual(hashlib.sha256(self.model.read_bytes()).hexdigest(),old)
        self.assertTrue((self.root/'audit'/'node_register.csv').exists())
    def test_changed_dimension_flags_failure(self):
        self.data['constraints'][0]['si_value']=5.0
        self.profile.write_text(json.dumps(self.data))
        result=audit(self.model,self.profile,self.root/'bad',drawings=False)
        self.assertEqual(result['checks'][0]['status'],'MODEL_NUMERIC_FAIL')
    def test_modified_mesh_rejected(self):
        self.data['base_model']['sha256']='0'*64
        self.profile.write_text(json.dumps(self.data))
        with self.assertRaisesRegex(ValueError,'Source GLB'):
            audit(self.model,self.profile,self.root/'bad',drawings=False)

if __name__=='__main__':unittest.main()
