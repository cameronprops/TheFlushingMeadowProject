# Flushing Meadows Theme Center Solver v0.1

**Scope:** 1939 Trylon, Perisphere, Helicline, and connecting bridge. Mathematically audited outputs, not final as-built geometry. Runs with Python 3.9 or newer. No Rhino, Wolfram, or Unreal runtime required to recheck the frozen facts.

## Commands

From the package directory:

```bash
python3 -m unittest discover -s tests -v
python3 src/fmp_theme_solver.py --out output --scale 120
```

Optional Perisphere-only envelope preview (requires `trimesh`):

```bash
python3 src/fmp_theme_solver.py --out output --scale 120 --preview-glb
```

## Files

- `data/master_facts.json`: 68 direct exports from `Master_Facts`, with original Fact_ID, status, Code_Drive, source IDs and open issue.
- `data/bim_object_register.json`: stable `TP_ElementID` registry exported from the same workbook.
- `source_refs/`: **read-only historic source snapshots**, SHA-checked workbook and existing Rhino 8 research-preview builder v0.7.0.
- `src/fmp_theme_solver.py`: authoritative computational gate; emits `constraint_report.json`, `game_handoff.json` and optional GLB with receipt.
- `tests/`: regression tests for known geometry, drift, quarantines, status gating, print scale, IDs and Unreal handoff.
- `output/`: tested results from this package generation.
- `WOLFRAM_CROSSCHECK.wl`: Wolfram Language symbolic/numeric independent check.

## What's verified versus conditional

`610 - 480 = 130 ft`, 180-ft Perisphere outside diameter, 72-ft ring girder diameter, 32 meridian truss **count**, 15 horizontal truss **count**, 8 tubular supports, 950-ft Helicline path **length**, and 18-ft deck width are coded as locked facts.

The sphere center at 107 ft above the modeled pool datum follows from the 17-ft clearance **conditional on verifying the pool datum**. The circle/sphere intersections at hypothetical ring girder elevation are **not** historical evidence of its ring girder Z.

The Trylon base width, bridge cross-section/entry Z, Helicline centerline/sweep/grade, ring elevations, support XY/OD, horizontal truss latitudes, shell thickness, 1939 true ground plan XY, and site northing/orientation remain **unresolved**. Provisional 52/64-ft entrances and 270-degree ramp sweep NEVER drive final output.

## Game-development workflow

`output/game_handoff.json` is an **engine-neutral contract**, not an Unreal-imported asset or Game Development Studio approved package. All positions in the contract are **centimeters** as appropriate for Unreal coordinates, while the optional GLB is **meters** and represents only a solid closed sphere envelope for display. Do not assume matching coordinate handedness; conversion is a separate engine adapter responsibility.

The current authoritative working runtime asset is **Theme Center assembled v005** (573 nodes, 558 visible mesh-bearing nodes, SHA `de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439`). This solver adds **constraints and QA overlays without replacing or rebuilding that asset**. The experimental GLB is only a separate analytic comparison envelope, **not** a walkable Perisphere model, not an interior, not evidence of truss geometry, and not physically validated historical wall construction. Collision and navigation are off pending placement and architectural completion.

The Game Development Studio skill requires the local `game-dev` CLI to inspect source geometry, validate provenance/license, build a canonical package, then dry-run project admission. This runtime lacks that CLI. **No CLI validation, canonical vendoring, Blender normalization, GPU render or Unreal import has been performed.** No installed provider or paid service is used.

## Wolfram audit

`WOLFRAM_CROSSCHECK.wl` reproduces the key equations with exact rational arithmetic. Solver code contains numerical guardrails and regression tests, not any invented site coordinates or architectural details. This separation allows independent cross-checks against Wolfram and Rhino/Common or Worldwright geometry engines.

## Data authority

Source workbook exact SHA-256:

`ae7a3f3443e0966e9d1acbb7fc4e8c406328eab80b99976a18f9b1d036c54acb`

The JSON snapshots are frozen exports of that workbook. Future archival changes require regenerated snapshot, a new truth SHA, review, and a revised solver, rather than silently overriding locked fact values.

This package intentionally does not mutate the v0.7.0 Rhino generator. Use the JSON report to reconcile behavior before altering it.

## Current FMP repo integration

The existing project repository is `cameronprops/TheFlushingMeadowProject`, with a 1939/1940 Theme Center assembly v005 in `research/pavilions/theme_center/ASSEMBLED_RUNTIME_v005.json`. The solver should be added as an audit tool (not as a new world model). Maintain GLB **Y-up/metres** for the existing assembly and never substitute the Z-up analytic GLB for the 573-node v005 scene. The contract documents both coordinate conventions explicitly. See `research/pavilions/theme_center/README.md` in the repository.

**Repo checkout:** The complete source workbook and archived Rhino builder are in the linked Drive package, not duplicated as binaries in Git.
