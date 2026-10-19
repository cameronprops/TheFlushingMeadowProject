"""FMP historical horticulture database and sourced plant-placement tests.
Run: python3 -m unittest -v tests.test_horticulture
Requires a full Git checkout; no external services or paid actions.
"""
import csv
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from tools.build_db import build
from tools.site.export_horticulture import export_horticulture

class HistoricalHorticultureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(prefix='fmp_horticulture_')
        cls.path=Path(cls.tmp.name)/'master.sqlite'
        build(cls.path)
    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()
    def connect(self):
        con=sqlite3.connect(self.path)
        con.row_factory=sqlite3.Row
        con.execute("PRAGMA foreign_keys=ON")
        return con

    def test_master_database_preserved(self):
        with self.connect() as db:
            self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0],"ok")
            self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(),[])
            self.assertEqual(db.execute("SELECT COUNT(*) FROM building_dossiers").fetchone()[0],195)

    def test_sources_garden_taxa_and_events(self):
        with self.connect() as db:
            wanted=[('horticulture_sources',19),('horticulture_taxa',10),
                    ('horticulture_areas',20),('horticulture_plantings',11),
                    ('horticulture_seasonal_events',5),('horticulture_era_links',2)]
            for table,count in wanted:
                with self.subTest(table=table):
                    self.assertEqual(db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0],count)

    def test_rose_quantity_correctly_scoped(self):
        with self.connect() as db:
            p=db.execute("SELECT * FROM horticulture_plantings WHERE planting_id='PL39-GOP-ROSES'").fetchone()
            self.assertEqual(p["quantity"],8000)
            self.assertEqual(p["variety_count"],250)
            self.assertEqual(p["quantity_basis"],"PLANTS_IN_THIS_AREA")
            self.assertEqual(p["era_year"],1939)

    def test_1940_living_stamp_not_invented_for_1939(self):
        with self.connect() as db:
            names={x["scientific_name"] for x in db.execute("""
             SELECT t.scientific_name FROM horticulture_plantings p
             JOIN horticulture_taxa t ON t.taxon_id=p.taxon_id
             WHERE p.area_id='HORT40-LIVINGSTAMP'""")}
            self.assertEqual(names,{"Alternanthera","Sedum"})
            self.assertEqual(db.execute("""
                SELECT COUNT(*) FROM horticulture_plantings
                WHERE era_year=1939 AND area_id LIKE '%LIVINGSTAMP%'""").fetchone()[0],0)

    def test_1964_400_trees_not_allocated_per_species(self):
        with self.connect() as db:
            a=db.execute("SELECT * FROM horticulture_plantings WHERE planting_id='PL64-400-TREES'").fetchone()
            self.assertEqual(a["quantity"],400)
            self.assertEqual(a["installation_status"],"CONTRACTED_NOT_VERIFIED_INSTALLED")
            self.assertEqual(a["quantity_basis"],"PROJECT_WIDE_CONTRACT")
            for id in ('PL64-MAPLE','PL64-LOCUST'):
                self.assertIsNone(db.execute(
                    "SELECT quantity FROM horticulture_plantings WHERE planting_id=?",(id,)).fetchone()[0])

    def test_nippon_planting_plan_only_not_species_fiction(self):
        with self.connect() as db:
            zone=db.execute("SELECT * FROM horticulture_areas WHERE area_id='HORT39-JAPANESE'").fetchone()
            self.assertEqual(zone["location_status"],"NAMED_AREA_ONLY")
            self.assertEqual(db.execute("SELECT COUNT(*) FROM horticulture_plantings WHERE area_id='HORT39-JAPANESE'").fetchone()[0],0)
            self.assertIn("15.3",db.execute("SELECT archive_locator FROM horticulture_sources WHERE source_id='HORT39-LIU-NIPPON-15-3'").fetchone()[0])

    def test_unregistered_gardens_have_no_fabricated_polygons(self):
        with self.connect() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM horticulture_mapped_areas").fetchone()[0],0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM horticulture_areas WHERE local_polygon_geojson IS NOT NULL").fetchone()[0],0)

    def test_cross_era_trees_not_claimed_as_individual_survivors(self):
        with self.connect() as db:
            row=db.execute("SELECT * FROM horticulture_era_links WHERE link_id='HLINK-ROWS-39-64'").fetchone()
            self.assertEqual(row["relation_type"],"TREES_RETAINED")
            self.assertEqual(row["certainty"],"RESEARCH_SUPPORTED")

    def test_false_year_planting_rejected(self):
        with self.connect() as db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("""INSERT INTO horticulture_plantings
                (planting_id,era_year,area_id,source_id,display_label,
                 planting_role,installation_status,quantity_basis)
                VALUES ('BAD-1939',1939,'HORT40-LIVINGSTAMP','HORT39-QBG-HISTORY',
                'false species','BEDDING','INSTALLED_DESCRIBED','UNKNOWN')""")
            db.rollback()

    def test_false_mapped_garden_without_geometry_rejected(self):
        with self.connect() as db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("UPDATE horticulture_areas SET location_status='MAP_TRACED' WHERE area_id='HORT39-JAPANESE'")
            db.rollback()

    def test_export_refuses_fake_map_positions(self):
        with self.connect() as db:
            output=Path(self.tmp.name)/'output'
            report=export_horticulture(db,output)
        self.assertEqual(report['planting_observations'],11)
        self.assertEqual(report['dated_garden_areas'],20)
        self.assertEqual(report['site_registered_or_traced_areas'],0)
        z=json.loads((output/'mapped_gardens_local.json').read_text())
        self.assertEqual(z['areas'],[])
        with (output/'planting_schedule.csv').open(newline='') as f:
            self.assertEqual(len(list(csv.DictReader(f))),11)
        with (output/'source_acquisition_queue.csv').open(newline='') as f:
            self.assertEqual(len(list(csv.DictReader(f))),19)

if __name__=='__main__': unittest.main()
