# Historical drawing georeferencing calculator

Input: CSV with columns `id,role,pixel_x,pixel_y,world_x_m,world_y_m,crs`.
`role` is `control` or `check`. Use measured, independent surveyed coordinates in metres and the **same projected CRS** for every record.

Run:
```bash
python3 tools/georeferencing/fmp_georef.py measurements.csv --output transform.json
cd tools/georeferencing && python3 -m unittest -v
```

The script fits a 6-parameter 2D affine transform using least squares, reports control/independent-check RMS errors and emits matrices in metres. A numerical fit is always marked `certified: false`. It will not invent values, reproject CRS, solve vertical datum or determine whether sources are historically trustworthy. A future QA gate should set maximum acceptable holdout residual and certify a fit separately. Source measurements and provenance should be linked to `research/georeferencing/FMP_Control_Point_Register_v0_1.csv`.

Synthetic test coverage: exact affine recovery, collinearity rejection, insufficient holdout rejection. No historical accuracy claim is implied.
