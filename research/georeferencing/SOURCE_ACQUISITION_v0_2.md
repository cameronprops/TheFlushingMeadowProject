# FMP source-image acquisition and control-point digitization

## Milestone: verified access, not completed georeferencing

The source manifest `research/georeferencing/FMP_Source_Scan_Register_v0_2.csv` documents six research leads with era, rights, format, and production priority.

### Confirmed from source-page review (2026-10-18)
- **1939 XM-250:** NYPL identifies drawing XM-250, with public image download options up to 760px; a separate original-scan order option exists. This is a promising primary plan but current web preview is unsuitable for accurate point picking.
- **1939 Hammond fair and approaches map:** NYPL explicitly offers an original raster and indicates likely U.S. public-domain status. The map is a bird's-eye view, not a survey substitute.
- **1939 All Roads Lead to the World's Fair:** original/TIFF offered; planimetric accuracy must be assessed before geometry extraction.
- **1964 Operations Manual:** Sheet 3 and Sheet 4 comprise the two general site plans. Both have a **printed 200-foot scale**. Publisher reports 200dpi digital derivatives and prohibits re-publication without permission. Do not add scans to Git.
- **NYPL engineering/survey records:** a research request remains open; no authoritative world-coordinate correspondence has yet been extracted.

### Capture procedure
1. Select the original image version and write source ID, archival catalog URL, pixel dimensions, rights, and revision to a manifest.
2. Open a **local image** in `tools/georeferencing/FMP_Point_Digitizer_v0_1.html`; for PDF, convert a local personal-reference copy to PNG (do not publish derivative image).
3. If scale bars exist, click their *actual printed endpoints* and record length in feet; local metres per pixel is illustrative only and is not a georeferencing solution.
4. Mark exactly identifiable fixed points and separately tag `control` and independent `check` observations. Preserve their image pixel coordinates with source ID. Recheck against source edition.
5. Enter real, externally established projected CRS coordinates in metres. Never calculate them by reading approximate map graphics or place name coordinates.
6. Export observations CSV (can include blanks). Export solver-ready CSV **only** once there are >=3 non-collinear control points and >=2 independent independent check points with valid projected coordinates.
7. Run `python3 tools/georeferencing/fmp_georef.py measurements.csv --output transform.json` and inspect both in-sample and holdout residuals before review.
8. Keep survey certification and vertical datums as independent engineering gates; all automatically calculated transforms remain **uncertified**.

### Source citation and re-use
- NYPL XM-250: https://old-digitalcollections.nypl.org/items/926ff6bc-5ff8-0931-e040-e00a180628c4
- NYPL Map and Approaches: https://old-digitalcollections.nypl.org/items/b07fa8e0-35d3-0131-4020-58d385a7bbd0
- NYPL All Roads: https://old-digitalcollections.nypl.org/items/b8678170-35d3-0131-ce10-58d385a7bbd0
- 1964 Operations Manual: https://www.worldsfairphotos.com/nywf64/operations-drawings-manual/index.htm
- Operations Manual introduction and rights: https://www.worldsfairphotos.com/nywf64/operations-drawings-manual/sheet-00-introduction.pdf
