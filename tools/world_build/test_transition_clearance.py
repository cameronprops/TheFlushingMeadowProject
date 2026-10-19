import unittest
import numpy as np
import trimesh
from tools.world_build.audit_transition_clearance import sphere_screen
class ScreenTest(unittest.TestCase):
    def test_wall_collision_and_separation(self):
        wall=trimesh.creation.box(extents=[.1,3,3])
        distances=sphere_screen(wall,np.array([[.2,0,0],[1,0,0]]),.3)
        self.assertAlmostEqual(distances[0],-.15)
        self.assertAlmostEqual(distances[1],.65)
    def test_transformed_obstacle(self):
        wall=trimesh.creation.box(extents=[.1,3,3]);wall.apply_translation([5,0,0])
        self.assertLess(sphere_screen(wall,np.array([[5.2,0,0]]),.3)[0],0)
    def test_tangent_and_batch_boundary(self):
        wall=trimesh.creation.box(extents=[.1,3,3])
        d=sphere_screen(wall,np.tile([.35,0,0],(65,1)),.3)
        self.assertTrue(np.allclose(d,0,atol=1e-12))
    def test_documented_containment_limit(self):
        box=trimesh.creation.box(extents=[4,4,4])
        self.assertGreater(sphere_screen(box,np.array([[0,0,0]]),.3)[0],0)
if __name__=='__main__':unittest.main()
