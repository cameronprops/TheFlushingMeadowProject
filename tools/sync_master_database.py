#!/usr/bin/env python3
"""FMP Master DB: rebuild once or auto-refresh while this program is running.

No paid GitHub Actions, hosted services, or background job implied.
CSV/SQL source files in Git are canonical; SQLite and JSON/MD are generated.

Run from repo root:
  python3 tools/sync_master_database.py --once
  python3 tools/sync_master_database.py --watch --interval 3
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.build_db import build
from tools.export_building_dossiers import export_pack
from tools.building_program.export_runtime_handoff import export as export_runtime_handoff
from tools.building_program.refresh_model_catalog import refresh_registered_models
WATCH_GLOBS = (
    "catalog/*.csv",
    "archive/*.csv",
    "database/schema.sql",
    "database/migrations/*.sql",
    "tools/build_db.py",
    "tools/export_building_dossiers.py",
    "tools/building_program/export_runtime_handoff.py",
    "tools/sync_master_database.py",
)

def watched_files(root: Path = ROOT):
    paths = {p for pattern in WATCH_GLOBS for p in root.glob(pattern) if p.is_file()}
    return sorted(paths)

def source_fingerprint(root: Path = ROOT) -> str:
    """Strong deterministic content checksum, not file mtime (safe across Git pulls)."""
    digest = hashlib.sha256()
    for path in watched_files(root):
        digest.update(str(path.relative_to(root)).encode("utf-8"))
        digest.update(b"\0")
        with path.open("rb") as stream:
            while block := stream.read(1048576):
                digest.update(block)
        digest.update(b"\0")
    return digest.hexdigest()

def verify_master(connection):
    """Fail closed: no misleading complete snapshot if references are broken."""
    if connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
        raise RuntimeError("SQLite integrity_check failed")
    missing = connection.execute("PRAGMA foreign_key_check").fetchall()
    if missing:
        raise RuntimeError(f"Foreign key violations in master database: {missing[:5]}")
    counts = {}
    for label, table in (
        ("research_subjects", "reconstruction_subjects"),
        ("building_candidates", "building_dossiers"),
        ("envelopes", "master_building_envelopes"),
        ("interactions", "master_interactive_points"),
        ("media_links", "master_all_media"),
    ):
        counts[label] = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    if counts["research_subjects"] == 0 or counts["building_candidates"] == 0:
        raise RuntimeError("Missing essential research inventory/building rows")
    duplicate_envelopes = connection.execute("""
        SELECT envelope_id,COUNT(*) AS n
        FROM master_building_envelopes
        GROUP BY envelope_id HAVING n>1""").fetchall()
    if duplicate_envelopes:
        raise RuntimeError("Duplicate envelope identities")
    return counts

def write_json_atomic(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".new")
    temporary.write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n",
                         encoding="utf-8")
    os.replace(temporary, path)

def sync_once(output_root: Path, root: Path = ROOT, model_root: Path | None = None):
    """Build full snapshot in a temp directory, validate, then promote it.

    Repo tables are never edited here; a corrupt incoming CSV cannot erase the
    last good production index. The generated output is a *cache*, not truth.
    """
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    if model_root is not None:
        refresh_registered_models(model_root, root / "catalog", repo_root=root)
    fingerprint = source_fingerprint(root)
    with tempfile.TemporaryDirectory(prefix=".fmp-master-build-", dir=output_root) as tmp:
        staging = Path(tmp)
        staged_db = staging / "master.sqlite"
        staged_dossiers = staging / "dossiers"
        staged_handoff = staging / "runtime_handoff"
        # Build_db is bound to ROOT, intentionally refusing another source tree.
        if root.resolve() != ROOT.resolve():
            raise ValueError("sync_once requires its own checkout; do not mix repositories")
        build(staged_db)
        with sqlite3.connect(staged_db) as connection:
            counts = verify_master(connection)
            summary = export_pack(connection, staged_dossiers)
            runtime_handoff = export_runtime_handoff(connection, staged_handoff, denominator=250)
        # Only replace the last good SQLite database after all checks/export pass.
        destination_db = output_root / "flushing_meadows.sqlite"
        os.replace(staged_db, destination_db)

        # Per-building exports are replaceable derived artifacts, never edited
        # directly. Keep the prior folder until new one has been built.
        destination_dossiers = output_root / "building_program"
        backup = output_root / ".building_program_previous"
        if backup.exists():
            shutil.rmtree(backup)
        if destination_dossiers.exists():
            os.replace(destination_dossiers, backup)
        try:
            os.replace(staged_dossiers, destination_dossiers)
        except Exception:
            if backup.exists():
                os.replace(backup, destination_dossiers)
            raise
        if backup.exists():
            shutil.rmtree(backup)
        handoff_dest = output_root / "runtime_handoff"
        handoff_backup = output_root / ".runtime_handoff_previous"
        if handoff_backup.exists():
            shutil.rmtree(handoff_backup)
        if handoff_dest.exists():
            os.replace(handoff_dest, handoff_backup)
        try:
            os.replace(staged_handoff, handoff_dest)
        except Exception:
            if handoff_backup.exists():
                os.replace(handoff_backup, handoff_dest)
            raise
        if handoff_backup.exists():
            shutil.rmtree(handoff_backup)
    report = {
        "schema": "fmp.master-db-refresh.v1",
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "source_fingerprint_sha256": fingerprint,
        "mode": "LOCAL_SOURCE_REBUILD",
        "counts": counts,
        "export": summary,
        "runtime_handoff": {"building_manifests": len(runtime_handoff["buildings"]), "units":"metres->Unreal centimetres and scaled print millimetres"},
        "source_of_truth": "version-controlled CSV + migration SQL; generated SQLite is derivative",
        "current_snapshot": str(output_root / "flushing_meadows.sqlite"),
        "dossiers_directory": str(output_root / "building_program"),
        "remote_drive_updates": "NOT_AUTO_POLLED",
        "notes": "No claim of site-registered envelopes, measured interaction XY or Unreal-ready collision",
    }
    write_json_atomic(output_root / "master_sync_report.json", report)
    return report

def run_watch(output_root: Path, seconds: float, model_root: Path | None = None):
    if seconds < 1:
        raise ValueError("Minimum local polling interval is 1 second")
    previous = None
    print("FMP local watcher running: source catalogs and explicitly registered GLBs.")
    try:
        while True:
            try:
                # Scan source models before checking CSV fingerprints so new
                # geometry revisions trigger a single DB/dossier refresh.
                if model_root is not None:
                    result = refresh_registered_models(model_root, ROOT / "catalog")
                    if result["changed"]:
                        print("Observed new model versions:", result["changed"],
                              "measured parts:", result["components_added"], flush=True)
                current = source_fingerprint()
                if current != previous:
                    report = sync_once(output_root)
                    previous = current
                    print("Master database refreshed:", report["counts"],
                          "at", report["updated_utc"], flush=True)
            except Exception as exc:
                # Keep last known-good master database and try the next cycle.
                print("Refresh rejected, previous snapshot retained:", exc, flush=True)
            time.sleep(seconds)
    except KeyboardInterrupt:
        print("FMP local watcher stopped.")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--once", action="store_true", help="Generate one validated snapshot")
    mode.add_argument("--watch", action="store_true",
                      help="Stay running and regenerate when local source files change")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "out")
    parser.add_argument("--interval", type=float, default=3.0)
    parser.add_argument("--model-root", type=Path,
                        default=ROOT / "models/incoming",
                        help="Directory containing registered *.fmp-model.json GLBs")
    parser.add_argument("--no-model-scan", action="store_true",
                        help="Only rebuild from existing CSV/SQL without touching GLB source catalogs")
    args = parser.parse_args()
    model_root = None if args.no_model_scan else args.model_root
    if args.watch:
        run_watch(args.output_dir, args.interval, model_root=model_root)
    else:
        report = sync_once(args.output_dir, model_root=model_root)
        print(json.dumps(report["counts"], indent=2))

if __name__ == "__main__":
    main()
