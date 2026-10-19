# FMP — Actual GLB geometry into the One Master Database (2026-10-19)

## Implementation delivered

**Code:** [ingest_glb.py](../../tools/building_program/ingest_glb.py). The importer loads an existing GLB, verifies its immutable SHA-256, selects exact mesh-node names for buildings sharing a scene, resolves actual node transforms, calculates model-local bounds, records each named mesh's vertex/face count, watertight condition, and available material name/PBR roughness and metallic values, and stages machine-readable CSV additions. **It never changes the original GLB.**

**Master schema:** [013_source_model_components.sql](../../database/migrations/013_source_model_components.sql) adds `master_model_components` (with source-media FK) and `master_model_materials` view for visual/material audits.

**Master build:** `tools/build_db.py` imports the new table, and `tools/export_building_dossiers.py` includes part-level and material-group audits in each per-building dossier. Existing 012 envelopes/media/interactive points and historical facts remain canonical.

**Current committed inventory:** `catalog/master_model_components.csv` has **696 measured mesh part records**; `catalog/master_building_envelopes.csv` contains 8 records (4 reviewed previews, 4 automatically measured current source-model envelopes). `catalog/master_media_assets.csv` contains 9 asset records (including two new model revisions), and `catalog/master_building_media.csv` has 14 attachment links. No old media record is overwritten during import.

| Model | Source GLB | Axis | Selected mesh nodes | Watertight | Distinct material groups |
|---|---|---|---:|---:|---:|
| Trylon | 510-node Theme Center staging | Y-up | 1 | 1 | 1 |
| Perisphere | same preserved Theme Center GLB | Y-up | 2 | 2 | 1 |
| Ford exterior/road/interior proxies v003 | standalone GLB | Z-up | 310 | 310 | 8 |
| Westinghouse public-access prototype v002 | standalone GLB | Z-up | 383 | 343 | 1 |
| **Total** | | | **696** | **656** | |

Westinghouse's 40 non-watertight component meshes need review *only where watertightness matters* (e.g. printed solids); single-sided architectural facade surfaces may intentionally remain open. **None** of these checks certifies 1939 site placement, historic dimensions, safe public passage, accurate surface colors, actual material samples, or print-ready wall thickness.

## Reinspect any building from a local file

First generate review-only staging files (replace path to model with actual local GLB path):

```bash
python3 tools/building_program/ingest_glb.py \
  --glb /your/models/FMP_ThemeCenter_Staging_v001.glb \
  --building WF0001 --year 1939 --up Y \
  --asset-id FMP-MEDIA-THEME-STAGING \
  --expected-sha a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5 \
  --node Trylon_Hollow_Exterior \
  --scope EXTERIOR_SHELL_SOURCE --out out/glb_qa/trylon
```

To merge the reviewed source-model facts into canonical version-controlled CSV catalogs, add:

```bash
  --apply --catalog-dir catalog
```

For Perisphere select **two** nodes using repeated `--node` flags. For Ford and Westinghouse, omit `--node` to inventory every mesh in the whole GLB; explicitly tag the scope as a preview including roads or interior, **not a measured exterior building footprint**. For subsequent versions, use a **new asset ID**. The importer rejects reusing a model media ID with a different recorded SHA-256, preserving release provenance.

Then refresh the one master database and all candidate dossiers:

```bash
python3 tools/sync_master_database.py --once
python3 -m unittest -v tests.test_master_building_index tests.test_building_program
```

The existing `--watch` mode in `tools/sync_master_database.py` updates SQLite when CSV/SQL files change; **it does NOT watch and reimport GLB files automatically yet**. Run the importer after a new model release, or connect it to the local build pipeline. Do not promise unattended Google Drive polling, GitHub Actions, or native Unreal tests.

## Standalone ingestion testing

```bash
cd tools/building_program
python3 -m unittest -v test_ingest_glb
```

Seven portable synthetic-GLB tests check node selection, transformed bounds, SHA guard, stable IDs, deterministic CSV staging, and CLI output. The first actual four-model inspection was also performed locally, including source readback and reported mesh tallies. The complete **195-candidate SQLite build and integration suite** have not yet been run in this sandbox because the full repository checkout isn't available to the sandbox; do not mark master-runtime verification complete.

## Future sync and cinematic/print enhancement

1. Add a locally configurable **model release manifest** to call ingestion automatically after new output GLBs are generated; let the existing CSV watcher refresh the SQLite cache.
2. Track exact material slots with source-linked period evidence: GLB PBR values are the *current shader*, not authenticated 1939 finish.
3. Track revised node/mesh hashes and materials between releases. For Unreal, preserve stable source node names and map visitors/interactions to separate collision volumes.
4. Validate separate source-model bounds and actual registered world-placement transforms; never convert local X/Y/Z into fairground coordinates without site control.
5. For printing, run thickness, manifold/closure, bounding-box, registration joint and segmentation checks before certifying source shell geometry.
