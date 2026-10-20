import copy
import json
import math
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from fmp_theme_solver import Catalog,TruthError,load_catalog,solve,game_manifest


class TestThemeCenterSolver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts=json.loads((ROOT/'data/master_facts.json').read_text())

    def catalog(self):
        return Catalog(copy.deepcopy(self.facts))

    def test_canonical_passes(self):
        result=solve(self.catalog())
        self.assertEqual(result['checks']['locked_facts'],'PASS')
        self.assertEqual(result['input_fact_count'],68)
        self.assertEqual(result['calculations']['trylon_plate_height_ft'],130)

    def test_sphere_placement_is_conditional(self):
        result=solve(self.catalog())
        e=result['elements'][0]
        self.assertEqual(e['geometry']['center_relative_pool_ft'],[0,0,107])
        self.assertEqual(e['geometry_status'],'VERIFIED_RADIUS_CONDITIONAL_Z')
        self.assertIsNone(game_manifest(result)['geometry_validation_overlay']['final_site_transform'])

    def test_3d_print_scale(self):
        c=solve(self.catalog())['calculations']
        self.assertAlmostEqual(c['print_perisphere_diameter_mm'],457.2)
        self.assertAlmostEqual(c['print_trylon_height_mm'],1549.4)
        self.assertAlmostEqual(c['print_helicline_developed_length_mm'],2413.0)

    def test_plate_height_corrupted_fails(self):
        facts=copy.deepcopy(self.facts)
        next(f for f in facts if f['Fact_ID']=='F010')['Value']=129
        with self.assertRaises(TruthError):solve(Catalog(facts))

    def test_no_unverified_automatic_drive(self):
        facts=copy.deepcopy(self.facts)
        next(f for f in facts if f['Fact_ID']=='F047')['Code_Drive']='YES'
        with self.assertRaises(TruthError):Catalog(facts)

    def test_bypass_with_status_change_still_blocked(self):
        facts=copy.deepcopy(self.facts)
        f=next(f for f in facts if f['Fact_ID']=='F047')
        f['Status']='VERIFIED_AS_BUILT';f['Code_Drive']='YES'
        # If source review unlocks it later, catalog may accept the fact, but
        # the v0.1 solver is deliberately not coded to use it in geometry.
        result=solve(Catalog(facts))
        bridge=next(e for e in result['elements'] if e['element_id']=='TP-BRIDGE-001')
        self.assertIsNone(bridge['geometry']['entry_elevations_ft'])

    def test_missing_facts_fail(self):
        with self.assertRaises(TruthError):Catalog(self.facts[:-1])

    def test_duplicate_ids_fail(self):
        facts=copy.deepcopy(self.facts)
        facts[1]['Fact_ID']=facts[0]['Fact_ID']
        with self.assertRaises(TruthError):Catalog(facts)

    def test_invalid_scale_fails(self):
        for denom in [0,-12,math.nan,math.inf]:
            with self.assertRaises(TruthError):solve(self.catalog(),denom)

    def test_underdetermined_no_fabrication(self):
        result=solve(self.catalog())
        bykind={e['kind']:e for e in result['elements']}
        self.assertIsNone(bykind['triangular_tower']['geometry']['base_footprint_ft'])
        self.assertIsNone(bykind['ramp']['geometry']['centerline_points_ft'])
        self.assertIsNone(bykind['ring_girder']['geometry']['elevation_ft'])
        self.assertIsNone(bykind['connecting_bridge']['geometry']['entry_elevations_ft'])

    def test_bim_ids_known(self):
        registered={item['TP_ElementID'] for item in json.loads((ROOT/'data/bim_object_register.json').read_text())}
        ids=[element['element_id'] for element in solve(self.catalog())['elements']]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(len(ids),60)
        for element_id in ids:
            self.assertIn(element_id,registered)

    def test_game_contract(self):
        game=game_manifest(solve(self.catalog()))
        self.assertAlmostEqual(game['geometry_validation_overlay']['sphere_radius_uu_cm'],2743.2)
        self.assertAlmostEqual(game['geometry_validation_overlay']['conditional_center_z_uu_cm'],3261.36)
        self.assertTrue(game['current_assembled_scene']['must_preserve_meshes_materials_source_node_ids'])
        self.assertFalse(game['engine_import_tested'])
        self.assertFalse(game['gpu_render_tested'])
        self.assertEqual(game['policy'],'PRESERVE_EXISTING_ASSEMBLY__NOT_GAME_DEV_VENDOR_APPROVED')


if __name__=='__main__':unittest.main()
