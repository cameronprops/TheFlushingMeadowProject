# FMP — model-aware master database refresh (v0.2)

## What is now operational

The existing FMP master database holds identities, historical evidence, shells, interior spaces, interactive points, materials, and media. We have extended it with **current model revision pointers** and a **registered-GLB file watcher**.

When a registered GLB changes on disk, the importer:

1. computes the full file SHA-256 and checks a required building/year/up-axis/role manifest;
2. measures the explicitly selected GLB nodes (or all nodes if unspecified) without editing the source;
3. records updated mesh bounds, individual component names, watertight status, material/roughness/metallic values;
4. creates an immutable *versioned* media ID that includes source hash and selection/settings hash;
5. preserves prior geometry/media records and updates exactly one **active-model pointer** per building/year/role;
6. writes all affected canonical CSVs after all registered models have passed inspection; rolls back files on an application error;
7. lets `tools/sync_master_database.py` rebuild SQLite plus 195 building-specific JSON/Markdown construction briefs.

**No historical site-placement claim is created by importing a GLB.** Bounds stay in explicitly declared GLB coordinates (e.g. Y-up for Theme Center versus Z-up for Ford). Curated drawing dimensions and archives are untouched.

## Usage

Install requirements for mesh reading: `python3 -m pip install numpy trimesh`.

In the clone, place your GLBs under `models/incoming` or edit the sidecar's GLB relative path. Copy an example file in `models/incoming` and remove `.template` from the filename so it ends in `.fmp-model.json`. Required manifest fields:

```json
{
  "building_id": "WF0001",
  "year": 1939,
  "up": "Y",
  "role": "EXTERIOR_SHELL",
  "glb": "FMP_ThemeCenter_Staging_v001.glb",
  "nodes": ["Trylon_Hollow_Exterior"],
  "envelope_scope": "EXTERIOR_SHELL_MODEL_BOUNDS"
}
```

`nodes` is optional (omit to inspect every mesh in the GLB). You can register one shared GLB twice using separate Trylon and Perisphere sidecars with different building IDs/selected nodes. `role` is a stable *logical release category*, not a historical material. Examples: EXTERIOR_SHELL, INTERIOR_SHELL, FULL_SCHEMATIC. Only one manifest may claim the same building/year/role.

From the checkout root:

```bash
# Inspect source GLBs, then rebuild the normalized SQLite and all building dossiers:
python3 tools/sync_master_database.py --once

# Keep this terminal running while working on registered GLB files:
python3 tools/sync_master_database.py --watch --interval 4

# Mesh-only ingestion without rebuilding the SQLite index:
python3 tools/building_program/refresh_model_catalog.py --once

# Database only (skip model reading):
python3 tools/sync_master_database.py --once --no-model-scan
```

### Inspect current model revisions with SQL

```sql
SELECT * FROM master_active_model_summary
WHERE building_id='WF0001';

SELECT source_node,faces,watertight,material_name
FROM master_active_model_components
WHERE building_id='WF0014'
ORDER BY source_node;
```

If you need to return to an earlier version, replace a building/year/role's `active_media_id` in the version-controlled `catalog/master_active_model_releases.csv` with a previous corresponding media ID and its matching SHA, or point the sidecar at that earlier GLB and ingest it again. The measured historical geometry observations remain in the database.

## Safety limits

- Unregistered GLBs are **ignored** rather than assumed to belong to a particular pavilion.
- Missing source files, wrong node names, duplicate manifest release keys and invalid source models cause the refresh to fail without silently publishing new data.
- The watcher reads a **local/synced folder while the process is running**. It is not a background cloud service and does not remotely poll Drive by itself. Google Drive Desktop can sync assets into that folder, but updates and permissions must be configured outside this tool.
- Historical pavilion footprints do not change when a local GLB bounding box changes. A GLB component might be watertight but still not be a 3D-print-ready assembly.
- Existing native Unreal lighting, visitor interactivity, collision, runtime movement and material correctness must be tested in the engine; neither SQL nor trimesh certifies these.
- Rebuilds of CAD geometry themselves still require the pavilion's dedicated parametric generator. The watcher responds to generated GLB files, not directly to arbitrary dimension edits.

## Validation observed 2026-10-19

- Eight synthetic integration tests passed: selected node ownership; deterministic reruns; revision retention; selection revisioning; corrupt/unknown node rejection; duplicate release-key rejection; unregistered GLBs ignored; absent source folder no-op.
- Tested against real existing Theme Center (Trylon selected shell) and Ford v0.3 (all 310 GLB nodes) using copies of the preexisting measurement catalogs: first pass produced 311 inspected model components; the second pass produced 0 changes. **Actual GLBs were not modified**.
- Whole-checkout master SQLite rebuild is **not yet locally certified** in this runtime, because the complete Git checkout is not mounted here. The new migrations, source catalogs, and tests are committed for a reproducible local verification.

## Source files

- `tools/building_program/ingest_glb.py`: pre-existing nonmutating GLB inspector.
- `tools/building_program/refresh_model_catalog.py`: version-aware file-scanned catalog promotion.
- `database/migrations/014_active_model_releases.sql`: active model revision and active-component query views.
- `catalog/master_active_model_releases.csv`: four seeded current release pointers.
- `tools/sync_master_database.py`: combined automatic model scan, normalized SQLite update, pavilion dossier export.
- `tests/test_model_autorefresh.py`: eight portable tests.
