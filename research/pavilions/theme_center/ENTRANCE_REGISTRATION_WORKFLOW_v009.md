# FMP 1939 Theme Center — Entrance registration / stairs v009

**Status (2026-10-27):** first source-chosen workflow + reproducible **read-only** stair/uncertainty gate. **No new as-built entrance placement, camera pose, or historical stair measurements have been certified.** This does not change the historical master, v005/v008 runtime GLB, or print meshes.

## We are solving eight separate architectural objects, not a single doorway

| Object ID | Historical function | Primary evidence | Next measured output |
|---|---|---|---|
| WF0001-ENTRY-GRADE | Ground-level entrance canopy, lettered sign, doorway | Gottscho Met 1987.1100.403 (CC0) | facade plane and portal jamb points in common 1939 site frame |
| WF0001-TURNSTILE | Ticket-control / turnstile threshold | NYPL turnstile original (secondary image ID found) | interior relative plan/alignment to entrance |
| WF0001-LOBBY | Aluminum-lined entrance lobby | Wurts Bros. May 1939 attributed photograph | actual planes, escalator origin centres |
| WF0001-ESC-A and B | Two **upward** escalators in enclosed lower bridge chamber | lobby photo, New Yorker firsthand report | start/end floor elevations, width, slope, enclosed bridge side/underside |
| WF0002-IN-LOW / WF0002-IN-HIGH | Distinct entrance apertures on Perisphere | period diagram, two escalator paths | two different 3D doorway centres; no direct conversion of plan figures to as-built |
| WF0002-OUT-LOW / WF0002-OUT-HIGH | Perisphere exit apertures | RIBApix source image and NYPL diagram | lower direct bridge connection; upper-to-bridge stair connection |
| WF0002-RETURN-BRIDGE | **Open** upper bridge over enclosed escalators, smooth concave outer soffit | Met/Gottscho full-res + bridge period closeup | actual deck edges, curvature, rail height/columns, ends |
| WF0001-RETURN-HELICLINE | Return portal **through Trylon** to descending ramp | as-built oblique views and turn/landing source | continuity to 18-ft wide, 950-ft route to verified ground grade |

Keep **the ground-level `PERISPHERE ENTRANCE` canopy** separate from elevated return portals and from the stair. No made-up decorative Art Deco arch; historic photographs show a smooth, continuous undersurface.

## Selected pictures and film timecodes

The machine-readable [shotlist](research/ENTRANCE_SOURCE_SHOTLIST_v009.json) ranks these six **actual photographs/period diagrams**: E01 MET/CC0 Gottscho 1987.1100.403 (3138x3847) for ground entrance/lettering and bridge soffit; E02 Met Gottscho 1987.1100.404 (2506x3808) for second sightline; E03 NYPL turnstiles (674x526 secondary reproduction); E04 1939 Wurts Bros. lobby/escalators (443x550 reproduction; original source/attribution needs reconciliation); E05 NYPL labeled circulation diagram (diagram, NOT survey); E06 RIBApix original bridge/exit staircase photo lead (`RIBA9908`, exact catalog source needs verification).

**Actual movie candidate M01**: already FMP-decoded Philip Medicus Reel 4 Part I at 00:01:30, 00:02:10, 00:02:20, 640x480 derivative. These are distant exterior/context frames **NOT doorway or stair measurements**. M02 Smithsonian Orth *Home Movie I* has promising catalog construction/aerial content but its video has **not been acquired**; no timecodes invented. M03 is a short 62-second Prelinger excerpt, but no entrance features timecoded. **Do not hallucinate film frames or apply image-enhancement algorithms to invent linework.** Prior 640px frame SHA inventory: `research/pavilions/theme_center/MEDICUS_REEL4_PARTI_HD_FRAME_SURVEY_v002.json`.

### Practical screenshot selection

1. Digitize E01 at original 3138px width: crop only for inspection (save original unchanged). Mark entrance lettering baseline; exterior jamb and threshold; canopy slab/edge; Trylon planar corners; bridge spring/soffit intersections. Record individual pixel XY uncertainties and source scan SHA. **Do not extrapolate lettering as a doorway width.**
2. Match E01 against E02 and original Gottscho negatives and use visible, physically anchored Trylon faces and Perisphere shell as control candidates. At least **six genuine non-coplanar 3D↔2D correspondences and two independent held-out features per camera**. AABB corners from a synthetic GLB are not real observed landmarks.
3. Source original E03–E04 archive negatives. Mark turnstile posts, lobby wall-plane corners, escalator landing edges and rail intersections. Use SIFT/LightGlue/COLMAP tracks only as **proposals**, requiring visual approval of stable architectural features. Film grain, moving people, lens distortion, cropping and repeated steelwork can produce false matches.
4. E05 is a **topology validator**: separate entry and exit and use preliminary elevations **only as hypotheses**, not as a measured as-built plan.
5. E06 plus period upper/lower exit photos are the **stair priority**. Mark the upper threshold, each clearly visible nosing, bottom landing, guard edges and return bridge deck. The upper platform's staircase is **not** one of the two entry escalators.
6. Sample M01 scenes for distant site orientation/foreground geometry only. For newly acquired film, preserve raw frame number, source fps/telecine aspect ratio, original/noisy frame and any stabilization transform; choose sharp frames with distinct camera translation/parallax, not just consecutive near-identical images.

## Registration and machine-learning pipeline

**A. Archival ingestion.** Collect original file URI and bytes where rights permit; hash immutable original scans/video; document creator/capture date vs upload date and 1939 vs 1940. Store high-res original and rights metadata to Drive; do not repost restricted scans to public Git. Preserve machine-selected crops and original-to-crop transforms.

**B. Camera & scale.** Use surveyed 1939 site controls, as-built footprint/survey or dimensioned late-stage plan. Lock the known final 610-ft Trylon/180-ft Perisphere against early 700/200 publicity. For each view initialize focal length/intrinsics from scan/film provenance where possible; solve PnP with RANSAC followed by bundle adjustment (OpenCV/COLMAP/pycolmap), use actual 3D building corner points (or triangulated points cross-supported in multiple views), and keep 2+ landmarks *outside* the fitting set. Log per-feature pixel residuals, camera uncertainties, principal point/crop/lens-distortion uncertainty, condition number and whether degeneracy/planarity exists. Single-image scale without a ground-control datum **cannot locate entrances to the inch**.

**C. Frame/feature extraction.** Detect line segments and keypoints, use feature matching (SIFT, SuperPoint/LightGlue) to propose rails, jambs, corners and edges, semantic segmentation for sky/people/crowds to exclude transient evidence; manually accept source-backed feature IDs. For each opening, intersect image rays with documented facade/plane or stable curved spherical surface. If no known facade plane or second calibrated view, only record a ray/screen silhouette and its uncertainty: **not a 3D door location**.

**D. Solve as a constrained network.** Wolfram optimizes shared world points, Trylon 3-sided planes, 180-ft spherical shell, level differences, bridge boundaries, two escalator centerlines, upper stair and lower direct exit. Minimize weighted reprojection error with hard locks only for verified controls; optimize proposed/derived coordinates with intervals and explicit priors. Verify both external approach/entry and elevated return portals in the same site frame. Keep **two** independent camera sets or survey-and-photo cross-check before releasing an as-built placement.

**E. Model in reversible CAD.** New `WF0001_Public_Entrance`, `WF0001_Lobby`, `WF0001_Escalator_A/B`, `WF0002_Low/High_Entry`, `WF0002_Low/High_Exit`, `WF0002_Exit_Stair`, `WF0002_Return_Bridge`, and `WF0001_Helicline_Return` families, with separately tagged surface/truss/trim/rail/collision. Maintain source-control transforms and as-built vs provisional layers. Derive Unreal/GLB runtime overlays from editable Rhino/Worldwright masters; never overwrite v005/v008 archival originals.

**F. Site and guest continuity QA.** Geometry-to-geometry swept capsules for 1.8 m bodies through entrance, stair, bridge, return turn, ramp; inspect discontinuities, nosings, soffit/ceiling clearance, rail endpoints, thresholds, self-intersections, duplicate surfaces and collision. Run native Unreal pawn traversal after importing. Existing v008 **375/375 tread/landing support rays** validate only discrete support, not full headroom, structural fitness, accessibility or native Unreal behavior.

## User's 2–3-inch target: an evidence gate, not a presumed result

Track separate X/Y/Z and width/height 95%-bound budgets with **control datum, camera, source distortion, human/ML annotation, and model-registration components**. Unknown values BLOCK inch-level approval. A conservative aggregate is the sum of component bounds; an actual calibrated statistical covariance model may supersede only if documented. A 2–3-inch feature tolerance may be realistic from a **dimensioned original plan**. For photos without a measured site datum or clear second view, do not promise it; preserve inch-integer arithmetic only when the original drawings substantiate it.

## Concrete stair candidate screen, **not** as-built validation

A period visitor guide describes two Perisphere **entrance** heights as 64 and 52 ft above grade. The 12-ft difference is a **proposal-era hypothesis** and need not equal final upper exit-stair rise. Existing v008 provisional return stair is 23 risers with nominal 0.15902610 m rise and 0.29662197 m going, ~28.1968° pitch. **Wolfram confirmed** 23×rise≈12 ft, and the existing modeled bridge-to-upper landing vertical separation is 145.2 inches, **1.2 inches greater** than the proposal's 144 inches. That happens to fall inside 2–3 inches but DOES NOT mean the historical stair is registered: both values were inherited from prior modeled hypotheses.

Candidate riser counts for a 12-ft drop: 20→7.20", 21→6.857", 22→6.545", **23→6.261"**, 24→6.00". The 23-riser solution is therefore geometrically reasonable **as a prototype**, with actual stair count, nominal section profile, continuous vertical landing positions and historical envelope not yet measured. Do not round its as-built risers to neat imperial sizes just because period construction used inches.

The Helicline is a **descending ramp** rather than stairs. If the bridge departs at 52 ft and the continuous 950-ft centerline descends to its own grade datum, the conditional mean drop/run ratio is 52/950 ≈ **5.47%**. This is a global plausibility example, not a measured historical ramp grade/segment slope; its actual varying slope, elevation datum and landing must come from plans.

## Reproduction

`python tools/entrance_stair_gate_v009.py > reports/STAIR_SCREEN_v009.json`

`python -m unittest discover -s tests -p 'test_*.py' -v`

This workflow reuses existing `tools/world_build/solve_theme_center_photo_pose_v001.py`, `tools/portal_approach_v008`, `tools/stair_run_review_v008`, `tools/portal_finish_v007`; it **does not duplicate or replace** their working geometry or previous body/mesh QA.

**Work completed here:** source discovery, distinct portal/flow contract, chosen shotlist, numerical screens and regression tests. **Still blocked:** original NYPL/RIBA negative acquisition, real entry-camera calibration and independently surveyed entrance points; all exact as-built geometry promotions, screenshots with unverified licensing, and native `game-dev`/Unreal. The `game-dev` binary is unavailable in the current container.
