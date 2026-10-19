"""Run with: python -m unittest discover -s tests -v."""
import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from build_db import build

class CatalogRoundTrip(unittest.TestCase):
    def test_sqlite_integrity(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / "fair.sqlite"
            build(p)
            self.assertTrue(p.exists())
            connection = sqlite3.connect(p)
            try:
                self.assertEqual(connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")
                years = {row[0] for row in connection.execute("SELECT year FROM eras")}
                self.assertEqual(years, {1939, 1940, 1964, 1965, 2026})
                self.assertGreater(connection.execute("SELECT count(*) FROM places").fetchone()[0], 0)
                self.assertGreater(connection.execute("SELECT count(*) FROM sources").fetchone()[0], 0)
            finally:
                connection.close()

if __name__ == "__main__":
    unittest.main()
