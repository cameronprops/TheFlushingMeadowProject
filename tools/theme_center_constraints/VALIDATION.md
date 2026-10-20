# Validation receipt (2026-10-20)

Scope: local standalone solver only; no external host Unreal or GPU runtime.

- Imported BIM-ready truth workbook with `artifact_tool`; source SHA-256 matches pinned expected hash.
- Exported 68 facts and 75 BIM object-register records, without modifying the workbook.
- Wolfram Language independent computation confirmed 610 − 480 = 130 ft, sphere radius 90 ft, sphere center 107 ft relative to water datum *conditional*, and hypothetical intersection heights 24.5136374908 / 189.4863625092 ft.
- 12 standard-library unittest cases passed, covering data drift, provisional locks, geometry underdetermination, verified scale, unit conversion, unique BIM IDs, Unreal-handoff flags.
- Generated 60 uniquely registered solver elements; 59 have insufficient geometry for full as-built mesh modeling. This is **not** a percent-complete metric for the actual 573-node assembled v005 model.
- Validated analytic Perisphere-only GLB manifold topology with trimesh `is_watertight` and `is_winding_consistent`; this is neither the game's working model nor the print master.
- Existing assembled runtime v005 in FMP GitHub dossier remains the target scene. No v005 binary was present in this environment; no v005 mesh-level solver comparison performed.
- `game-dev` CLI unavailable (`command not found`); no canonical package build/vendoring, Unreal PIE, GPU visual tests, navigation, or performance certification.

Open gates: compare full 573-node runtime v005 against the solver's geometry facts, resolve historical apertures/route controls, and validate real Unreal scale/collision once available.
