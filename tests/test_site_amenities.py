"""Regression suite for dated refuse, benches, luminaire, fountains and public facilities.
Run locally: python3 -m unittest -v tests.test_site_amenities
Requires full source checkout with SQLite standard library only.
"""
from __future__ import annotations
import csv
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from tools.build_db import build
from tools.site.export_site_amenities import export_site_amenities

class SiteAmenitiesIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(prefix="fmp_amenities_")
        cls.root=Path(cls.tmp.name)
        cls.db=cls.root/"site.sqlite"
        build(cls.db)
    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()
    def connect(self):
        con=sqlite3.connect(self.db)
        con.row_factory=sqlite3.Row
        con.execute("PRAGMA foreign_keys=ON")
        return con
    def test_preserves_building_inventory_and_archive(self):
        with self.connect() as db:
            self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0],"ok")
            self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(),[])
            self.assertEqual(db.execute("SELECT COUNT(*) FROM building_dossiers").fetchone()[0],195)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM reconstruction_subjects").fetchone()[0],239)
    def test_documented_archival_types(self):
        with self.connect() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM site_amenity_categories").fetchone()[0],23)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM site_amenity_types").fetchone()[0],32)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM site_amenity_evidence").fetchone()[0],56)
            for t in ("AMT39-REFUSE","AMT39-DRINK","AMT39-BENCH",
                      "AMT39-WASHINGTON","AMT39-MANSHIP","AMT64-FOUNTAINPLANETS",
                      "AMT64-POLES","AMT64-TOILET","AMT64-DRINK"):
                self.assertEqual(db.execute("SELECT COUNT(*) FROM site_amenity_types WHERE type_id=?",(t,)).fetchone()[0],1)
            for sh in ("OPS64-08","OPS64-09","OPS64-10","OPS64-57",
                       "NYPL39-238-26","NYPL39-275-11","NYPL39-275-18"):
                self.assertIsNotNone(db.execute("SELECT sheet_id FROM site_network_sheets WHERE sheet_id=?",(sh,)).fetchone())
    def test_named_area_not_fabricated_gps(self):
        with self.connect() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM site_amenity_instances").fetchone()[0],6)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM site_amenity_map_points").fetchone()[0],0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM site_amenity_instances WHERE longitude IS NOT NULL OR x_m IS NOT NULL").fetchone()[0],0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM site_amenity_instances WHERE position_status='NAMED_AREA_ONLY'").fetchone()[0],6)
    def test_service_link_is_not_historically_certified(self):
        with self.connect() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM site_amenity_service_links").fetchone()[0],2)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM site_amenity_service_links WHERE linkage_status='DOCUMENTED'").fetchone()[0],0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM site_amenity_era_relations").fetchone()[0],0)
            self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(),[])
    def test_false_cross_year_instance_rejected(self):
        with self.connect() as db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("""INSERT INTO site_amenity_instances
                    (instance_id,type_id,era_year,position_status)
                    VALUES ('SYN-BAD-YEAR','AMT39-BENCH',1964,'UNLOCATED')""")
            db.rollback()
    def test_false_mapped_instance_rejected(self):
        with self.connect() as db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("""INSERT INTO site_amenity_instances
                    (instance_id,type_id,era_year,position_status,
                     x_m,y_m,z_m,coordinate_frame)
                    VALUES ('SYN-BAD-MAP','AMT39-BENCH',1939,'MAP_TRACED',
                            1,2,0,'LOCAL_METRES')""")
            db.rollback()
    def test_false_certified_service_rejected(self):
        with self.connect() as db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("""INSERT INTO site_amenity_service_links
                   (service_link_id,instance_id,network_layer_id,service_kind,linkage_status)
                   VALUES ('SYN-BAD-SERVICE','SITE64-PLANETS','FMP_UTIL_FOUNTAIN',
                           'FAKE_PIPE','GEOREGISTERED')""")
            db.rollback()
    def test_period_inversion_rejected(self):
        with self.connect() as db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("""INSERT INTO site_amenity_era_relations
                  (relation_id,earlier_instance_id,later_instance_id,relation_type,certainty)
                  VALUES ('SYN-BAD-ERA','SITE64-PLANETS','SITE39-GW',
                         'POSSIBLE_RELATION','UNVERIFIED')""")
            db.rollback()
    def test_export_no_fabricated_geojson(self):
        with self.connect() as db:
            summary=export_site_amenities(db,self.root/"export")
        self.assertEqual(summary["typologies"],32)
        self.assertEqual(summary["source_observations"],56)
        self.assertEqual(summary["named_area_only_instances"],6)
        self.assertEqual(summary["geodetically_registered_wgs84_points"],0)
        self.assertFalse(summary["complete_spatial_map"])
        doc=json.loads((self.root/"export"/"verified_points_wgs84.geojson").read_text())
        self.assertEqual(doc["features"],[])
        guide=json.loads((self.root/"export"/"named_area_landmarks.json").read_text())
        self.assertEqual(len(guide["features"]),6)
        with (self.root/"export"/"research_queue.csv").open(newline="") as f:
            self.assertEqual(len(list(csv.DictReader(f))),32)

if __name__=="__main__":unittest.main()
