import hashlib,json,os,unittest
from pathlib import Path
import trimesh
from tools.world_build.audit_helicline_join import SOURCE_SHA,world_mesh
class SharedPortalTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=Path(os.environ.get('FMP_V004_DIR','out-r4'))
  cls.r=json.loads((cls.root/'Shared_Portals_v004.json').read_text())
  cls.scene=trimesh.load(cls.root/cls.r['output'],force='scene')
 def test_export_hash_and_closed_replacements(self):
  self.assertEqual(hashlib.sha256((self.root/self.r['output']).read_bytes()).hexdigest(),self.r['overlay_sha256'])
  for row in self.r['replacements']:
   m=world_mesh(self.scene,row['replacement_node']);self.assertTrue(m.is_watertight);self.assertTrue(m.is_winding_consistent)
 def test_limited_material_removal(self):
  for row in self.r['replacements']:
   removed=row['source_volume_m3']-row['replacement_volume_m3']
   self.assertGreaterEqual(removed,-1e-8);self.assertLess(removed/row['source_volume_m3'],.02)
 def test_no_duplicate_original_replacement_nodes(self):
  for row in self.r['replacements']:
   self.assertNotIn(row['source_node'],self.scene.graph.nodes)
   self.assertIn(row['source_node'],self.r['hide_source_nodes'])
 def test_clearance_report_belongs_to_this_revision(self):
  c=json.loads((self.root/'Return_Route_Clearance_v004.json').read_text())
  self.assertEqual(c['overlay_sha256'],self.r['overlay_sha256']);self.assertEqual(c['source_sha256'],SOURCE_SHA)
  self.assertEqual(c['pose_count'],435);self.assertEqual(c['findings'],[])
  self.assertEqual(c['hidden_source_nodes'],sorted(self.r['hide_source_nodes']))
  self.assertEqual(self.r['historical_acceptance'],'UNVERIFIED')
if __name__=='__main__':unittest.main()
