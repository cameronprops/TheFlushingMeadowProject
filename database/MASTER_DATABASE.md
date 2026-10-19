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

- 8 source-model envelopes (four reviewed preview bounds and four newly GLB-inspected release bounds)
- 10 planned interactive points, all with unknown XYZ until surveyed
- 9 registered project media assets, 14 explicit attachment links
- all existing building_evidence, building_shell_parts, and building_view_observations are automatically included in master_all_media.

Full source files: database/migrations/012_master_building_index.sql; catalog/master_*.csv; tools/build_db.py; tools/export_building_dossiers.py; tools/sync_master_database.py.

## GLB ingestion v1 — 19 October 2026

We extended the same database, rather than creating another project inventory. Real source-GLB inspection now populates `master_model_components` (migration 013) and `master_model_materials`. The canonical catalog contains **696 mesh-component records** from the original Trylon/Perisphere shared GLB, Ford v003 and Westinghouse v002: **656 watertight** and **40 currently open component meshes** (all 40 in Westinghouse). Ford exposes **eight shader/material groups**. These are *geometry observations*, not proof of period construction dimensions or successful printer/Unreal validation.

The model release inspector is `tools/building_program/ingest_glb.py`. To review first, run it against a local GLB, explicitly specifying building/year/axis and selecting the correct nodes for shared scenes. To merge the computed data into CSV source-of-truth files, add `--apply --catalog-dir catalog`. It preserves the original mesh, requires a consistent source SHA per asset identity, stages media links and source-model envelopes, and records material and mesh QA. The existing SQLite watcher then regenerates the indexed master database when CSV source files change.

The repository now contains 8 measured *model-space* envelopes, 10 planned interaction points (locations unresolved), 9 explicit project media assets, 14 file links, and 696 individually identified GLB meshes in addition to the archival/photo/material/history evidence. The 195-dossier export includes source-mesh and material counts per building.

**See** [model import and reproducible measurements](../docs/buildings/FMP_AUTOMATIC_GLB_INGEST_v001.md). The importer is tested on actual source files and seven portable synthetic fixtures; the full 195-candidate SQLite build still needs a complete-checkout runtime test.

## New: automatic current-GLB refresh (2026-10-19)

Registered GLBs can now update this single database as the user saves model revisions in a local/synced folder. The model scanner creates **new immutable media/mesh records** when the GLB's SHA-256 or selected node set changes; `master_active_model_releases` tracks the currently selected revision for each building/year/logical role.

The `master_building_dashboard_v2` view merges earlier architectural and media information with active mesh/closed-component/material counts. Its building dossiers include `active_model_releases`; no measurements are represented as certified historic as-built drawings.

Run `python3 tools/sync_master_database.py --once` to import registered GLBs, validate/rebuild the SQLite index, and export updated dossiers in one command. Run the same tool with `--watch --interval 4` while working for active file-change monitoring; default model folder is `models/incoming`. Add `--no-model-scan` to refresh only catalog sources.

Registration examples and setup: [models/incoming/README.md](../models/incoming/README.md); full technical instructions: [AUTOMATIC_MODEL_REFRESH_v002.md](../docs/buildings/AUTOMATIC_MODEL_REFRESH_v002.md).

The initial active-release register preserves known source file SHA-256 values for Trylon, Perisphere, Ford v003 and Westinghouse v002; local file paths remain unresolved until each model folder is configured. A local watcher is not a persistent online task and does not itself sync or back up assets to Drive.

## Historical route and buried utility networks (migration 015)

[Production specification](../docs/site/FMP_HISTORIC_ROUTES_AND_UTILITIES_v001.md) extends this same master database with named pedestrian paths, streets, service-only alleys, bridges, gates and separate buried potable-water, building-water, sanitary, storm, gas, conduit, power and fountain layers. Each segment has a historical year, sheet source, alignment status, possible measured width/depth, access/navigability flag and optional dated cross-era relationship. Unknown positions are NULL; an archival sheet index is not a surveyed sewer line.

Inputs: `catalog/site_network_*.csv`; schema: `database/migrations/015_dated_site_networks.sql`. Reads: `site_network_progress`, `site_walkable_edges` and `site_utility_segments`. As of v001: 43 catalog sheet records, 19 layer families, 19 named untraced route records; 0 georeferenced route/pipe segments, no manufactured cross-era pipe continuity. Source-backed RCA shell comes first; the full site network is the following FMP production milestone.
