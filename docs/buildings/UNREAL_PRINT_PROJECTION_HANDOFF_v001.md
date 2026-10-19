# FMP — Unreal / Fabrication / Future Projection Handoff v0.1

**Purpose:** Produce read-only, reproducible JSON from the existing FMP master SQLite database. This is a *shared release contract*, not a new authoritative database or a finished Unreal scene.

## Inputs
- `master_active_model_releases`: selected revision and source GLB SHA-256.
- `master_model_components`: geometry part IDs, mesh bounds and PBR source names.
- `master_interactive_points`: planned visitor interactions; coordinates remain null until located.
- `master_all_media`: related archival media and model files.
- `master_building_envelopes` / `building_spaces`: measured model bounds, portal and room status.

## Outputs
One `{building_id}_{year}_handoff.json` per modelled building and `handoff_index.json` with deterministic SHA-256 hashes. Includes per-model source-to-Unreal 4×4 matrix (metres → centimetres), preview-scale bounding dimensions in millimetres, persistent mesh source IDs, material slots, media and interactions. Projection calibration (physical registration, optics, warps), Unreal binding, collision QA and slicer QA are explicitly **NOT IMPLEMENTED** and always marked as such.

## Use after complete FMP database build
```bash
python3 tools/sync_master_database.py --once
python3 tools/building_program/export_runtime_handoff.py --db out/flushing_meadows.sqlite --out out/unreal_print_handoff --scale 250
python3 -m unittest -v tests.test_runtime_handoff
```

Native host acceptance is required for axis/winding conversion, z-fighting, material instances, collision, print-bed sizing and projection registration. A model-level bounding box is NOT a printable solid.

## Geometry and coordinates
- Historical site registration is **not inferred** from preview GLB coordinates.
- GLB source units assumed metres. Source Y-up (right-handed) maps to Unreal Z-up (left-handed) centimetres by `(x, z, y)*100`; source Z-up (right-handed) by `(x, -y, z)*100`. Source handedness and winding must be verified in the native host before production deployment.
- Physical model preview dimensions = source bounds in metres × `1000 / print_scale_denominator`.
- Projection hardware calibration is future work, so world→physical registration matrix and projector intrinsics/extrinsics/warp are all `null`.
- Both render looks are material overrides assigned to the exact same persistent mesh IDs; FMP's historical material research is distinct from GLB preview materials.

## Real-geometry test fixture
The accompanying four-building sample was generated from the earlier **696-part FMP GLB inspection cache**, and its source SHA-256 values were independently checked against the three surviving original local GLB files (one shared Trylon/Perisphere file). Four preview handoffs: Trylon 1 component, Perisphere 2, Ford 310, Westinghouse 383. The test fixture does **not** contain the complete current normalized 195-candidate research database; its 8 interaction records are demonstration placeholders, deliberately UNLOCATED.

This is the first transport artifact compatible with an eventual FMP–Worldwright–Unreal–projection workflow; it does not implement show cue transport, nDisplay, projector calibration, or a physical installation.