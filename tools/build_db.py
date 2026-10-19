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
    "historical_interviews": ("catalog/historical_interviews.csv", ("interview_id", "interviewee_or_group", "interviewer_or_host", "interview_date", "publication_date", "recalled_fair_years", "fair_role", "building_or_subject", "research_value", "record_type", "repository", "catalog_url", "transcript_access", "audio_access", "source_review", "rights_status", "archive_copy_status", "priority", "next_action")),
    "oral_history_collections": ("catalog/oral_history_collections.csv", ("collection_id", "title", "repository", "date", "era_covered", "catalog_url", "status", "description", "next_action")),
    "interview_claims": ("catalog/interview_claims.csv", ("claim_id", "interview_id", "linked_asset", "summary", "claim_class", "timecode_or_section", "recalled_era", "verification_next")),
    "future_scenarios": ("catalog/future_scenarios.csv", ("scenario_id", "branch_id", "year", "title", "scenario_class", "status", "canonical", "site_coordinate_policy", "notes")),
    'archive_inventory_candidates': ('catalog/archive_inventory_candidates.csv', ('inventory_id', 'label', 'year_candidates', 'category', 'zone', 'evidence_status', 'identity_status', 'is_verified_structure', 'physical_structure_state', 'plans_status', 'geometry_status', 'gameplay_scope', 'source_id', 'source_url', 'archive_status', 'notes')),
    'archive_source_catalog_v2': ('catalog/archive_source_catalog_v2.csv', ('source_id', 'title', 'repository', 'source_kind', 'catalog_url', 'year_scope', 'date_on_source', 'access_status', 'full_source_downloaded', 'local_or_drive_location', 'sha256', 'rights_status', 'priority', 'notes')),
    'archive_operations_manual_sheets': ('catalog/archive_operations_manual_sheets.csv', ('sheet_id', 'sheet_number', 'title', 'year_scope', 'source_id', 'sheet_catalog_url', 'drawing_direct_url', 'downloaded', 'registered_to_site', 'reconstruction_value', 'notes')),
    'archive_production_availability': ('catalog/archive_production_availability.csv', ('inventory_id', 'label', 'year_candidates', 'priority', 'identity', 'map_footprint', 'floorplan', 'elevations_sections', 'period_photographs', 'terrain_elevation', 'exterior_model', 'interior_model', 'historical_show', 'gameplay', 'testing', 'next_research')),
    'building_details': ('catalog/building_details.csv', ('building_id', 'architectural_attribution', 'architectural_form', 'known_dimensions', 'structural_materials', 'facade_roof', 'site_orientation', 'documented_interiors', 'interaction_points', 'exact_dimensions_status', 'year_variant_notes', 'workflow_notes', 'details_status')),
    'building_evidence': ('catalog/building_evidence.csv', ('evidence_id', 'building_id', 'year', 'document_title', 'repository', 'document_url', 'archive_locator', 'document_type', 'evidence_scope', 'claim_or_research_value', 'evidence_status', 'rights_status', 'local_or_drive_uri', 'sha256', 'revision_date', 'reviewer_note')),
    'building_spaces': ('catalog/building_spaces.csv', ('space_id', 'building_id', 'year', 'space_name', 'space_type', 'access_intent', 'evidence_status', 'floor_level', 'plan_reference', 'entrance_geometry_status', 'interior_model_status', 'collision_status', 'navigation_status', 'notes')),
    'building_geometry_parameters': ('catalog/building_geometry_parameters.csv', ('parameter_id', 'building_id', 'period_year', 'component_id', 'parameter_key', 'value_si', 'units_si', 'period_source_value', 'source_evidence_id', 'evidence_class', 'tolerance_si', 'adjustment_status', 'notes')),
    'building_surface_research': ('catalog/building_surfaces.csv', ('surface_id', 'building_id', 'period_year', 'component_selector', 'material_family', 'finish_description', 'substrate', 'glass_transmission', 'measured_color', 'metallic', 'roughness', 'texture_asset_uri', 'evidence_id', 'certainty', 'skin_policy', 'notes')),
    'building_view_observations': ('catalog/building_visual_observations.csv', ('view_id', 'building_id', 'period_year', 'evidence_id', 'image_uri', 'view_direction', 'lens_perspective', 'visible_components', 'fixed_points', 'estimated_dimensions', 'mesh_reference_uri', 'geometry_use', 'confidence', 'notes')),
}

def build(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    connection = sqlite3.connect(output)
    try:
        connection.executescript((ROOT / "database/schema.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/001_narrative_tables.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/002_oral_history_tables.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/003_future_scenarios.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/004_archived_inventory.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/005_building_program.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/007_procedural_architecture.sql").read_text(encoding="utf-8"))
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
        connection.executescript((ROOT / "database/migrations/006_building_priorities.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/008_gm_research_priority.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/009_ford_cycle_identification.sql").read_text(encoding="utf-8"))
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
