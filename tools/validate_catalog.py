"""Minimal catalog QA, intentionally without third-party dependencies."""
import csv
from pathlib import Path
from build_db import ROOT, TABLES

# Header-only tables remain empty until dated, evidenced coordinates or links exist.
# Their schemas are still checked; all other catalog tables require real rows.
ALLOW_SCHEMA_ONLY = {
    "catalog/atlas_placement_reviews.csv",
    "catalog/atlas_placements.csv",
    "catalog/atlas_world_frames.csv",
    "catalog/horticulture_irrigation_links.csv",
    "catalog/horticulture_plant_instances.csv",
    "catalog/site_amenity_era_relations.csv",
    "catalog/site_individual_plants.csv",
    "catalog/site_network_era_relations.csv",
    "catalog/site_network_nodes.csv",
    "catalog/site_plant_era_relations.csv",
    "catalog/site_planting_schedules.csv",
}

def main() -> None:
    for table, (relative, expected) in TABLES.items():
        path = ROOT / relative
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            assert tuple(reader.fieldnames or ()) == expected, f"{relative}: bad columns"
            rows = list(reader)
        assert rows or relative in ALLOW_SCHEMA_ONLY, f"{relative}: no rows"
        pk = expected[0]
        keys = [row[pk] for row in rows]
        assert all(keys), f"{relative}: missing {pk}"
        assert len(set(keys)) == len(keys), f"{relative}: duplicate {pk}"
        print(f"PASS {relative}: {len(rows)} unique rows" + (" (schema-only)" if not rows else ""))
    with (ROOT / "catalog/eras.csv").open(newline="", encoding="utf-8") as file:
        years = {int(r["year"]) for r in csv.DictReader(file)}
    assert years == {1939,1940,1964,1965,2026}, f"era mismatch: {years}"
    print("PASS five-era coverage")

if __name__ == "__main__":
    main()
