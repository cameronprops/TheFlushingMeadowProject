"""Minimal catalog QA, intentionally without third-party dependencies."""
import csv
from pathlib import Path
from build_db import ROOT, TABLES

def main() -> None:
    for table, (relative, expected) in TABLES.items():
        path = ROOT / relative
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            assert tuple(reader.fieldnames or ()) == expected, f"{relative}: bad columns"
            rows = list(reader)
        assert rows, f"{relative}: no rows"
        pk = expected[0]
        keys = [row[pk] for row in rows]
        assert all(keys), f"{relative}: missing {pk}"
        assert len(set(keys)) == len(keys), f"{relative}: duplicate {pk}"
        print(f"PASS {relative}: {len(rows)} unique rows")
    with (ROOT / "catalog/eras.csv").open(newline="", encoding="utf-8") as file:
        years = {int(r["year"]) for r in csv.DictReader(file)}
    assert years == {1939,1940,1964,1965,2026}, f"era mismatch: {years}"
    print("PASS five-era coverage")

if __name__ == "__main__":
    main()
