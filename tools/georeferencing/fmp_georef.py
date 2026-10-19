#!/usr/bin/env python3
"""Fit raster image coordinates to projected *metre* coordinates.

Source drawing imagery and survey observations must be independently vetted.
This program never asserts historical/survey certification.
"""
import argparse
import csv
import json
import math

# Only metre-based CRS that we have verified for this project's baseline.
# EPSG:2263 is NYC's common NAD83 State Plane CRS but its units are US survey feet.
METRE_CRS = {"EPSG:32118", "EPSG:26918"}


def solve3(m, v):
    a = [list(map(float, r)) + [float(z)] for r, z in zip(m, v)]
    for i in range(3):
        pivot = max(range(i, 3), key=lambda k: abs(a[k][i]))
        if abs(a[pivot][i]) < 1e-12:
            raise ValueError("Singular or collinear control-point geometry")
        a[i], a[pivot] = a[pivot], a[i]
        divisor = a[i][i]
        a[i] = [x / divisor for x in a[i]]
        for j in range(3):
            if j != i:
                factor = a[j][i]
                a[j] = [x - factor * y for x, y in zip(a[j], a[i])]
    return [a[i][3] for i in range(3)]


def fit(rows):
    if not rows:
        raise ValueError("No measurements supplied")
    crs_set = {str(r.get("crs", "")).strip().upper() for r in rows}
    if len(crs_set) != 1:
        raise ValueError("Mixed or missing projected CRS")
    crs = crs_set.pop()
    if crs not in METRE_CRS:
        raise ValueError(
            "Expected projected coordinates in metres (EPSG:32118 or EPSG:26918). "
            "EPSG:2263 uses US survey feet: run fmp_import_nyc_state_plane.py first."
        )
    seen, parsed = set(), []
    for r in rows:
        ident = str(r.get("id", "")).strip()
        role = str(r.get("role", "")).strip().lower()
        if not ident or ident in seen:
            raise ValueError("Point IDs must be nonempty and unique")
        seen.add(ident)
        if role not in {"control", "check"}:
            raise ValueError("Each point role must be control or check")
        try:
            p = {k: float(r[k]) for k in ("pixel_x", "pixel_y", "world_x_m", "world_y_m")}
        except (KeyError, ValueError, TypeError) as exc:
            raise ValueError("Missing or invalid numeric coordinates for " + ident) from exc
        if not all(math.isfinite(v) for v in p.values()):
            raise ValueError("Non-finite coordinates for " + ident)
        parsed.append({"id": ident, "role": role, **p})

    control = [p for p in parsed if p["role"] == "control"]
    checks = [p for p in parsed if p["role"] == "check"]
    if len(control) < 3 or len(checks) < 2:
        raise ValueError("Need >=3 controls and >=2 independent check points")

    # Center/scale pixel coordinates before solving normal equations. Historical
    # PDFs can have very large raster pixel coordinates and tiny physical scales.
    cx = sum(p["pixel_x"] for p in control) / len(control)
    cy = sum(p["pixel_y"] for p in control) / len(control)
    spread = math.sqrt(sum((p["pixel_x"] - cx) ** 2 + (p["pixel_y"] - cy) ** 2
                           for p in control) / len(control))
    if spread < 1e-12:
        raise ValueError("Controls must have spatial extent")

    avg_x = sum(p["world_x_m"] for p in control) / len(control)
    avg_y = sum(p["world_y_m"] for p in control) / len(control)
    m = [[0.0] * 3 for _ in range(3)]
    bx, by = [0.0] * 3, [0.0] * 3
    for p in control:
        v = [(p["pixel_x"] - cx) / spread, (p["pixel_y"] - cy) / spread, 1.0]
        for i in range(3):
            bx[i] += v[i] * (p["world_x_m"] - avg_x)
            by[i] += v[i] * (p["world_y_m"] - avg_y)
            for j in range(3):
                m[i][j] += v[i] * v[j]
    nx, ny = solve3(m, bx), solve3(m, by)
    tx = [nx[0] / spread, nx[1] / spread,
          avg_x + nx[2] - (nx[0] * cx + nx[1] * cy) / spread]
    ty = [ny[0] / spread, ny[1] / spread,
          avg_y + ny[2] - (ny[0] * cx + ny[1] * cy) / spread]

    residuals = []
    for p in parsed:
        xp = tx[0] * p["pixel_x"] + tx[1] * p["pixel_y"] + tx[2]
        yp = ty[0] * p["pixel_x"] + ty[1] * p["pixel_y"] + ty[2]
        dx, dy = xp - p["world_x_m"], yp - p["world_y_m"]
        residuals.append({"id": p["id"], "role": p["role"],
                          "dx_m": dx, "dy_m": dy, "error_m": math.hypot(dx, dy)})

    def rmse(role):
        errors = [p["error_m"] ** 2 for p in residuals if p["role"] == role]
        return math.sqrt(sum(errors) / len(errors))

    return {"crs": crs, "coordinate_units": "metres", "affine_x": tx, "affine_y": ty,
            "control_rmse_m": rmse("control"), "check_rmse_m": rmse("check"),
            "residuals": residuals, "certified": False,
            "note": "Mathematical fit only; independently verify archival provenance, survey datum and holdout accuracy."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv", help="Point digitizer CSV with projected coordinates in metres")
    p.add_argument("--output", help="Write JSON fit (defaults to stdout)")
    args = p.parse_args()
    with open(args.csv, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    result = json.dumps(fit(rows), indent=2) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
