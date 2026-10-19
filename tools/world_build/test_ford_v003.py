#!/usr/bin/env python3
"""FMP Ford 1939 schematic v003 local acceptance suite (not host/archival tests)."""
import importlib.util
import json
import math
import sys
import unittest
from pathlib import Path
import numpy as np
import trimesh
import ezdxf

PARENT = Path(__file__).resolve().parent
SOURCE = PARENT / 'build_ford_exterior_v003.py'
if not SOURCE.is_file():
    raise RuntimeError('Place both v002 and v003 builders alongside this file')
sys.path.insert(0, str(PARENT))
from build_ford_exterior_v003 import base, make_v003, road_strip, cylinder_between, roof_ring

class FordRoadV003(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = dict(base.DEFAULTS)
        cls.s, cls.components, cls.info = make_v003(cls.p)

    def test_historic_values_are_distinct_from_calculated_spiral(self):
        self.assertAlmostEqual(self.p['turntable_diameter_m'], 100 * .3048)
        self.assertAlmostEqual(self.p['period_half_mile_car_route_m'], 804.672)
        self.assertLess(self.info['spiral_3d_length_m'], self.p['period_half_mile_car_route_m'])

    def test_ramp_grade_is_solved_from_model(self):
        p=self.p
        theoretical = 100*(p['road_z_end_m']-p['road_z_start_m'])/(2*math.pi*p['road_turns']*p['road_centerline_radius_m'])
        self.assertAlmostEqual(self.info['spiral_slope_pct'], theoretical, places=6)
        self.assertGreater(theoretical, 0)
        self.assertLess(theoretical, 8)

    def test_interlevel_vertical_clearance_derived_not_claimed(self):
        p=self.p
        z_pitch = (p['road_z_end_m']-p['road_z_start_m'])/p['road_turns']
        clear = z_pitch - p['road_structural_deck_thickness_m']
        self.assertAlmostEqual(clear, 2.5421428571428564)
        self.assertGreater(clear, 2.4)

    def test_all_derived_road_and_structural_meshes_closed(self):
        names=[n for n in self.s.geometry if n.startswith(('ROAD_THREE_TIER','ROAD_ENTRANCE','ROAD_UPPER','ROAD_STRUCTURAL','ROAD_CANTILEVER','INDUSTRIAL_HALL_INTERPRETIVE_CLOSED_ROOF'))]
        self.assertEqual(len(names), 105)
        for n in names:
            m=self.s.geometry[n]
            self.assertTrue(m.is_watertight,n)
            self.assertGreater(m.volume,0,n)
            self.assertTrue(np.isfinite(m.vertices).all(),n)

    def test_line_items_and_geometry_in_sync(self):
        self.assertEqual(len(self.s.geometry),310)
        self.assertEqual(len(self.components),310)
        self.assertEqual(len({x['id'] for x in self.components}),310)

    def test_pbr_monocork_is_not_generic_road(self):
        names=[x['material_slot'] for x in self.components if x['id'].endswith('MONOCORK_SURFACE')]
        self.assertEqual(names,['road_monocork','road_monocork','road_monocork'])

    def test_motion_remains_unverified(self):
        anim=self.info['animation']
        self.assertIsNone(anim['rpm'])
        self.assertEqual(anim['status'],'NOT_MEASURED')

    def test_dxf_file_if_built(self):
        fp=PARENT/'A103_Ford_1939_Exterior_Structure_Plan_v003.dxf'
        if not fp.exists():self.skipTest('Generate the DXF before file QA')
        doc=ezdxf.readfile(fp)
        self.assertEqual(doc.header['$INSUNITS'],6)
        self.assertEqual(len(doc.modelspace()),32)
        self.assertFalse(doc.audit().errors)

    def test_manifest_disclaims_survey_and_unreal_validation(self):
        p=PARENT/'Ford_1939_Exterior_Road_Manifest_v003.json'
        if not p.exists():self.skipTest('Generate manifest before file QA')
        m=json.loads(p.read_text())
        self.assertFalse(m['qa']['historic_geo_certified'])
        self.assertFalse(m['qa']['unreal_tested'])
        self.assertFalse(m['viewer_ready'])

if __name__ == '__main__':unittest.main()
