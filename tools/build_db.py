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
    'master_building_envelopes': ('catalog/master_building_envelopes.csv', ('envelope_id', 'building_id', 'period_year', 'envelope_scope', 'coordinate_frame', 'min_x_m', 'min_y_m', 'min_z_m', 'max_x_m', 'max_y_m', 'max_z_m', 'source_geometry_node', 'source_asset_id', 'evidence_status', 'uncertainty_m', 'site_registered', 'notes')),
    'master_interactive_points': ('catalog/master_interactive_points.csv', ('point_id', 'building_id', 'period_year', 'space_id', 'label', 'interaction_type', 'public_access', 'coordinate_frame', 'x_m', 'y_m', 'z_m', 'position_status', 'requested_behavior', 'trigger_or_scene_key', 'implementation_status', 'native_unreal_tested', 'notes')),
    'master_media_assets': ('catalog/master_media_assets.csv', ('media_id', 'title', 'kind', 'period_year', 'uri', 'repo_path', 'mime_type', 'sha256', 'rights_status', 'acquisition_status', 'notes')),
    'master_building_media': ('catalog/master_building_media.csv', ('link_id', 'building_id', 'media_id', 'period_year', 'role', 'component_id', 'notes')),
    'master_model_components': ('catalog/master_model_components.csv', ('component_id', 'building_id', 'period_year', 'model_asset_id', 'source_node', 'mesh_key', 'role', 'coordinate_frame', 'min_x_m', 'min_y_m', 'min_z_m', 'max_x_m', 'max_y_m', 'max_z_m', 'vertices', 'faces', 'watertight', 'material_name', 'roughness', 'metallic', 'source_sha256', 'verification_status')),
    'master_active_model_releases': ('catalog/master_active_model_releases.csv', ('release_key','building_id','period_year','logical_role','active_media_id','source_path','source_sha256','up_axis','selected_nodes','observed_utc','status')),
    'site_network_sheets': ('catalog/site_network_sheets.csv', ('sheet_id','era_year','sheet_title','sheet_number','archive_collection','archive_url','primary_layer','availability','status_note')),
    'site_network_layers': ('catalog/site_network_layers.csv', ('layer_id','family','medium','walkable','typically_buried','description')),
    'site_network_features': ('catalog/site_network_features.csv', ('feature_id','canonical_name','feature_kind','identity_status','comment')),
    'site_network_nodes': ('catalog/site_network_nodes.csv', ('node_id','era_year','layer_id','name','x_m','y_m','z_m','coordinate_frame','horizontal_crs','vertical_datum','location_status','source_sheet_id')),
    'site_network_segments': ('catalog/site_network_segments.csv', ('segment_id','feature_id','era_year','layer_id','historical_name','from_node_id','to_node_id','geojson_geometry','source_sheet_id','alignment_status','width_m','depth_m','invert_elevation_m','flow_direction','access_class','navigable','estimated_accuracy_m','note')),
    'site_network_era_relations': ('catalog/site_network_era_relations.csv', ('relation_id','earlier_segment_id','later_segment_id','relation_type','evidence_sheet_id','confidence','note')),
    'site_amenity_categories': ('catalog/site_amenity_categories.csv', ('category_id','category_family','display_name','suggested_layer','visible_in_unreal','note')),
    'site_amenity_types': ('catalog/site_amenity_types.csv', ('type_id','category_id','era_year','historical_label','type_status','period_quantity','measured_height_m','measured_width_m','measured_depth_m','material_note','source_sheet_id','linked_model_uri','evidence_note')),
    'site_amenity_evidence': ('catalog/site_amenity_evidence.csv', ('observation_id','type_id','era_year','source_sheet_id','source_url','source_locator','observation_kind','observation_status','claim','approximate_named_context','observed_quantity','rights_status','notes')),
    'site_amenity_instances': ('catalog/site_amenity_instances.csv', ('instance_id','type_id','era_year','location_label','nearby_building_id','nearby_route_segment_id','source_observation_id','position_status','coordinate_frame','x_m','y_m','z_m','longitude','latitude','horizontal_crs','vertical_datum','yaw_deg','placement_uncertainty_m','historical_visibility','model_asset_uri','unreal_scene_object_id','print_component_id','notes')),
    'site_amenity_service_links': ('catalog/site_amenity_service_links.csv', ('service_link_id','instance_id','network_layer_id','segment_id','service_kind','linkage_status','source_observation_id','notes')),
    'site_amenity_era_relations': ('catalog/site_amenity_era_relations.csv', ('relation_id','earlier_instance_id','later_instance_id','relation_type','evidence_observation_id','certainty','notes')),
    'horticulture_sources': ('catalog/horticulture_sources.csv', ('source_id','era_year','title','repository','source_url','archive_locator','document_date','source_class','access_status','historical_status','rights_status','notes')),
    'horticulture_taxa': ('catalog/horticulture_taxa.csv', ('taxon_id','display_name','scientific_name','taxonomic_precision','growth_form','notes')),
    'horticulture_areas': ('catalog/horticulture_areas.csv', ('area_id','era_year','historical_name','area_kind','parent_area_id','associated_building_id','associated_route_segment_id','source_id','named_context','approximate_area_m2','area_measurement_status','location_status','local_polygon_geojson','coordinate_frame','horizontal_crs','vertical_datum','notes')),
    'horticulture_plantings': ('catalog/horticulture_plantings.csv', ('planting_id','era_year','area_id','taxon_id','source_id','display_label','planting_role','installation_status','quantity','quantity_basis','variety_count','cultivar_name','seasonal_window','growing_pattern','evidence_excerpt','estimated_height_m','model_asset_uri','unreal_layer','note')),
    'horticulture_seasonal_events': ('catalog/horticulture_seasonal_events.csv', ('event_id','era_year','area_id','planting_id','source_id','event_type','date_start','date_end','date_precision','event_status','notes')),
    'horticulture_era_links': ('catalog/horticulture_era_links.csv', ('link_id','earlier_area_id','later_area_id','relation_type','source_id','certainty','notes')),
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
        connection.executescript((ROOT / "database/migrations/012_master_building_index.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/013_source_model_components.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/014_active_model_releases.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/015_dated_site_networks.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/016_dated_site_amenities.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/017_historical_horticulture.sql").read_text(encoding="utf-8"))
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
        connection.executescript((ROOT / "database/migrations/010_theme_center_asset_registry.sql").read_text(encoding="utf-8"))
        connection.executescript((ROOT / "database/migrations/011_shell_first_production.sql").read_text(encoding="utf-8"))
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
