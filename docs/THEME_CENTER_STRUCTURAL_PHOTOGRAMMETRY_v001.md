# Theme Center structural/photo solver v001

**Date:** 2026-10-20. **Scope:** Read-only historical engineering constraint checks, idealized truss calculations, and planar film/photo registration. Existing 510-node staging GLB and assembled v005 asset remain unchanged.

## Why this exists
The 1938 Institution of Structural Engineers describes **approximately 39 column lengths per each Trylon leg**, with diagonals/struts below the 480-ft transition and a 130-ft plate structure above. This DOES NOT specify 39 equally spaced truss bays or permit a fully inferred historical steel skeleton. The Perisphere's 32 meridians, 15 horizontal trusses, eight support columns and 72-ft ring girder diameter are documented, but actual horizontal ring elevations and steel connections are unresolved. Helicline tubular supports vary in spacing and dimensions. No automatic array of identical columns or equal bay heights is historically authorized.

## Working source files
- `tools/world_build/theme_center_structural_solver.wl` : Wolfram structural audit, conditional constant-radius ramp, and planar projective photo fit.
- `tests/theme_center_structural_solver_tests.wl`: 10 regression checks, real FMP constraint JSON plus synthetic photo controls.
- `research/pavilions/theme_center/STRUCTURAL_EVIDENCE_REGISTER_v001.json`: primary source pointers, explicit zero-image-measurement state, frame annotation contract.
- Authoritative built dimensions remain in `THEME_CENTER_ASBUILT_CONSTRAINTS_v001.json`. This addition **does not override** existing 2026-10-20 `preflight_theme_center_v005.py` game-engine gate.

From repository root, with Wolfram installed:
```wolfram
Get["tools/world_build/theme_center_structural_solver.wl"];
facts = Import["research/pavilions/theme_center/THEME_CENTER_ASBUILT_CONSTRAINTS_v001.json", "RawJSON"];
FMPStructuralAudit[facts]
FMPHeliclineHypothesis[270, 52] (* DEMONSTRATION ONLY: 52-ft drop NOT verified *)
```
Run tests:
```sh
wolframscript -file tests/theme_center_structural_solver_tests.wl
```

## Interpreting outputs
- `DOCUMENTED_COUNTS_AND_DIMENSIONS_CONSISTENT`: dimensional/era/status records agree with whitelisted source facts. **Not** proof that v005 mesh steel topology matches photographs or that complete as-built framing is known.
- `HYPOTHESIS_ONLY`: conditional path-length model, using arc length `sqrt[(radius*sweepRadians)^2 + drop^2] = 950ft`. Assumes a single constant-radius 3D helix and uniform grade. Neither assumption is proven.
- `IMAGE_TO_PLAN_FIT_REVIEW_REQUIRED`: homography connecting known **coplanar** plan points (feet) to image pixels. Requires at least four control points that produce a full-rank system. Results include pixel RMS and per-control residuals.
- Planar homography **cannot** reconstruct true 3D truss endpoints, camera pose, support heights or geodetic coordinates. Those require camera calibration, noncoplanar controls/multiple views and uncertainty propagation. Retain underlying calibration controls, not just a best-fit transform.
- `BLOCKED` and `DEGENERATE_CONTROLS`: reject downstream geometry promotion. Film pixels are not source of truth without recorded frame/timecode, lens context and measured points.

## Next evidence capture
1. Open period 1939/1940 views linked in `STRUCTURAL_EVIDENCE_REGISTER_v001.json`, compare visible features to 1938/1939 structural descriptions, and record original versus derivative-resolution rights/quality.
2. For a photographed **planar site feature**, identify >=4 actual known plan control points; store associated stable IDs, frame timecode, pixel coordinates and individual uncertainties. Run `FMPPhotoPlanFit` only on real annotations, inspect residuals and reject ambiguous geometry. Keep plate transition / bracing observations independent.
3. For truss nodes/Helicline column positions use a camera model with multi-view control and parallax. Do not treat the current homography as a 3D solution.
4. Export reviewed results as a derived overlay retaining TF/TP IDs, source status, image residuals and model-local frame. Do not edit original 3D print master or overwrite v005.
5. Game Development Studio: source inspection -> normalization plan -> separately authorized packaging -> asset vendoring dry run -> separately authorized Unreal admission and native clearance checks. This solver delivers **source-constrained notes and data only**, not GPU evidence, Unreal import, or a vendored game asset.

## Tested / not tested
Wolfram evaluator executed the **committed source text** with the checked-in regression tests plus the repo's current JSON constraints: **10 passes, zero failures** on 2026-10-20. The camera-fixture fit uses synthetic points, not actual Prelinger or Library of Congress film frames. Local Game Development Studio CLI and Unreal runtime were not executed. Pending source acquisition: NYPL engineering files (Helicline stability, foundations and superstructure; Theme Center steel plans); independently date 1939 vs 1940 photographs. No frame analysis or exact support positions are claimed.

## 2026-10-20: Source probe and independent image holdout gate v002

- Executed **Wolfram `Import[URI,"Image"]`** against two Library of Congress official JPEG derivatives and decoded them successfully: [LOC 2018750315](https://www.loc.gov/item/2018750315/) at **560 x 384 px** (1939 or 1940) and [LOC 2018750258](https://www.loc.gov/item/2018750258/) at **560 x 385 px** (1940-10-27). Image bytes were not retained or archived by this change. LOC lists *no known restrictions on publication*, subject to its full rights guidance. See `source_probe_v002` in the evidence register.
- The 0315 image shows the finished Helicline deck/rail and tubular supports in an oblique view. It is useful for locating *candidate visible features*, but is **not** a calibrated drawing. The 560-pixel derivative is not adequate grounds for claiming exact support sizes or millimetre accuracy.
- `tools/world_build/theme_center_image_quality_gate_v002.wl` adds a **fit/holdout separation** atop `FMPPhotoPlanFit`, requires at least four independently identified planar fit points **plus two held-out points**, checks duplicate IDs, source provenance, coordinates, positive pixel uncertainties, image bounds, and rejects a projective fit with >6 px or >3-sigma holdout error. These tolerances are screening policy, not historical measurements. Even passing data is flagged `HOLDOUT_PASS_REVIEW_REQUIRED` and `model_update_allowed=False`.
- `tests/theme_center_image_quality_gate_tests.wl` includes ten deterministic synthetic regression checks: clean registration, held-out residual, lack of auto-promotion, synthetic outlier rejection, incomplete holdout rejection, coordinate mislabeling, duplicate IDs, outside-image point and impossible uncertainty. The full v002 cases **10/10 passed** in the Wolfram evaluator.
- There are still **zero** surveyed pixel-to-plan annotations and **zero** triangulated structural points. Prelinger footage has not been frame-extracted, and no as-built structural geometry is certified. Photo registration here concerns the planar XZ ground projection in a Y-up local model, **not** true 3D camera calibration or site georeferencing.

Next concrete operation: obtain a high-quality dated construction image or a suitable Prelinger frame, annotate distinguishable **known** landmarks with coordinate source and pixel uncertainty, set aside two holdout landmarks, calculate independent pixel reprojection errors, then compare proposed truss/support locations with a second viewpoint. Preserve all original image/source versions and do not edit print masters or v005 GLB on the basis of a single uncalibrated frame.
