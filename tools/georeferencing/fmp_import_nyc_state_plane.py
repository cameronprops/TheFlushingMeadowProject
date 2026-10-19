#!/usr/bin/env python3
"""Convert FMP EPSG:2263 State Plane US survey-foot observations to EPSG:32118 metres.

Both projections are NAD83 New York Long Island State Plane with identical projection
parameters expressed in different units. Historical datums are NOT handled here.
"""
import argparse
import csv
import math

US_SURVEY_FOOT_METRES = 1200.0 / 3937.0


def convert(rows):
    if not rows:
        raise ValueError("No rows")
    output = []
    for i, r in enumerate(rows, 1):
        if r.get("source_crs", "").strip().upper() != "EPSG:2263":
            raise ValueError(f"Row {i}: require source_crs EPSG:2263")
        if any(k in r and str(r[k]).strip() for k in ("world_x_m", "world_y_m", "crs")):
            raise ValueError(f"Row {i}: meter output fields already populated; refusing overwrite")
        try:
            x, y = float(r["world_x_ftus"]), float(r["world_y_ftus"])
        except (ValueError, KeyError, TypeError) as exc:
            raise ValueError(f"Row {i}: missing/invalid world_x_ftus or world_y_ftus") from exc
        if not (math.isfinite(x) and math.isfinite(y)):
            raise ValueError(f"Row {i}: nonfinite input")
        new = dict(r)
        new["world_x_m"] = f"{x * US_SURVEY_FOOT_METRES:.9f}"
        new["world_y_m"] = f"{y * US_SURVEY_FOOT_METRES:.9f}"
        new["crs"] = "EPSG:32118"
        output.append(new)
    return output


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input_csv")
    ap.add_argument("output_csv")
    args = ap.parse_args()
    with open(args.input_csv, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        original_fields = reader.fieldnames or []
    converted = convert(rows)
    fields = list(original_fields)
    for name in ("world_x_m", "world_y_m", "crs"):
        if name not in fields:
            fields.append(name)
    with open(args.output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(converted)


if __name__ == "__main__":
    main()
