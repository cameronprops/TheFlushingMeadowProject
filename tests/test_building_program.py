"""Integration checks for FMP's source-linked building program.
Run: python3 -m unittest -v tests.test_building_program
"""
import csv
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from tools.build_db import build
from tools.export_building_dossiers import export_pack

class BuildingProgramIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="fmp_building_test_")
        cls.root = Path(cls.tmp.name)
        cls.db = cls.root/"fmp.sqlite"
        build(cls.db)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def connect(self):
        c=sqlite3.connect(self.db)
        c.row_factory=sqlite3.Row
        return c

    def test_archive_all_subjects_preserved(self):
        with self.connect() as c:
            self.assertEqual(c.execute("SELECT count(*) FROM reconstruction_subjects").fetchone()[0],239)
            self.assertEqual(c.execute("SELECT count(*) FROM archive_inventory_candidates").fetchone()[0],239)
            self.assertEqual(c.execute("PRAGMA integrity_check").fetchone()[0],"ok")

    def test_building_candidates_are_not_automatically_certified(self):
        with self.connect() as c:
            self.assertEqual(c.execute("SELECT count(*) FROM building_dossiers").fetchone()[0],195)
            self.assertEqual(c.execute("SELECT count(*) FROM building_dossiers WHERE classification='ARCHITECTURE_LISTED'").fetchone()[0],38)
            self.assertEqual(c.execute("SELECT count(*) FROM building_dossiers WHERE architecture_status='CANDIDATE_NOT_CERTIFIED'").fetchone()[0],194)
            self.assertEqual(c.execute("SELECT count(*) FROM building_dossiers WHERE classification='CONFIRMED_BUILDING'").fetchone()[0],1)

    def test_source_linkage_and_access_spaces(self):
        with self.connect() as c:
            self.assertEqual(c.execute("SELECT count(*) FROM building_details").fetchone()[0],14)
            self.assertEqual(c.execute("SELECT count(*) FROM building_evidence").fetchone()[0],37)
            self.assertEqual(c.execute("SELECT count(*) FROM building_spaces").fetchone()[0],9)
            self.assertEqual(c.execute("PRAGMA foreign_key_check").fetchall(),[])

    def test_dual_skins_share_geometry_contract(self):
        with self.connect() as c:
            rows=c.execute("SELECT building_id,count(*) AS total,count(DISTINCT variant) AS distinct_types FROM building_appearance GROUP BY building_id").fetchall()
            self.assertEqual(len(rows),195)
            self.assertTrue(all(r["total"]==2 and r["distinct_types"]==2 for r in rows))
            self.assertEqual(c.execute("SELECT count(*) FROM building_appearance WHERE shared_geometry_contract='SAME_FOOTPRINT_DOORS_COLLISION'").fetchone()[0],390)

    def test_four_public_access_pilots_not_mistaken_for_completed(self):
        with self.connect() as c:
            ids={row[0] for row in c.execute("SELECT building_id FROM building_dossiers WHERE public_access_status='INTERIOR_ALPHA_TARGET'")}
            self.assertEqual(ids,{"WF0002","WF0020","WF0009","WF0008"})
            self.assertEqual(c.execute("SELECT count(*) FROM building_spaces WHERE collision_status='NOT_TESTED'").fetchone()[0],9)

    def test_gm_both_eras_and_procedural_evidence(self):
        with self.connect() as c:
            self.assertEqual(c.execute("SELECT classification FROM building_dossiers WHERE building_id='FMP64SUBJ0064'").fetchone()[0],"CONFIRMED_BUILDING")
            self.assertEqual(c.execute("SELECT count(*) FROM building_geometry_parameters").fetchone()[0],10)
            self.assertEqual(c.execute("SELECT count(*) FROM building_surface_research").fetchone()[0],5)
            self.assertEqual(c.execute("SELECT count(*) FROM building_view_observations").fetchone()[0],6)
            self.assertEqual(c.execute("SELECT count(*) FROM unidentified_visual_leads WHERE status='MATCH_CONFIRMED' AND candidate_building_id='WF0014'").fetchone()[0],1)
            param=c.execute("SELECT value_si,units_si,evidence_class FROM building_geometry_parameters WHERE parameter_id='GM64-INDICATOR-W'").fetchone()
            self.assertAlmostEqual(param['value_si'],12.192,places=6)
            self.assertEqual(param['units_si'],'m')
            self.assertEqual(param['evidence_class'],'PERIOD_PRINTED')
            self.assertEqual(c.execute("PRAGMA foreign_key_check").fetchall(),[])

    def test_ford_rotating_exhibit_nested_not_another_pavilion(self):
        with self.connect() as c:
            row=c.execute("SELECT candidate_building_id,status,feature_motion FROM unidentified_visual_leads WHERE lead_id='FMP-VIS-ROTATING-PYRAMID-01'").fetchone()
            self.assertEqual(row['candidate_building_id'],'WF0014')
            self.assertEqual(row['status'],'MATCH_CONFIRMED')
            self.assertIn('PONTOONS',row['feature_motion'])
            self.assertEqual(c.execute("SELECT production_priority FROM building_dossiers WHERE building_id='WF0014'").fetchone()[0],'P1')
            dims=dict(c.execute("SELECT parameter_key,value_si FROM building_geometry_parameters WHERE building_id='WF0014'"))
            self.assertEqual(dims['working_models'],87)
            self.assertEqual(dims['animated_figures'],142)
            self.assertEqual(dims['raw_material_categories'],27)
            self.assertAlmostEqual(dims['diameter_hypothesis'],30.48)
            self.assertEqual(c.execute("SELECT count(*) FROM building_spaces WHERE space_id='FMP-SP-FORD-1939-CYCLE'").fetchone()[0],1)

    def test_dossier_export_consistency(self):
        with self.connect() as c:
            out=self.root/"pack"
            summary=export_pack(c,out)
            self.assertEqual(summary["research_subjects"],239)
            self.assertEqual(summary["building_candidates"],195)
            self.assertEqual(len(list((out/"buildings").glob("*.json"))),195)
            self.assertEqual(len(summary["accessible_alpha_targets"]),4)
            b=json.loads((out/"buildings"/"WF0020.json").read_text())
            self.assertEqual(len(b["source_evidence"]),5)
            self.assertEqual(len(b["interior_spaces"]),3)
            self.assertFalse(b["is_historically_certified"])
            with (out/"master_building_queue.csv").open(newline="") as f:
                self.assertEqual(len(list(csv.DictReader(f))),195)

if __name__=="__main__":
    unittest.main()
