# FMP historic map alignment: first-pass control register

## Purpose
Create a reversible documented transformation from historical 1939/1940 and 1964/1965 source drawings into the *same* modern projected coordinate system. This is a CONTROL-POINT RESEARCH REGISTER, not a completed survey.

## New evidence found
- NYPL 1939 General Plan (XM-250), site plans, catalog image nypl_mss_913: https://old-digitalcollections.nypl.org/items/926ff6bc-5ff8-0931-e040-e00a180628c4
- 1964/65 Operations Drawing Manual: sheets 3 and 4 are General Plan sheets 1 and 2 of 2: https://www.worldsfairphotos.com/nywf64/operations-drawings-manual/index.htm
- NYPL Board of Design container list calls out archival Grading, Surveying and Plotting Maps in Box 2389, Tubes 13-17: https://worldsfair.nypl.org/containerlist.pdf
- NYPL World's Fair 1939/40 collection finding aid: https://archives.nypl.org/mss/2233

## Research output
`FMP_Control_Point_Register_v0_1.csv` provides candidate common control features, all explicitly UNMEASURED. None is yet accepted as a fixed shared survey landmark. No coordinates or source pixel measurements have been invented.

## Operational acceptance gates
1. Acquire adequate-resolution plan scans and record exact issue date, revision, original scale, original orientation, scan width and height, rights, and file hash.
2. Determine whether any published 1939 or 1964 drawing carries survey monument numbers, grid labels or a projected coordinate system. Seek surveyed *point* locations, not merely visual landmarks.
3. Open NYPL Box 2389 Tubes 13-17 as a retrieval request for grading and survey records, subject to NYPL availability.
4. Establish modern basemap projected CRS by explicit code and datum, then separately handle historical vertical elevations and datum conversions.
5. Record at least 3 non-collinear surveyed correspondences and use at least 2 more independent check points. More control points are preferable across entire fairgrounds.
6. Solve least-squares similarity/affine transform (as warranted by scan distortion). Report per-control residuals and independent hold-out error in meters. Do NOT default to rubber-sheeting that conceals source error.
7. Certify horizontal alignment only after independent evidence corroborates the fit; vertical models require separately validated elevation datum and site grading.
8. Publish matrices, residual CSV and source URLs in Git. Store legally acquired raw plan scans in Drive and record their hashes/rights separately. Never commit scans without a license review.

## Dataset semantics
- `source_pixel_x_*` and `source_pixel_y_*`: measured source-image pixel locations from the exact version identified in manifest; blank until measured.
- `world_x_m`, `world_y_m`: accepted modern projected CRS coordinates; blank until sourced.
- `crs`: obligatory when world coordinates filled.
- `confidence`: current hypothesis strength, not measured positional accuracy.
- `verification_status`: UNMEASURED, MEASURED, CROSSCHECKED, ACCEPTED, REJECTED.
- `current_survival`: records physical continuity of a feature, not proof of fixed geometry.

## Roadmap impact
Shared coordinates enable the 1939/1940 and 1964/1965 reconstructed worlds to load at the same real-world location. A later modern park world and four future-world locations can all reuse this basis. The 2039 and 2064 worlds remain fictional in two continuous branches, and must not contaminate the historical evidence layers.
