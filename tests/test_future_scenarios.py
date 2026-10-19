"""Verify that alternative futures never contaminate documented historical eras."""
import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from build_db import build

class FutureScenarioTests(unittest.TestCase):
    def test_branch_and_year_separation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"fmp.sqlite"
            build(path)
            with sqlite3.connect(path) as c:
                self.assertEqual({r[0] for r in c.execute("SELECT year FROM eras")}, {1939,1940,1964,1965,2026})
                rows=list(c.execute("SELECT branch_id, year, scenario_class, canonical, status FROM future_scenarios ORDER BY branch_id, year"))
                self.assertEqual(len(rows),4)
                self.assertEqual({(r[0],r[1]) for r in rows}, {
                    ("NEW_FAIR",2039),("NEW_FAIR",2064),
                    ("DECLINE",2039),("DECLINE",2064)})
                self.assertTrue(all(r[3] == 0 and r[4]=="CONCEPT" for r in rows))
                self.assertEqual({r[2] for r in rows if r[0]=="NEW_FAIR"},{"UTOPIAN"})
                self.assertEqual({r[2] for r in rows if r[0]=="DECLINE"},{"DYSTOPIAN"})

if __name__ == "__main__":
    unittest.main()
