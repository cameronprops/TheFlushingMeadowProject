"""FMP master building data contracts; run locally:
python3 -m unittest -v tests.test_master_building_index
This exercises the complete CSV->SQLite build, not a mocked catalog.
"""
import csv
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from tools.build_db import build
from tools.export_building_dossiers import export_pack
from tools.sync_master_database import source_fingerprint


class MasterBuildingIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.root=Path(cls.tmp.name)
        cls.db=cls.root/"db.sqlite"
        build(cls.db)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def con(self):
        con=sqlite3.connect(self.db)
        con.row_factory=sqlite3.Row
        return con

    def test_existing_research_not_lost(self):
        with self.con() as db:
            self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0],"ok")
            self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(),[])
            self.assertEqual(db.execute("SELECT COUNT(*) FROM reconstruction_subjects").fetchone()[0],239)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM building_dossiers").fetchone()[0],195)

    def test_master_envelopes_provenance(self):
        with self.con() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_building_envelopes").fetchone()[0],8)
            row=db.execute("SELECT * FROM master_building_envelopes WHERE building_id='WF0001'").fetchone()
            self.assertAlmostEqual(row["max_y_m"],185.928,places=3)
            self.assertEqual(row["coordinate_frame"],"SOURCE_GLB_Y_UP")
            self.assertEqual(row["evidence_status"],"SOURCE_MODEL_MEASURED")
            self.assertEqual(row["site_registered"],0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_building_envelopes WHERE site_registered=1").fetchone()[0],0)

    def test_interaction_points_do_not_invent_coordinates(self):
        with self.con() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_interactive_points").fetchone()[0],10)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_interactive_points WHERE position_status='UNLOCATED' AND x_m IS NULL AND y_m IS NULL AND z_m IS NULL").fetchone()[0],10)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_interactive_points WHERE native_unreal_tested=1").fetchone()[0],0)

    def test_media_resolves_with_archival_references(self):
        with self.con() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_media_assets").fetchone()[0],9)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_building_media").fetchone()[0],14)
            src=db.execute("SELECT uri FROM master_all_media WHERE building_id='WF0001' AND record_type='REGISTERED_FILE' AND media_kind='3D_GLB'").fetchone()
            self.assertTrue(src and "drive.google.com" in src["uri"])
            a=db.execute("SELECT COUNT(*) FROM master_all_media WHERE building_id='WF0002' AND record_type='ARCHIVE_REFERENCE'").fetchone()[0]
            self.assertGreater(a,0)
            self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(),[])

    def test_master_view_keeps_all_candidates(self):
        with self.con() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_building_overview").fetchone()[0],195)
            row=db.execute("SELECT * FROM master_building_overview WHERE building_id='WF0002'").fetchone()
            self.assertGreaterEqual(row["media_count"],4)
            self.assertGreaterEqual(row["interaction_count"],3)
            self.assertEqual(row["release_certification"],"NOT_NATIVE_ENGINE_CERTIFIED")

    def test_end_to_end_export_json_and_index(self):
        with self.con() as db:
            target=self.root/"dossiers"
            summary=export_pack(db,target)
        self.assertEqual(summary["source_model_envelopes"],8)
        self.assertEqual(summary["interactive_locations"],10)
        self.assertEqual(summary["inspected_glb_components"],696)
        self.assertEqual(summary["current_model_revisions"],4)
        self.assertGreater(summary["linked_media_references"],40)
        items=list((target/"buildings").glob("*.json"))
        self.assertEqual(len(items),195)
        trylon=json.loads((target/"buildings"/"WF0001.json").read_text())
        self.assertEqual(len(trylon["envelopes"]),2)
        self.assertGreater(len(trylon["media_inventory"]),0)
        self.assertTrue((target/"buildings"/"WF0001.md").exists())
        self.assertEqual(len(trylon["active_model_releases"]),1)
        with (target/"master_building_overview.csv").open(newline="") as stream:
            self.assertEqual(len(list(csv.DictReader(stream))),195)

    def test_real_glb_part_registry_and_surface_qa(self):
        with self.con() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_model_components").fetchone()[0],696)
            rows=dict(db.execute("SELECT building_id,COUNT(*) FROM master_model_components GROUP BY building_id"))
            self.assertEqual(rows,{"WF0001":1,"WF0002":2,"WF0014":310,"WF0020":383})
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_model_components WHERE watertight=1").fetchone()[0],656)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_model_materials WHERE building_id='WF0014'").fetchone()[0],8)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_model_components WHERE building_id='WF0020' AND watertight=0").fetchone()[0],40)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_model_components WHERE verification_status='MODEL_OBSERVED_NOT_HISTORIC_CERTIFIED'").fetchone()[0],696)
            self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(),[])

    def test_current_glb_pointer_and_dashboard(self):
        with self.con() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_active_model_releases").fetchone()[0],4)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_active_model_components").fetchone()[0],696)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM master_building_dashboard_v2").fetchone()[0],195)
            p=db.execute("SELECT * FROM master_active_model_summary WHERE building_id='WF0014'").fetchone()
            self.assertEqual(p["parts"],310)
            self.assertGreater(p["closed_parts"],0)
            view=db.execute("SELECT active_mesh_parts FROM master_building_dashboard_v2 WHERE building_id='WF0020'").fetchone()
            self.assertEqual(view["active_mesh_parts"],383)
            self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(),[])

    def test_source_fingerprint_is_reproducible(self):
        digest=source_fingerprint()
        self.assertEqual(digest,source_fingerprint())
        self.assertEqual(len(digest),64)

if __name__=="__main__":
    unittest.main()
