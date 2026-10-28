# Theme Center: lower exit aperture as a conditional door-size anchor — v011

**Date:** 2026-10-27. **Status:** actual historical image observations and hypothetical size tests only. No historical 3D coordinates, doors or stair geometry changed.

## New observation

The user identified an apparently standard-size doorway under the upper staircase in the RIBApix photograph of the Perisphere exit. The image is the 647 × 1,000 px `RIBA9908.jpg` secondary reproduction, decoded in Wolfram with pixel-array SHA-256 `e1ae067b4bbfced3bc31407d1610b322c9197cc5f3360246d530d91e65af29d2`.

**Identification correction:** Based on contemporary visitor-flow descriptions, it is more likely the **lower public Perisphere exit to the bridge** than a dedicated service door. This remains an interpretation, not a verified building-plan label. It is distinct from the upper exit stair, ground entrance under Trylon, and return opening through Trylon. The bottom half is obscured by the foreground glass balustrade. No exposed complete leaf, threshold, or 3D point is visible.

Provisional visual picks, in the **original reproduction's 647×1000 pixel coordinate frame**, ±5 px per selected feature:

| Feature | x | y |
|--|--:|--:|
| Approx upper left | 210 | 351 |
| Approx upper right | 240 | 355 |
| Visible left / railing occlusion | 198 | 387 |
| Visible right / railing occlusion | 229 | 387 |

Observed projected head width = **30.2655 pixels**, head-midpoint to balustrade-midpoint = **35.8922 pixels** (note the side jamb skews). Under a *purely hypothetical same-local-X/Y-scale assumption*, a **36-inch-wide by 80-inch-high** door would project to 67.2566 pixels in full height, with about 53.37% visible above the railing. However, doorway plane/camera foreshortening, glass rail perspective, opening taper/size, and occlusion are unknown. Many common width/height priors from 30 × 80 to 48 × 84 inches also fit the fact that the bottom is hidden. **These conditional scenarios cannot pick a real door size or locate it to 2–3 inches.** The hypotheses are *not verified 1939 dimensional standards*.

## New complementary NYPL photo

A separate NYPL-attributed [bridge image](https://drivingfordeco.com/wp-content/uploads/2019/05/nypl.digitalcollections.5e66b3e8-a654-d471-e040-e00a180654d7.001.w.jpg) was decoded at **582 × 730 pixels**, decoded pixel-array SHA-256 `91a52b7962db3c21789baf32b7ff09edba6442e750445f3e30966881dade6679`. It depicts the bridge in the opposite direction, including glass-panel railings and a **candidate paired recess/portal grouping** at the far structure (likely Trylon-side). These are *not* the same aperture as the RIBA near-sphere doorway unless a separately validated correspondence establishes that fact. The white center split might be a pier, reveal or shadow. Pixel metadata and a rough bounds candidate are registered; no physical sizes accepted.

## Source evidence boundary

- [RIBApix image reproduction and identifying caption](https://drivingfordeco.com/vanished-new-york-city-art-deco-the-trylon-and-perisphere-part-two-1939-1941/). The original RIBApix source rights and negative remain unverified; **photo bytes intentionally excluded** from public repo ZIP.
- Period Alfred J. Dillon *Theme Center* report (May 1939) notes **egress from Perisphere via doors to the return bridge**. However, the same report retains older superseded 700/200-ft overall dimensions, so it does not certify exact doorway dimensions.
- Existing source of truth: `research/pavilions/theme_center/THEME_CENTER_VISITOR_CIRCULATION_CORRECTION_v001.md`, plus v009/v010 observation packages.

## Reproduction, limitations

`python door_scale_gate.py annotations.json SCREEN_REPORT.json`

`python -m unittest test_door_scale_gate.py -v` (**12 regression tests**)

Wolfram independently confirmed 30.26549-pixel top width, 35.89220-pixel partial opening height, and all six illustrative nominal-door scenarios. The image pixels themselves were decoded/inspected in Wolfram, but the source JPEG binaries are not in this package. No original negative, calibrated camera, floor datum, full jamb or staircase nosing has been recovered. No 3D mesh, print master or Unreal runtime changed.

**Next:** original RIBA and NYPL negative plus dated door schedule or as-built floorplan to identify the opening (and paired Trylon recesses). Then solve facade-local camera and outer railing/door/upper stair, with independently held-out points and world-coordinate uncertainty <= 3 inches before promotion.
