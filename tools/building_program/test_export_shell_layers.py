"""Synthetic regression tests for generic pavilion profile exports."""
import hashlib,json,sys,tempfile,unittest
from pathlib import Path
import trimesh
sys.path.insert(0,str(Path(__file__).resolve().parent))
from export_shell_layers import export
class LayerExportTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  sc=trimesh.Scene()
  for name in ("A_EXTERIOR","B_INTERIOR","C_SHOW"):
   sc.add_geometry(trimesh.creation.box(),node_name=name,geom_name=name)
  self.model=self.root/"source.glb";self.model.write_bytes(sc.export(file_type="glb"))
  self.profile=self.root/"profile.json"
  self.config={"building_id":"TEST","source_sha256":hashlib.sha256(self.model.read_bytes()).hexdigest(),
   "model_accuracy":"SYNTHETIC_TEST","fail_on_unclassified":True,
   "rules":[{"pattern":"^A_","role":"EXTERIOR"},{"pattern":"^B_","role":"INTERIOR"},{"pattern":"^C_","role":"EXHIBIT"}]}
  self.profile.write_text(json.dumps(self.config))
 def tearDown(self):self.tmp.cleanup()
 def test_export(self):
  report=export(self.model,self.profile,self.root/"out")
  self.assertEqual(report["classified_nodes"],3)
  self.assertEqual(len(report["outputs"]),3)
  self.assertFalse(report["steel_required"])
  self.assertTrue(report["original_source_unchanged"])
 def test_wrong_hash(self):
  self.config["source_sha256"]="a"*64;self.profile.write_text(json.dumps(self.config))
  with self.assertRaisesRegex(ValueError,"hash differs"):export(self.model,self.profile,self.root/"bad")
 def test_unknown(self):
  self.config["rules"].pop();self.profile.write_text(json.dumps(self.config))
  with self.assertRaisesRegex(ValueError,"Unclassified"):export(self.model,self.profile,self.root/"bad")
 def test_ambiguous(self):
  self.config["rules"].append({"pattern":"^A_","role":"EXTRA"});self.profile.write_text(json.dumps(self.config))
  with self.assertRaisesRegex(ValueError,"Ambiguous"):export(self.model,self.profile,self.root/"bad")
if __name__=="__main__":unittest.main()
