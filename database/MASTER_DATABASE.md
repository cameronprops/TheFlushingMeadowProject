# FMP: The One Master Database (v1, 2026-10-19)

There is **one master building record** for every possible fair structure, with linked architectural, historical, media, gameplay, and model data. This extends the existing database; it does not replace the Trylon/Perisphere point of truth or older research.

## Existing system (preserved)

The project already had 239 archival research subjects, 195 architecture/pavilion/venue candidates requiring classification, and linked historical evidence, dimensional parameters, architectural details, period variants, interiors, material/appearance variants, procedural geometry, and shell-first exports. The candidates are **not** all independently verified buildings.

The canonical inputs are the version-controlled CSV catalogs and SQL migrations. The generated SQLite database, JSON/Markdown building dossiers and overview CSV are reproducible indexes; never edit those derived files as competing authorities.

## New v1 fields and views

- **master_building_envelopes:** Dated coordinate-frame-specific actual mesh bounding boxes, model source IDs, source status and position-registration flags. A GLB mesh envelope is not a surveyed 1939 site footprint.
- **master_interactive_points:** Stable point ID, building, year, optional room, label, behavior (enter, examine, watch, board, exit), XYZ if known, position confidence, public/restricted access, Unreal binding/QA.
- **master_media_assets** and **master_building_media:** Explicit links for GLB, CAD, photos, brochures, videos, audio, textures, generator scripts and source archives. Respect ownership and acquisition status.
- **master_all_media (view):** Automatically combines explicit registered files with existing archival evidence records, shell assets and photographed view references. Research links are NOT claims that source files were downloaded.
- **master_building_overview (view):** One row per building candidate with name, years, zone, stage, priority and counts of dimensions, envelopes, interactions, rooms, source evidence and related media.
- JSON/Markdown per-building exports now include all linked records.

## Run locally after cloning the repository

Build and export once:

    python3 tools/sync_master_database.py --once

Or run an optional local watcher during active modeling. It reacts when local CSV/SQL source files change:

    python3 tools/sync_master_database.py --watch --interval 3

Validate when updating code:

    python3 -m unittest -v tests.test_master_building_index tests.test_building_program

Outputs:
- out/flushing_meadows.sqlite — master read/query database
- out/master_sync_report.json — fingerprint and last successful refresh
- out/building_program/master_building_overview.csv — one indexed building row per candidate
- out/building_program/buildings/WF0001.json + WF0001.md — Trylon
- out/building_program/buildings/WF0002.json + WF0002.md — Perisphere
- out/building_program/buildings/WF0014.json + WF0014.md — Ford
- out/building_program/buildings/WF0020.json + WF0020.md — Westinghouse

**Watcher limits:** The process must be running. It does not poll the remote Google Drive account, download new pictures, automatically recalculate GLB geometry, or run while the computer is off. Run git pull (or edit local catalogs) to trigger a local refresh. No GitHub Actions charges.

## Example questions the index can answer

    SELECT * FROM master_building_overview WHERE building_id='WF0002';

    SELECT * FROM master_building_envelopes
    WHERE building_id='WF0014';

    SELECT label,requested_behavior,position_status,x_m,y_m,z_m
    FROM master_interactive_points WHERE building_id='WF0014';

    SELECT record_type,title,uri,project_uri,rights_status,acquisition_status
    FROM master_all_media WHERE building_id='WF0002';

    SELECT building_id,display_name,dimension_count,room_count,interaction_count,media_count
    FROM master_building_overview WHERE production_priority='P1';

## Critical distinctions

Original Trylon and Perisphere 510-node GLB, 1939 Ford v003 and Westinghouse v002 are **source model-space objects** with different up-axis conventions (Y-up / Z-up). Initial envelope bounds come from the existing GLBs and are not site-registered. The first 10 interactive points are purposely left unlocated rather than inventing measured coordinates.

Each historically supported number remains dated, attributed, and tagged documented/proposed/photo-inferred. Exterior and guest-facing interior shells take priority; optional steel lives in a structural/construction-animation layer. Realistic and stylized skins share one geometry and collision coordinate contract.

The database can index the existence of assets, photographs, videos, models, drawings, and music even when rights/bytes are unavailable. It cannot truthfully say an unavailable source has been acquired.

Media pipeline future: connected Drive folder-change ingestion; automatic source GLB envelope extraction; further automated procedural geometry rebuilding. Today the master index and dossier **refresh themselves from local source catalogs when invoked**, but they do not regenerate historical models or remote media without explicit source ingestion and modeling steps.

## Recorded initial v1 population

- 4 measured-in-model-space envelopes (Trylon, Perisphere, Ford and Westinghouse)
- 10 planned interactive points, all with unknown XYZ until surveyed
- 7 registered project media assets, 10 explicit attachment links
- all existing building_evidence, building_shell_parts, and building_view_observations are automatically included in master_all_media.

Full source files: database/migrations/012_master_building_index.sql; catalog/master_*.csv; tools/build_db.py; tools/export_building_dossiers.py; tools/sync_master_database.py.
