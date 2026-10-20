import unittest,tempfile,json,copy
from pathlib import Path
import numpy as np,trimesh
from asset_fixes import *
ROOT=Path(__file__).parent
SRC=ROOT/'inputs/ThemeCenter_v005.glb'
WF=ROOT/'inputs/WF0028_v015'
class Fixes(unittest.TestCase):
 def test_actual_repair_preserves_geometry_and_metadata(self):
  d,b=read_glb(SRC);e,c=read_glb(ROOT/'output/ThemeCenter_WindingRepair_v006.glb')
  self.assertEqual(d['nodes'],e['nodes']);self.assertEqual(d['materials'],e['materials']);self.assertEqual(d['scenes'],e['scenes']);self.assertEqual(b,c[:len(b)])
  for i,(m,n) in enumerate(zip(d['meshes'],e['meshes'])):
   if i not in [354,355,356,357,358]:self.assertEqual(m,n);continue
   p=m['primitives'][0];q=n['primitives'][0]
   self.assertEqual(p['attributes']['POSITION'],q['attributes']['POSITION']);self.assertEqual(p['attributes']['COLOR_0'],q['attributes']['COLOR_0'])
   f=array(d,b,p['indices']).reshape(-1,3);g=array(e,c,q['indices']).reshape(-1,3)
   np.testing.assert_array_equal(np.sort(f,axis=1),np.sort(g,axis=1))
   mesh=trimesh.Trimesh(array(e,c,q['attributes']['POSITION']),g,process=False)
   self.assertTrue(mesh.is_winding_consistent);self.assertTrue(np.isfinite(array(e,c,q['attributes']['NORMAL'])).all())
 def test_actual_filter(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t)/'out.glb';r=export_runtime(str(WF)+'.glb',str(WF)+'.json',out)
   d,b=read_glb(str(WF)+'.glb');e,c=read_glb(out)
   self.assertEqual(b,c);self.assertEqual(len(e['meshes']),len(r['runtime_render_and_collision_candidates']))
   for a,z in zip(d['nodes'],e['nodes']):
    expected=copy.deepcopy(a)
    if a.get('name') in r['excluded']:expected.pop('mesh',None)
    elif 'mesh' in a:
     self.assertEqual(d['meshes'][a['mesh']],e['meshes'][z['mesh']]);expected['mesh']=z['mesh']
    self.assertEqual(expected,z)
   active=set(trimesh.load(out,force='scene',process=False).graph.nodes_geometry)
   self.assertEqual(active,set(r['runtime_render_and_collision_candidates']))
   self.assertIn('V015_SOUTH_FACADE_HEIGHT_STUDY',r['excluded'])
 def test_v016_reference_flag(self):
  self.assertTrue(excluded({'kind':'NEW_CURVE_TYPE','excluded_from_runtime_collisions':True}))
  self.assertTrue(excluded({'kind':'REFERENCE_ONLY_NO_COLLISION'}))
 def test_unknown_fails_closed(self):
  with self.assertRaises(ValueError):excluded({'kind':'NEW_UNCLASSIFIED'})
 def test_bad_hash_refused(self):
  with tempfile.TemporaryDirectory() as t:
   m=json.loads(Path(str(WF)+'.json').read_text());m['glb_sha256']='bad';p=Path(t)/'m.json';p.write_text(json.dumps(m))
   with self.assertRaises(ValueError):export_runtime(str(WF)+'.glb',p,Path(t)/'out.glb')
 def test_unregistered_mesh_refused(self):
  with tempfile.TemporaryDirectory() as t:
   m=json.loads(Path(str(WF)+'.json').read_text());m['components'].pop();p=Path(t)/'m.json';p.write_text(json.dumps(m))
   with self.assertRaises(ValueError):export_runtime(str(WF)+'.glb',p,Path(t)/'out.glb')
if __name__=='__main__':unittest.main()
