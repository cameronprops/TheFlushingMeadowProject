"""Source-gated FMP historic paths and utilities. Run:
python3 -m unittest -v tests.test_site_networks
"""
import sqlite3
import tempfile
import unittest
from pathlib import Path
from tools.build_db import build

class DatedSiteNetworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(prefix='fmp_network_')
        cls.db=Path(cls.tmp.name)/'site.db'
        build(cls.db)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def connect(self):
        c=sqlite3.connect(self.db);c.row_factory=sqlite3.Row
        return c
    def test_all_research_records_retained(self):
        with self.connect() as c:
            self.assertEqual(c.execute('SELECT COUNT(*) FROM building_dossiers').fetchone()[0],195)
            self.assertEqual(c.execute('SELECT COUNT(*) FROM site_network_layers').fetchone()[0],19)
            self.assertGreaterEqual(c.execute('SELECT COUNT(*) FROM site_network_sheets').fetchone()[0],68)
            self.assertEqual(c.execute('SELECT COUNT(*) FROM site_network_features').fetchone()[0],19)
            self.assertEqual(c.execute('SELECT COUNT(*) FROM site_network_segments').fetchone()[0],19)
            self.assertEqual(c.execute('PRAGMA foreign_key_check').fetchall(),[])
    def test_utilities_are_distinct_layers(self):
        with self.connect() as c:
            got={r['medium'] for r in c.execute("SELECT medium FROM site_network_layers WHERE family='UTILITY'")}
            for t in ('POTABLE_WATER_MAIN','BUILDING_WATER_LATERAL','SANITARY_SEWER','STORM_DRAIN',
                      'GAS_MAIN','TELEPHONE_TV_CONDUIT','FOUNTAIN_PUMP_PIPING'):
                self.assertIn(t,got)
    def test_not_invented_as_drawn_site_lines(self):
        with self.connect() as c:
            self.assertEqual(c.execute('SELECT COUNT(*) FROM site_walkable_edges').fetchone()[0],0)
            self.assertEqual(c.execute('SELECT COUNT(*) FROM site_network_segments WHERE geojson_geometry IS NOT NULL').fetchone()[0],0)
            self.assertEqual(c.execute('SELECT COUNT(*) FROM site_network_nodes').fetchone()[0],0)
    def test_sheet_1964_water_sewage_storm(self):
        with self.connect() as c:
            for layer in ('FMP_UTIL_POTABLE','FMP_UTIL_SANITARY','FMP_UTIL_STORM'):
                count=c.execute('SELECT COUNT(*) FROM site_network_sheets WHERE era_year=1964 AND primary_layer=?',(layer,)).fetchone()[0]
                self.assertGreaterEqual(count,3)
    def test_named_roads_source_linked(self):
        with self.connect() as c:
            x=c.execute("SELECT * FROM site_network_segments WHERE historical_name='Constitution Mall'").fetchone()
            self.assertIsNotNone(x)
            self.assertEqual(x['era_year'],1939)
            self.assertEqual(x['alignment_status'],'UNTRACED')
            self.assertFalse(x['navigable'])
    def test_date_view_has_separate_eras(self):
        with self.connect() as c:
            self.assertEqual(len(c.execute('SELECT * FROM site_network_progress').fetchall()),5)
            self.assertGreater(c.execute('SELECT cataloged_sheets FROM site_network_progress WHERE era_year=1939').fetchone()[0],1)
            self.assertGreater(c.execute('SELECT cataloged_sheets FROM site_network_progress WHERE era_year=1964').fetchone()[0],1)
    def test_wrong_era_connection_refused(self):
        with self.connect() as c:
            c.execute("""INSERT INTO site_network_nodes
              (node_id,era_year,layer_id,name,location_status)
              VALUES ('TEST-1964-ACCESS',1964,'FMP_PATH_PEDESTRIAN','Synthetic','UNLOCATED')""")
            with self.assertRaises(sqlite3.IntegrityError):
                c.execute("""INSERT INTO site_network_segments
                  (segment_id,feature_id,era_year,layer_id,historical_name,
                   from_node_id,alignment_status,access_class)
                  VALUES ('TEST-BAD-ERA','NR1939-CONSTITUTION',1939,
                  'FMP_PATH_PEDESTRIAN','Wrong year','TEST-1964-ACCESS','UNTRACED','UNKNOWN')""")
            c.rollback()
    def test_cross_era_requires_order(self):
        with self.connect() as c:
            c.execute("""INSERT INTO site_network_segments
              (segment_id,feature_id,era_year,layer_id,alignment_status,access_class)
              VALUES ('TEST-65','NR1964-PROGRESS',1965,'FMP_PATH_STREET','UNTRACED','UNKNOWN')""")
            with self.assertRaises(sqlite3.IntegrityError):
                c.execute("""INSERT INTO site_network_era_relations
                  (relation_id,earlier_segment_id,later_segment_id,relation_type,confidence)
                  VALUES ('BAD','TEST-65','SEG-NR1964-PROGRESS-1964','POSSIBLE_LINK','UNVERIFIED')""")
            c.rollback()
    def test_no_certified_cross_era_links_without_evidence(self):
        with self.connect() as c:
            c.execute("""INSERT INTO site_network_segments
              (segment_id,feature_id,era_year,layer_id,alignment_status,access_class)
              VALUES ('TEST-65','NR1964-PROGRESS',1965,'FMP_PATH_STREET','UNTRACED','UNKNOWN')""")
            with self.assertRaises(sqlite3.IntegrityError):
                c.execute("""INSERT INTO site_network_era_relations
                  (relation_id,earlier_segment_id,later_segment_id,relation_type,confidence)
                  VALUES ('BAD','SEG-NR1964-PROGRESS-1964','TEST-65','ALIGNMENT_PERSISTED','VERIFIED')""")
            c.rollback()
if __name__=='__main__':unittest.main()
