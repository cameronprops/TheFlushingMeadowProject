"""Hermetic tests for evidence-only Theme Center registration controls."""
from pathlib import Path
import importlib.util,tempfile,unittest
import numpy as np
import trimesh

spec=importlib.util.spec_from_file_location('rig',Path(__file__).with_name('build_bridge_registration_controls_v001.py'))
rig=importlib.util.module_from_spec(spec);spec.loader.exec_module(rig)

class TestPhotoRegistrationRig(unittest.TestCase):
 def test_box_has_twelve_edges(self):
  edges=rig.bbox_segments(np.array([[1,2,3],[4,6,8.]]))
  self.assertEqual(len(edges),12)
  self.assertTrue(all(np.sum(a!=b)==1 for a,b in edges))
 def test_world_transform_is_respected(self):
  scene=trimesh.Scene();name='test-geometry'
  scene.add_geometry(trimesh.creation.box(extents=(2,4,6)),node_name=name,geom_name=name,transform=trimesh.transformations.translation_matrix([10,20,30]))
  b=rig.transformed_bounds(scene,name)
  np.testing.assert_allclose(b,[[9,18,27],[11,22,33]])
 def test_guides_are_finite_and_registered(self):
  bounds=[[0,1,2],[3,4,5]]
  guide=rig.guide_node(bounds,(20,30,40,255))
  self.assertTrue(np.isfinite(guide.vertices).all())
  self.assertEqual(guide.bounds.shape,(2,3))
  self.assertTrue(np.allclose(guide.bounds[0],np.array(bounds[0]),atol=.031))
  self.assertTrue(np.allclose(guide.bounds[1],np.array(bounds[1]),atol=.031))
 def test_invalid_hash_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'mock.glb';p.write_bytes(b'not the verified GLB')
   with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):rig.build(p,Path(d)/'output')
 def test_missing_node_refused(self):
  scene=trimesh.Scene()
  with self.assertRaisesRegex(ValueError,'Missing source node'):rig.transformed_bounds(scene,'not-present')
 def test_all_controls_are_existing_nodes_not_architectural_designs(self):
  self.assertEqual(len(rig.NODES),6)
  self.assertNotIn('Bridge_Arched_Underside',rig.NODES.values())
  self.assertNotIn('Perisphere_Entrance_Canopy',rig.NODES.values())
if __name__=='__main__':unittest.main()
