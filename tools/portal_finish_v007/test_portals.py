import unittest,json
from pathlib import Path
import numpy as np,trimesh
from validation_gate import require_clear
R=Path(__file__).parent
class PortalChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((R/'output/portal_manifest.json').read_text());cls.s=trimesh.load(R/'output/ThemeCenter_Framed_Portals_v007.glb',force='scene',process=False)
 def test_four_complete_frames(self):
  for p in self.r['portals']:
   for suffix in ['LEFT_JAMB_REVEAL','RIGHT_JAMB_REVEAL','HEADER_REVEAL','FLUSH_THRESHOLD']:
    self.assertIn(p['id']+'_'+suffix,self.s.graph.nodes_geometry)
 def test_opening_dimensions(self):
  for p in self.r['portals']:
   meshes=[]
   for suffix in ['LEFT_JAMB_REVEAL','RIGHT_JAMB_REVEAL']:
    t,g=self.s.graph[p['id']+'_'+suffix];m=self.s.geometry[g].copy();m.apply_transform(t);meshes.append(m)
   self.assertAlmostEqual(meshes[1].bounds[0,2]-meshes[0].bounds[1,2],p['width'],places=5)
   t,g=self.s.graph[p['id']+'_HEADER_REVEAL'];m=self.s.geometry[g].copy();m.apply_transform(t)
   self.assertAlmostEqual(m.bounds[0,1]-p['floor_y'],2.4,places=5)
 def test_prior_conflicting_parts_disabled(self):
  for n in self.r['disabled']:self.assertNotIn(n,self.s.graph.nodes_geometry)
  self.assertIn('PROVISIONAL_UPPER_EXIT_STAIR',self.r['disabled'])
 def test_braces_contact_frame(self):
  self.assertEqual(len(self.r['brace_cap_contacts']),4)
  self.assertTrue(all(p['all_inside_jamb_x_depth'] and p['cap_triangles']>0 for p in self.r['brace_cap_contacts']))
 def test_all_body_screens_clear(self):
  result=json.loads((R/'output/portal_validation.json').read_text())
  require_clear(result, R/'output/ThemeCenter_Framed_Portals_v007.glb', [p['id'] for p in self.r['portals']])
  self.assertEqual(sum(x['poses'] for x in result['screens']),204)
  self.assertTrue(all(not x['surface_contacts'] for x in result['screens']))
 def test_shell_and_collars_closed(self):
  for n in ['Perisphere_Lower_Removable_Shell__UNREAL_PORTALS_v001','PERISPHERE_LOWER_CURVED_WALL_COLLAR','PERISPHERE_UPPER_CURVED_WALL_COLLAR']:
   t,g=self.s.graph[n];self.assertTrue(self.s.geometry[g].is_watertight,n)
if __name__=='__main__':unittest.main()
