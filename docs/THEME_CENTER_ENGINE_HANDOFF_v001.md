# Theme Center v005: Wolfram + Game Development Studio engineering handoff

**Date:** 2026-10-20. **Scope:** 1939 FMP Theme Center **runtime-only derivative**. This is a first production gate, not a new model or approval of the existing circulation.

## Purpose

Join historical numerical constraints, the source-preserving v005 GLB, and the v004 visitor-route screen into one **read-only, reproducible preflight**. Maintain one artifact lineage rather than rebuilding the Trylon/Perisphere or fabricating historic portal dimensions. The original watertight print assets remain unchanged.

**Active asset**: [Assembled runtime v005](https://drive.google.com/file/d/1OzFZRkHCxN3jMBGwH3Lwdbx0pFJIJhM0/view). Its expected SHA-256 is `de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439` per `research/pavilions/theme_center/ASSEMBLED_RUNTIME_v005.json`.

## Wolfram numerical calculations (performed 2026-10-20)

Inputs are the repository's `THEME_CENTER_ASBUILT_CONSTRAINTS_v001.json`, `SHARED_PORTALS_v004.json`, `RETURN_ROUTE_CLEARANCE_v004.json`, and `HELICLINE_TRANSITION_v003.json`. The Wolfram Language evaluator returned:

| Computation | Output | Evidence boundary |
| --- | ---: | --- |
| F009 + F010 minus F001 | 0.000000 m | Documented 146.304 + 39.624 = 185.928 m, not a mesh measurement |
| Built Trylon height / 0.3048 | 610 ft | Historical constraint, not measured from v005 |
| Built Perisphere diameter / 0.3048 | 180 ft | Historical constraint, not measured from v005 |
| Perisphere radius | 27.432 m | Arithmetic derivative of documented diameter |
| If 32 meridians were equally spaced, angular pitch | 11.25° | Mathematical idealization, not actual installed spacing |
| Corresponding sphere-equator arc pitch | 5.3862606046 m | Theoretical arc spacing, not truss profile verification |
| F058 / 0.3048 | 950 ft | Historical Helicline centerline length, not reconstructed route length |
| F059 / 0.3048 | 18 ft | Historical Helicline deck width, not mesh width |
| v004 preview aperture nominal center-width for 0.3-m body radius | 1.8 m | Width 2.4 m in local Z, depth 3.4 m in local X |
| v004 preview aperture headroom margin for 1.8-m body and 0.05-m floor lift | 0.55 m | Assumes the portal sill coincides with the test floor; not swept clearance |
| v003 transition sampled maximum slope | 6.9312359879% / 3.9649643051° | Inherited model sample; not general Helicline slope or code compliance |

**Important:** v004 reports **435 discrete sampled poses with no reported surface contacts** after provisional cuts. Its algorithm is surface-based, does not detect every solid containment, does not sweep between poses and does not certify native Unreal physics. The 2.4 m portal sizes are **interpretive topology-test parameters**, not historical measurements. The modeled body dimensions are provisional test assumptions, not an accessibility or safety standard.

## Run the read-only Python gate

From repository root, using Python 3.10+ (no third-party dependencies):

```bash
python3 -m unittest -v tools.world_build.test_preflight_theme_center_v005
python3 tools/world_build/preflight_theme_center_v005.py --root .
```

The second command checks source/overlay hash lineage *between manifests*, exact node counts documented by the assembler, built-number consistency, provisional portal envelopes, route status and coordinate conventions. **It does not verify the actual GLB bytes when `--glb` is omitted.**

Once the v005 file has been obtained locally from the linked Google Drive package, run:

```bash
python3 tools/world_build/preflight_theme_center_v005.py \
  --root . \
  --glb /absolute/path/to/FMP_ThemeCenter_Assembled_Runtime_v005.glb \
  --out /absolute/path/to/theme_center_preflight_report.json
```

This independently hashes the exact GLB and checks its glTF 2.0 chunk structure, object count, visible mesh count, disabled source meshes, and persistent node identity. It does **not** prove normal orientation, actual triangle geometry, collision shape, materials in Unreal, GPU performance, or game readiness. The output report explicitly leaves those acceptances false.

The JSON gate lives at `research/pavilions/theme_center/ENGINE_HANDOFF_GATE_v001.json`. The Python entry point is `tools/world_build/preflight_theme_center_v005.py`; its tests are `tools/world_build/test_preflight_theme_center_v005.py`.

## Controlled handoff to Game Development Studio

1. Obtain exact v005 GLB and pass byte-level preflight. Keep the source archive and print geometry immutable.
2. Check local `game-dev` CLI availability and capabilities with the official skill, but do not treat this document as authorization to run an asset-normalization, provider, packaging, adapter-install, project-launch, GPU-capture or vendor-admission command.
3. Plan an asset inspection against this exact SHA-256; diagnose any technical changes needed. Prefer **no-op** normalization when valid.
4. Before any file writes/process launches, obtain authorization for the exact invocation, resolved input and destination. Do not use paid model-generation providers unless separately requested and authorized with a spend ceiling.
5. Validate and package a **derivative runtime asset** with manifest, stable IDs, hashes, rights and provenance, then dry-run project admission. Copy into Unreal only after specific admission approval.
6. In a real Unreal PIE build, confirm `[X,Z,Y]*100` preview conversion, object identity, material orientation, configured character capsule, collision and continuous travel through the entrance/escalators, two viewing levels, upper stairs/lower bridge, Trylon return and Helicline. Native import and actual visitor tests remain **NOT TESTED** until their own run evidence exists.
7. Capture repeatable scene telemetry/render frames only after an engine adapter and actual engine build exist. Performance optimization requires a measured baseline; do not invent FPS, draw calls or route completion percentages.

**Unresolved historical engineering:** 1939 portal dimensions, support/brace reframing, bridge levels, rail returns and perimeter site registration. Don't use an offline clearances report to overwrite the historical evidence state.

## Next executable gate

Obtain `FMP_ThemeCenter_Assembled_Runtime_v005.glb`, check its exact SHA, run the byte-level preflight, inspect with a configured Game Development Studio runtime, then test actual Unreal import and body-volume navigation. If runtime absent, retain **NOT TESTED** and continue building evidenced fairground geometry.