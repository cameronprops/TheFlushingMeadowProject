import os,tempfile,unittest
from pathlib import Path
import numpy as np
import trimesh
from tools.world_build.build_helicline_transition import build,NAME
from tools.world_build.audit_helicline_join import world_mesh,vertical_surface

class TransitionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=Path(os.environ.get('FMP_THEME_CENTER_GLB','missing.glb'))
        if not cls.source.exists():raise unittest.SkipTest('Set FMP_THEME_CENTER_GLB')
        cls.temp=tempfile.TemporaryDirectory();cls.out=Path(cls.temp.name)
        cls.r=build(cls.source,cls.out)
        cls.scene=trimesh.load(cls.out/cls.r['runtime_glb'],force='scene')
        cls.original=trimesh.load(cls.source,force='scene')
        cls.mesh=world_mesh(cls.scene,NAME)
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def test_closed_exported_mesh(self):
        self.assertTrue(self.mesh.is_watertight)
        self.assertTrue(self.mesh.is_winding_consistent)
        self.assertTrue(self.r['source_unchanged'])
    def test_entry_and_exit_seams(self):
        helix=world_mesh(self.original,'Helicline_Deck_and_Curved_Soffit')
        route=world_mesh(self.scene,'PROVISIONAL_ReturnViaTrylon_04')
        entry=np.array(self.r['entry_center_m']);end=np.array(self.r['exit_center_m'])
        direction=end-entry;across=np.array([-direction[2],0,direction[0]])
        for offset in np.linspace(-1.05,1.05,85):
            p=entry+offset*across
            # Exact boundary ray tests are brittle after float32 GLB export;
            # measure actual triangle distance to each expected seam point.
            for surface in (self.mesh,route):
                _,distance,_=trimesh.proximity.closest_point_naive(surface,[p])
                self.assertLess(distance[0],1e-5)
            p=end+offset*across
            ramp=vertical_surface(helix,p[[0,2]],entry[1])
            self.assertIsNotNone(ramp)
            p[1]=ramp['surface_y_m']
            _,distance,_=trimesh.proximity.closest_point_naive(self.mesh,[p])
            self.assertLess(distance[0],.001)
    def test_interior_surface_support(self):
        helix=world_mesh(self.original,'Helicline_Deck_and_Curved_Soffit')
        entry=np.array(self.r['entry_center_m']);end=np.array(self.r['exit_center_m'])
        direction=end-entry;across=np.array([-direction[2],0,direction[0]])
        for t in np.linspace(.025,.975,20):
            for offset in np.linspace(-1.025,1.025,42):
                p=entry+t*direction+offset*across
                join=vertical_surface(self.mesh,p[[0,2]],entry[1])
                ramp=vertical_surface(helix,p[[0,2]],entry[1])
                self.assertIsNotNone(join);self.assertIsNotNone(ramp)
                self.assertGreaterEqual(join['surface_y_m']-ramp['surface_y_m'],-.001)
    def test_replacement_and_limits(self):
        self.assertEqual(sum(n=='PROVISIONAL_ReturnViaTrylon_04' for n in self.scene.graph.nodes),1)
        self.assertIn('OPEN',self.r['acceptance'])
        self.assertEqual(self.r['status'],'PROVISIONAL_RUNTIME_ONLY')
    def test_unknown_source_refused(self):
        bad=self.out/'bad.glb';bad.write_bytes(b'bad')
        with self.assertRaises(ValueError):build(bad,self.out/'bad')

if __name__=='__main__':unittest.main()
