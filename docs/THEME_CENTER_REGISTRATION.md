# Theme Center: source review and registration

## Source review, 2026-10-18

| Archived ID | Reviewed catalog evidence | Permitted use at this stage |
|---|---|---|
| SRC0003 | NYPL general plan, drawing XM-250, image nypl_mss_913. Catalog creation range 1935–1945; booths and entrances identified in red. Rights status inconclusive. | Primary plan lead. Drawing revision, scale and built-state date still require image review. Not a measured 1939 footprint. |
| SRC0004 | Hammond map of fair and approaches, image 5072220, catalog range 1939–1940. NYPL explicitly classifies it as a bird's-eye view and believes it public domain in the US. | Orientation and visual context; exclude from metric control fitting unless geometry is independently justified. |
| SRC0005 | Dolph & Stewart, All roads lead to the world's fair: map of site and environs, image 5072222. Catalog range 1939–1940, 22 by 34 inches. NYPL believes it public domain in the US. | Candidate regional reference; scale, projection and control suitability not yet inspected. |

Source pages:
- https://old-digitalcollections.nypl.org/items/926ff6bc-5ff8-0931-e040-e00a180628c4
- https://old-digitalcollections.nypl.org/items/b07fa8e0-35d3-0131-4020-58d385a7bbd0
- https://old-digitalcollections.nypl.org/items/b8678170-35d3-0131-ce10-58d385a7bbd0

The two 2560-pixel download attempts returned HTTP 502. The NYPL finding aid and
container-list requests returned HTTP 403. The June 1939 Architectural Forum PDF
exceeded the web reader's size limit. Those failures do not mean the originals
are unavailable elsewhere. No high-resolution original was acquired or measured.
Archived source CSVs remain unchanged; this document records the newer review.

## Implemented alignment tool

`tools/fit_site_registration.py` fits translation, uniform scale and rotation
from paired 2D controls. It reports each residual, fit/check RMSE, maximum errors
and the inverse transform. It does not fit perspective distortion or shear.

Input header:

```csv
control_id,source_x,source_y,target_x,target_y,role
```

Supply at least three distributed, non-collinear `fit` controls and at least two
independent `check` controls. The latter are never used to estimate the transform.
Coordinates must share deliberate axis conventions: convert image-down Y to
map-up Y before using an orientation-preserving fit. Keep source pixel dimensions,
crop and any Y inversion in the control provenance. Never silently mirror a plan.

Example command, using your reviewed inputs and project-selected tolerance:

```bash
python tools/fit_site_registration.py controls.csv \
  --source-ref SOURCE_RECORD_AND_DRAWING_REVISION \
  --target-crs DOCUMENTED_PROJECT_CRS \
  --target-units m --tolerance 0.25 --output out/registration.json
```

The example tolerance is illustrative, not an accepted FMP accuracy requirement.
`WITHIN_LIMIT_WITH_CHECKS` means only that the supplied coordinates satisfy the
chosen residual limit. Every output retains `survey_verified: false`. A script
cannot certify point identity, independent measurement or historical suitability.

The tool rejects duplicate IDs, invalid coordinates, degenerate fit controls and
collapsed solutions. It keeps outliers visible. No point is silently discarded.
It performs no projection conversion, terrain reconstruction or vertical shift.

## Next evidence needed

1. Legible source drawing with date, revision, scale and dimensions.
2. Documented target CRS and measured control coordinates, with source/date/units.
3. Control correspondences and independent check points around the Theme Center.
4. Source-specific uncertainty and a justified project residual tolerance.
5. Separate historical elevation evidence before placing foundations or circulation.

No site origin, elevations or physical Theme Center placement has been invented.
Seventeen tests pass, including known synthetic rotation/scale, inverse recovery,
independent check failure and invalid-control rejection. Real-site fitting remains
pending acquisition and review of control data.
