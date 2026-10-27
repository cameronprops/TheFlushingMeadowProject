# WF0028 entrance reconstruction workflow v028 — 2026-10-27
Status: SOURCE SELECTION AND WORKFLOW DESIGN. No original film frames yet extracted, camera calibration performed, stairs measured or historical wall geometry corrected.

## Priority sequences (actual archival footage embedded)
1. Science & Education / Hippocrates entrance, intersection Avenue of Patriots and Hamilton Place. 1939 Meière film, Archives of American Art: https://www.hildrethmeiere.org/commissions/new-york-1939-worlds-fair-medicine-and-public-health-science-and-education-building-complex-entrance-facing-intersection-of-the-avenue-of-patriots-and-hamilton-place
2. Avenue of Patriots entrance / Primitive Man and Civilized Man: https://www.hildrethmeiere.org/commissions/new-york-1939-worlds-fair-medicine-and-public-health-science-and-education-building-complex-entrance-facing-the-avenue-of-patriots
3. Curved courtyard mural facade: https://www.hildrethmeiere.org/commissions/new-york-1939-worlds-fair-medicine-and-public-health-science-and-education-building-complex-facade-facing-courtyard
4. Annotated historic scale model locating all mural sites: https://www.hildrethmeiere.org/commissions/new-york-1939-worlds-fair-medicine-and-public-health-science-and-education-building-complex-southwest-and-south-facades
5. LOC Gottscho–Schleisner photograph: https://www.loc.gov/pictures/item/2018750371/
6. Smithsonian Meière film context: https://www.aaa.si.edu/blog/2015/12/artist%E2%80%99s-home-movies-hildreth-mei%C3%A8re-and-the-new-york-world%E2%80%99s-fair
7. Architectural drawing holdings NYSL Box 5 Folder 11; NYPL C2.3 Box 206 Folder 10, actual scans needed.

## Execution
Acquire permission/scan files, record byte hashes and frame timing; select 8–20 candidate stills per entrance with camera movement and high-visibility static architectural landmarks. Trace points, camera uncertainty and edge reliability. Register dimensioned building floorplan to fairground shared controls. Solve camera intrinsics/extrinsics and lens distortion via OpenCV/SfM and use bundle adjustment, robust outlier rejection and Wolfram constraint/error checks. Use at least two independently useful views with parallax; 6+ landmarks distributed across the feature, hold back independent points and at least one full view from solving. Reproject editable Rhino/GLB curves, entrances and door frames and record in-sample and holdout pixel residual + 3D uncertainty. Test circular versus multi-segment curves; do not confuse sculptural ribs with structural walls.

## Accuracy gate
Measured drawings can potentially support +/- 1 inch for specifically dimensioned details. Two to three inches is an aspirational relative-geometry tolerance only when full camera + site-registration error is quantified; cannot promise it from a single photo. Whole-inch drafting conventions do not guarantee as-built or measurement accuracy. Wolfram verified illustrative scenario: 21 ft relief spanning 700 px gives 0.36 in/px locally, 2 px edge error ~0.72 inches before scale, camera/lens, scan, facade-depth and positioning uncertainty. The documented 14 x 21 ft relief dimensions are approximate, not a metrology certificate.

## Stair/grade process
First locate historical finished floor and door threshold; register pavement/curb/landing spot elevations and photos. Determine step count from multiple views, total rise from dated section/site survey, then calculate equal nominal rise H/n and treads from calibrated perspective or plan. Confirm riser uniformity, door swing and landing clear depth, actual grade closure, path connections and railings. Do not apply modern accessibility rules to historical master; simulated Unreal collision/accessible routes are separate. No stair geometry may be marked verified without an elevation datum.

## Acceptance
Before replacing any part of v026/v027 model, require source IDs, frame coordinates, per-point residuals, plan coordinate frame, camera parameters, independent holdout errors and explicit uncertainty. Preserve as-is v004 historic/provisional editable master and all alternatives; promote ONLY validated local components. Rights-restricted images linked only pending licensed originals. No invented timestamps, precise plan coordinates, stairs or radii.
