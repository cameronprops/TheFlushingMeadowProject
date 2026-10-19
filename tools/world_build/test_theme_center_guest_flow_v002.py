"""Source-backed FMP Theme Center guest-flow tests.

Run: FMP_THEME_CENTER_GLB=/path/to/FMP_ThemeCenter_Staging_v001.glb \
      python3 -m unittest -v tools.world_build.test_theme_center_guest_flow_v002

Uses the reviewed source model and deliberately does NOT run in Unreal.
"""
import hashlib,os,tempfile,unittest
from pathlib import Path
import numpy as np
import trimesh
from tools.world_build.build_theme_center_guest_flow_v002 import (
    generate_v002,source_mesh,SOURCE_SHA,
)

SOURCE=Path(os.environ.get("FMP_THEME_CENTER_GLB","/mnt/data/FMP_ThemeCenter_Staging_v001.glb"))

class GuestFlowV002Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SOURCE.exists():raise unittest.SkipTest("Set FMP_THEME_CENTER_GLB to original model")
        cls.temp=tempfile.TemporaryDirectory()
        cls.output=Path(cls.temp.name)
        cls.report=generate_v002(SOURCE,cls.output)
        cls.scene=trimesh.load(cls.output/cls.report["output_runtime_glb"],force="scene")
        cls.cut=trimesh.load(cls.output/cls.report["output_cad_boolean_guides"],force="scene")
        cls.source=trimesh.load(SOURCE,force="scene")
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def test_01_source_hash_preserved(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(),SOURCE_SHA)
        self.assertTrue(self.report["qa"]["source_unchanged"])
    def test_02_closed_original_print_shells(self):
        for name in ("Trylon_Hollow_Exterior","Perisphere_Upper_Removable_Shell",
                     "Perisphere_Lower_Removable_Shell"):
            self.assertTrue(source_mesh(self.source,name).is_watertight)
    def test_03_runtime_open_portals(self):
        self.assertEqual(len(self.report["portals"]),2)
        self.assertFalse(source_mesh(self.scene,
            "Perisphere_Lower_Removable_Shell__UNREAL_PORTALS_v001").is_watertight)
    def test_04_separate_closed_cutter_guides(self):
        self.assertEqual(len(self.cut.geometry),2)
        self.assertTrue(all(m.is_watertight for m in self.cut.geometry.values()))
        self.assertEqual(self.report["print_booleans"],"NOT_APPLIED")
    def test_05_two_jambed_openings(self):
        for kind in ("LOWER","UPPER"):
            for item in ("HEAD","JAMB_N","JAMB_S","SILL_GUIDE"):
                self.assertIn(f"INTERPRETIVE_{kind}_PORTAL_{item}",self.scene.graph.nodes)
    def test_06_stair handrails_and_posts(self):
        for side in ("L","R"):
            self.assertIn(f"INTERPRETIVE_UPPER_EXIT_HANDRAIL_{side}",self.scene.graph.nodes)
            for i in range(9):
                self.assertTrue(source_mesh(self.scene,
                    f"INTERPRETIVE_UPPER_EXIT_POST_{side}_{i:02}").is_watertight)
        self.assertEqual(self.report["qa"]["added_nodes"],28)
    def test_07_existing_helicline_alignment(self):
        self.assertLess(self.report["qa"]["helicline_nearest_vertex_error_m"],.1)
        self.assertEqual(self.report["unreal_native_collision"],"NOT_TESTED")
    def test_08_local_to_unreal_cm_coordinates(self):
        for obj in self.report["interaction_candidates"]:
            p=np.array(obj["xyz_glb_y_up_m"])
            ue=np.array(obj["xyz_unreal_z_up_cm"])
            self.assertTrue(np.allclose(ue,p[[0,2,1]]*100,atol=.001))
            self.assertIn("NOT_HISTORICALLY_REGISTERED",obj["status"])
    def test_09_print_envelopes_are_only_dimensions(self):
        t=self.report["print_envelopes"]["Trylon"]["250"]
        sphere=self.report["print_envelopes"]["Perisphere"]["250"]
        self.assertAlmostEqual(t["envelope_mm"][1],743.712,places=1)
        self.assertAlmostEqual(sphere["envelope_mm"][0],219.426,places=1)
        self.assertFalse(t["min_wall_checked"])
    def test_10_unknown_source_rejected(self):
        source=self.output/"bad.glb"
        source.write_bytes(b"invalid glb")
        with self.assertRaisesRegex(ValueError,"Unknown original"):
            generate_v002(source,self.output/"invalid")

if __name__=="__main__":
    unittest.main()
