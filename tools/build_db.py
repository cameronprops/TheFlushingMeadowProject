"""Build SQLite search index from reviewed CSV records (Python 3.10+)."""
from __future__ import annotations
import argparse
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TABLES = {
    "eras": ("catalog/eras.csv", ("year", "label", "scene_status")),
    "places": ("catalog/places.csv", ("place_id", "name", "category", "zone",
               "year_scope", "identity_status", "geometry_status", "site_registration", "notes")),
    "sources": ("catalog/sources.csv", ("source_id", "title", "repository", "url",
                "source_type", "access_status", "rights_status", "notes")),
    "releases": ("archive/releases.csv", ("release_id", "component", "version",
                 "drive_url", "status", "notes")),
    "narrative_literature": ("catalog/narrative_literature.csv", ("literature_id", "title", "literature_type", "repository_or_author", "years", "source_url", "access_status", "rights_status", "research_subjects", "local_archive_uri", "sha256")),
    "narrative_threads": ("catalog/narrative_threads.csv", ("thread_id", "subject", "year_scope", "category", "place_id", "literature_id", "source_grounded_summary", "evidence_status", "next_action", "event_or_era_date", "fact_or_fiction")),
}

def build(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    connection = sqlite3.connect(output)
    try:
        connection.executescript((ROOT / "database/schema.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/001_narrative_tables.sql").read_text(encoding="utf-8"))
        for table, (relative, expected) in TABLES.items():
            with (ROOT / relative).open(newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                if tuple(reader.fieldnames or ()) != expected:
                    raise ValueError(f"{relative}: unexpected CSV columns {reader.fieldnames}")
                cols = ", ".join(expected)
                placeholders = ", ".join("?" for _ in expected)
                rows = [tuple((row[k] or None) for k in expected) for row in reader]
                connection.executemany(
                    f"INSERT INTO {table} ({cols}) VALUES ({placeholders})", rows
                )
                print(f"{table}: {len(rows)} rows")
        connection.commit()
        outcome = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if outcome != "ok":
            raise RuntimeError(f"SQLite integrity check failed: {outcome}")
        print(f"SQLite index built: {output}")
    except Exception:
        connection.rollback()
        if output.exists():
            output.unlink()
        raise
    finally:
        connection.close()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, default=ROOT / "out/flushing_meadows.sqlite")
    args = p.parse_args()
    build(args.output)
