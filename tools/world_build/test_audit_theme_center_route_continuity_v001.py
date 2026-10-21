"""Synthetic proofs and refusal tests; these are NOT native Unreal tests."""
import math
import unittest
import numpy as np
import trimesh
from tools.world_build.audit_theme_center_route_continuity_v001 import (
    RouteAuditError, corner_surface_certificate, straight_segment_bound, track_groups,
    validate_lineage,
)

BODY = {'radius_m': .3, 'height_m': 1.8, 'axis_cover_radius_m': math.hypot(.3, .05)}


def fake_route(*, longitudinal=0.2, clearance=.3):
    poses=[]
    for segment in range(1,5):
        for j in range(3):
            for t in (0.0, longitudinal):
                poses.append({'segment':segment,'lateral_m':(-.6,0,.6)[j],
                              'foot_xyz_m':[segment*100.0+t,0.05,j*2.0]})
    return {'poses':poses,'checked_nodes':[{'minimum_surface_clearance_m':clearance}]}


class RouteContinuityUnitTests(unittest.TestCase):
    def test_track_grid_has_twelve_groups(self):
        groups=track_groups(fake_route())
        self.assertEqual(len(groups),12)
        self.assertTrue(all(len(p)==2 for p in groups.values()))

    def test_one_lipschitz_straight_certification_positive(self):
        route=fake_route(longitudinal=.2,clearance=.3)
        report=straight_segment_bound(route,track_groups(route))
        self.assertEqual(report['edges_checked'],12)
        self.assertAlmostEqual(report['minimum_screened_obstacle_lower_bound_m'],.2)
        self.assertTrue(report['all_straight_interpolants_surface_contact_excluded'])

    def test_straight_steps_can_be_inconclusive(self):
        route=fake_route(longitudinal=.8,clearance=.3)
        r=straight_segment_bound(route,track_groups(route))
        self.assertFalse(r['all_straight_interpolants_surface_contact_excluded'])

    def test_empty_scene_is_surface_clear(self):
        r=corner_surface_certificate(trimesh.Scene(),[-1,.05,0],[1,.05,0],BODY,subdivisions=8)
        self.assertTrue(r['surface_contact_excluded'])
        self.assertEqual(r['candidate_triangles'],0)
        self.assertIsNone(r['candidate_min_lipschitz_lower_bound_m'])

    def test_distant_obstacle_is_excluded_by_broad_phase(self):
        scene=trimesh.Scene()
        cube=trimesh.creation.box(extents=[.2,2,.2])
        cube.apply_translation([12,1,0])
        scene.add_geometry(cube,node_name='distant_box')
        r=corner_surface_certificate(scene,[-1,.05,0],[1,.05,0],BODY,subdivisions=8)
        self.assertTrue(r['surface_contact_excluded'])
        self.assertEqual(r['candidate_triangles'],0)

    def test_midway_crossing_detected(self):
        scene=trimesh.Scene()
        cube=trimesh.creation.box(extents=[.1,2,.4])
        cube.apply_translation([0,.8,0])
        scene.add_geometry(cube,node_name='crossing_box')
        r=corner_surface_certificate(scene,[-1,.05,0],[1,.05,0],BODY,subdivisions=8)
        self.assertFalse(r['surface_contact_excluded'])
        self.assertLessEqual(r['candidate_min_lipschitz_lower_bound_m'],0)

    def test_subdivision_refinement_converts_inconclusive_floor_margin_to_pass(self):
        # A floor 5cm beneath the capsule toe has small positive separation.
        scene=trimesh.Scene()
        box=trimesh.creation.box(extents=[3,.2,3])
        box.apply_translation([0,-.1,0])
        scene.add_geometry(box,node_name='floor')
        a,b=[0,.05,0],[.84865,.05,0]
        rough=corner_surface_certificate(scene,a,b,BODY,subdivisions=8)
        fine=corner_surface_certificate(scene,a,b,BODY,subdivisions=16)
        self.assertFalse(rough['surface_contact_excluded'])
        self.assertTrue(fine['surface_contact_excluded'])

    def test_invalid_subdivision_rejected(self):
        with self.assertRaisesRegex(RouteAuditError,'subdivisions'):
            corner_surface_certificate(trimesh.Scene(),[0,0,0],[1,0,0],BODY,subdivisions=0)

    def test_changed_body_axis_cover_rejected(self):
        bad={**BODY,'axis_cover_radius_m':.25}
        with self.assertRaisesRegex(RouteAuditError,'Axis-cover'):
            corner_surface_certificate(trimesh.Scene(),[0,.05,0],[.5,.05,0],bad)

    def test_hash_refusal_before_geometry(self):
        from pathlib import Path
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source.glb';p.write_bytes(b'NOT THE EXPECTED GLB')
            with self.assertRaisesRegex(RouteAuditError, 'GLB SHA-256'):
                validate_lineage({}, {}, p)


if __name__=='__main__':
    unittest.main()
