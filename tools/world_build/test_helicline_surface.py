import unittest
import numpy as np
import trimesh
from tools.world_build.audit_helicline_join import vertical_surface

class SurfaceTest(unittest.TestCase):
    def test_sloped_triangle_interpolation(self):
        m=trimesh.Trimesh(vertices=[[0,0,0],[0,1,1],[1,0,0]],faces=[[0,1,2]],process=False)
        hit=vertical_surface(m,[.25,.25],.5)
        self.assertAlmostEqual(hit['surface_y_m'],.25)
        self.assertAlmostEqual(hit['drop_from_route_m'],.25)
        self.assertIsNone(vertical_surface(m,[2,2],.5))
    def test_soffit_is_excluded(self):
        m=trimesh.Trimesh(vertices=[[0,0,0],[1,0,0],[0,0,1]],faces=[[0,1,2]],process=False)
        self.assertIsNone(vertical_surface(m,[.1,.1],.5))
    def test_near_level_selected_and_remote_surface_excluded(self):
        m=trimesh.creation.box(extents=[2,.2,2])
        self.assertAlmostEqual(vertical_surface(m,[0,0],.2)['surface_y_m'],.1)
        self.assertIsNone(vertical_surface(m,[0,0],5))
    def test_vertical_face_and_shared_edge(self):
        m=trimesh.creation.box(extents=[2,.2,2])
        self.assertIsNotNone(vertical_surface(m,[1,1],.2))
        self.assertIsNone(vertical_surface(m,[1.1,0],.2))

if __name__=='__main__': unittest.main()
