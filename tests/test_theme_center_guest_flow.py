"""Source-backed Theme Center circulation tests. Run from FMP clone root:
FMP_THEME_CENTER_GLB=/path/to/FMP_ThemeCenter_Staging_v001.glb \
 python3 -m unittest -v tests.test_theme_center_guest_flow
"""
import hashlib,os,tempfile,unittest
from pathlib import Path
import trimesh
from tools.world_build.build_theme_center_guest_flow_v001 import generate,SOURCE_SHA

SOURCE=Path(os.environ.get('FMP_THEME_CENTER_GLB','/mnt/data/FMP_ThemeCenter_Staging_v001.glb'))

class ThemeCenterGuestRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SOURCE.exists():
            raise unittest.SkipTest('Set FMP_THEME_CENTER_GLB to original 510-node FMP model')
        cls.temp=tempfile.TemporaryDirectory()
        cls.record=generate(SOURCE,cls.temp.name)
        cls.scene=trimesh.load(Path(cls.temp.name)/cls.record['unreal_overlay'],force='scene')
    @classmethod
    def tearDownClass(cls): cls.temp.cleanup()
    def test_original_source_unchanged(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(),SOURCE_SHA)
        self.assertTrue(self.record['source_unchanged'])
    def test_two_openings_and_upper_exit_stairs(self):
        self.assertEqual(self.record['removed_source_triangles'],216)
        self.assertEqual(self.record['stairs']['count'],23)
        self.assertEqual(self.record['portals']['count'],2)
        self.assertEqual(len([n for n in self.scene.graph.nodes if n.startswith('PROVISIONAL_UpperReturnStair_')]),23)
    def test_runtime_not_print_shell(self):
        self.assertIn('Perisphere_Lower_Removable_Shell',self.record['keep_printing_source_nodes'])
        altered=next(n for n in self.scene.graph.nodes if 'UNREAL_PORTALS' in n)
        self.assertFalse(self.scene.geometry[self.scene.graph[altered][1]].is_watertight)
    def test_does_not_invent_historical_portal_data(self):
        self.assertFalse(self.record['site_registered'])
        self.assertEqual(self.record['certification'],'RECONSTRUCTION_PREVIEW_ONLY')
        self.assertEqual(self.record['portals']['status'],'INTERPRETIVE_NOT_AS_BUILT')

if __name__=='__main__':unittest.main()
