# Theme Center Site XY Registration Gate v008

Status: **partially validated** (source identification and synthetic mathematical transform only; historical surveyed XY remains unresolved).

## Existing source geometry
Source: research/pavilions/theme_center/THEME_CENTER_ASBUILT_CONSTRAINTS_v001.json and docs/THEME_CENTER_STAGING.md. 510-node staged GLB, Y-up, meters; local frame only, **not georeferenced**. Never promote model-local XY to surveyed coordinates.

## Primary original survey archive to request
NYPL World's Fair Board of Design: **Box 2389, tubes 13–17** (Grading, Surveying and Plotting Maps), **Box 2387, folder 3** (General Plan), **Box 2389, rolls 10–11** (oversize general plan). Finding aid https://worldsfair.nypl.org/containerlist.pdf

## Verified relative constraint
C_Helicline_XY = C_Perisphere_XY (1939 engineering account). https://www.worldradiohistory.com/Archive-Broadcast-Engineers-Journal/ATE-1939-05.pdf

## Registration process
Acquire as-built common plan with labeled surveyed controls; locate at least 3 matching noncollinear control points; record source/date/datum/CRS/units; measure image pixel coordinates; solve 2D similarity or affine calibration; validate held-out residuals; extract Perisphere and Trylon centers, bridge entrance/exit, and Helicline start bearings; convert to source Y-up meters with reversible transform. Do not confuse 1937 proposals with as-built 1939 plans. Scale and orientation must be validated independently; rectification required for perspective photography.

## Implementation
v008 ZIP generated separately contains `fit_site_xy.py`, `controls_TEMPLATE.json`, and `README.md` with test. Wolfram verified synthetic case: (0,0)->(100,200), (1,0)->(100,300) gives scale=100, rotation=90°, translation=(100,200). This validates transformation algebra, not historic placement.

## Do not change
Trylon height locked 610 ft. Historical master shell and GLB topology/coordinates retained until site control is validated. Bridge/Helicline junction remains provisional.
