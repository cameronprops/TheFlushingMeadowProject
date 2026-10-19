"""Shell-first extraction tests. Optional original GLB from FMP_THEME_CENTER_SOURCE_GLB."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np
import trimesh
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_shell_kit import build,print_mesh,group_for,SOURCE_HASH,sha256
SOURCE=Path(os.environ.get("FMP_THEME_CENTER_SOURCE_GLB","/mnt/data/FMP_ThemeCenter_Staging_v001.glb"))
class ShellKitTests(unittest.TestCase):
 def test_source_hash_if_available(self):
  if not SOURCE.exists():self.skipTest("Set FMP_THEME_CENTER_SOURCE_GLB to original staging GLB")
  self.assertEqual(sha256(SOURCE),SOURCE_HASH)
 def test_role_mapping(self):
  self.assertEqual(group_for("Trylon_Hollow_Exterior"),"EXTERIOR_SHELL")
  self.assertEqual(group_for("Interior_Projection_Liner"),"INTERIOR_SHELL_AND_VIEWING")
  self.assertEqual(group_for("Helicline_Deck_and_Curved_Soffit"),"GUEST_CIRCULATION_PREVIEW")
  self.assertEqual(group_for("Trylon_Face_1_Frame"),"OPTIONAL_STEEL_STRUCTURE")
  self.assertIsNone(group_for("DEMOCRACITY_CHILD"))
 def test_scaled_z_up(self):
  scaled=print_mesh(trimesh.creation.box(extents=(1,2,3)),100)
  np.testing.assert_allclose(scaled.extents,[10,30,20])
  self.assertAlmostEqual(scaled.bounds[0,2],0)
  self.assertTrue(scaled.is_volume)
 def test_nonwatertight_rejected(self):
  mesh=trimesh.creation.box()
  mesh.update_faces(np.arange(1,len(mesh.faces)))
  with self.assertRaises(ValueError):print_mesh(mesh,800)
 def test_original_source_and_all_print_parts(self):
  if not SOURCE.exists():self.skipTest("GLB retained outside GitHub; set env var")
  with tempfile.TemporaryDirectory() as d:
   report=build(SOURCE,Path(d))
   self.assertEqual(report["original_source_nodes"],510)
   self.assertEqual(report["layer_counts"],{"EXTERIOR_SHELL":3,"INTERIOR_SHELL_AND_VIEWING":10,"GUEST_CIRCULATION_PREVIEW":5,"OPTIONAL_STEEL_STRUCTURE":60})
   self.assertEqual(len(report["print_parts"]),7)
   self.assertTrue(all(p["is_watertight"] and p["is_volume"] for p in report["print_parts"]))
   self.assertTrue(all(not p["minimum_wall_thickness_checked"] for p in report["print_parts"]))
   self.assertTrue(report["source_unmodified"])
if __name__=="__main__":unittest.main()
