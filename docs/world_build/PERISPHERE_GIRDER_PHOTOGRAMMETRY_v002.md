# WF0002 · Drum girder photo calibration screen v002

**Date:** 2026-10-22. **Status:** Implemented, tested; **photometric/metric camera calibration NOT obtained; historic CAD geometry NOT certified**.

## Source and research boundary

Original period construction-photo reproduction: [Driving for Deco drum-girder image](https://drivingfordeco.com/wp-content/uploads/2019/04/Drum-Girder.jpg), displayed/retrieved into Wolfram at 673 × 520 px. Wolfram decoded-pixel SHA-256: `6d5fdba8ff455d0d10c44ed0a404cc318d80d128ac47b0f17d791cfdb860175c`. The article references historical images. **We have not located/permission-cleared the original negative.** Therefore the image pixels are NOT redistributed in this ZIP or Git.

Original period publication: November 1938 *Architectural Record* (Theme Center construction description) states the ring girder is **72 ft in diameter and 8 ft deep**. These are period engineering descriptions, not independent survey of every as-built node. Existing v005 runtime mesh's `Perisphere_Support_Ring` torus was separately measured at **approximately 1.30 ft vertical extent**, with nominal 72-ft centerline diameter; those mesh measurements are **derived**, and the ring's intended engineering role is not proven.

## What changed from v001

1. **Fourteen manually marked points** around the photographed *upper circular rim*, with pixel coordinate origin in the top-left corner, stored in `PHOTO_ANNOTATIONS_v002.json`. The fitted ellipse is approximately **627.04 px major, 261.92 px minor**, aspect 0.418, **24.69° conditional viewing elevation** assuming weak-perspective projection of a horizontal circle.
2. **Five top/bottom approximate vertical stiffener pairs** on the near side. Their recorded height differences are 74, 78, 81, 84, 88 pixels (median **81 pixels**). These point placements were visually reviewed in an annotated *Wolfram preview* but should be remeasured directly on a high-resolution original negative. Image-edge selection is provisional, with 8-pixel annotation jitter in the Monte Carlo screen.
3. Camera distance, focal length, radial lens distortion, precise vertical-vs-horizontal relative scale, and outside-flange versus 72-ft centerline offset remain **unknown**. Therefore `perspective_gain_sensitivity_only` values **1.0, 1.15, 1.3, 1.45, 1.6** are scenarios, **not** calibrated confidence bounds. Independent camera constraints or second same-member view are required.
4. Under the weak-perspective baseline, observed web span / (627 px /72 ft × cos(24.69°)) equals 10.24 ft. At relative near-face gains [1, 1.15, 1.3, 1.45, 1.6] that maps to **[10.24, 8.90, 7.87, 7.06, 6.40] ft**. To explain that pixel height using a 1.30-ft torus requires **7.87×** near-face magnification, versus **1.28×** for the period-reported 8-ft deep drum. This makes a mere 1.30-ft *load-bearing girder* inconsistent with ordinary imaging geometry, without proving the actual structural depth to the inch.
5. The 5%-95% quantiles in `MEASUREMENT_REPORT_v002.json` represent **annotation jitter only, conditional on EACH arbitrary perspective gain scenario**. They are not combined metric confidence intervals and exclude all major systematic uncertainty. Do not report a single as-built measured value from them.

## Reproduce

```bash
python -m pip install numpy opencv-python
python measure_girder_ellipse.py --input PHOTO_ANNOTATIONS_v002.json --out MEASUREMENT_REPORT_v002.json --iterations 2000
python -m unittest -q test_girder_ellipse.py
# Wolfram Language: Get["WOLFRAM_CHECK_v002.wl"]
```

**Validation:** 12/12 Python regression cases passed. Independent Wolfram check matches displayed major/minor axes, conditional depth scenarios and required magnification to rounding. Tests are solver/geometry controls, not a native game-engine test. `game-dev` CLI and Unreal were unavailable; neither was executed.

## Historical workflow

- Historical labels: **Documented period** 72-ft diameter/8-ft depth; **Derived runtime** 1.30-ft torus; **Provisional photographic inference** image ellipse and web height, camera gain.
- No print masters, assembled runtime v005 GLB or Rhino geometry were edited. All geometric release gates remain **false**.
- Next: obtain original high-resolution negative, identify absolute flange/contact interfaces, same-edge top-bottom stiffener pairs, solve camera and intrinsics with independent 3D controls, and validate against second non-identical construction view. Check architectural/structural drawings for exact plate width and node schedule.
