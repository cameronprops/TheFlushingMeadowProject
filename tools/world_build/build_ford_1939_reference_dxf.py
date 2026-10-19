#!/usr/bin/env python3
"""FMP 1939 Ford Exposition: period-tagged, metre-based, INTERPRETIVE plan DXF.

Run in a checkout with ezdxf installed:
python3 tools/world_build/build_ford_1939_reference_dxf.py \
  --output out/Ford_1939_Reference_Plan.dxf

Reads the committed parameter preset. Not a historically surveyed as-built plan.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRESET = ROOT / "research/pavilions/ford/FORD_1939_PARAMETRIC_BUILD_PRESET_v001.json"

def write_reference_plan(preset, filename):
    import ezdxf
    if preset.get("schema") != "fmp.ford1939.parametric-preset.v1":
        raise ValueError("Unexpected Ford parameter schema")
    if preset.get("building_id") != "WF0014" or preset.get("certified") is not False:
        raise ValueError("Expected uncertified 1939 Ford project")
    doc = ezdxf.new("R2010")
    doc.header["$INSUNITS"] = 6  # metres
    for name, color in [
        ("FORD_PERIOD_DOCUMENTED", 4),
        ("FORD_ESTIMATED_ENVELOPE", 30),
        ("FORD_INTERPRETIVE_ROAD", 8),
        ("FORD_INTERPRETIVE_SHOW", 9),
        ("FORD_NOTES_AND_REFERENCES", 7),
    ]:
        doc.layers.add(name=name, color=color)
    msp = doc.modelspace()
    I, D = preset["interpretive"], preset["documented"]

    def circle(center, radius, layer):
        if float(radius) <= 0:
            raise ValueError("Circle radius must be positive")
        msp.add_circle(center, float(radius), dxfattribs={"layer": layer})

    def rectangle(geo, layer):
        cx, cy = [float(v) for v in geo["center_xy_m"]]
        w, h = float(geo["width_m"]), float(geo["depth_m"])
        if min(w, h) <= 0:
            raise ValueError("Invalid proxy plan size")
        msp.add_lwpolyline([
            (cx-w/2, cy-h/2), (cx+w/2, cy-h/2),
            (cx+w/2, cy+h/2), (cx-w/2, cy+h/2),
        ], close=True, dxfattribs={"layer": layer})

    def note(x, y, message, height=1.5):
        msp.add_text(message, dxfattribs={
            "layer": "FORD_NOTES_AND_REFERENCES",
            "height": height, "insert": (x, y)
        })

    rectangle(I["industrial_hall"], "FORD_ESTIMATED_ENVELOPE")
    rectangle(I["entrance_hall"], "FORD_ESTIMATED_ENVELOPE")
    rectangle(I["garden_court"], "FORD_ESTIMATED_ENVELOPE")

    cx, cy = [float(v) for v in I["cycle"]["center_xy_m"]]
    diameter = float(D["turntable_diameter_m"]["value"])
    radius = diameter / 2
    circle((cx, cy), radius, "FORD_PERIOD_DOCUMENTED")

    for r in I["cycle"]["tier_radii_m"][1:]:
        circle((cx, cy), r, "FORD_INTERPRETIVE_SHOW")
    for key in ["moat_outer_radius_m", "audience_ring_outer_radius_m"]:
        circle((cx, cy), I["cycle"][key], "FORD_INTERPRETIVE_SHOW")

    rx, ry = I["road_spiral"]["center_xy_m"]
    road_r = float(I["road_spiral"]["mean_radius_m"])
    width = float(I["road_spiral"]["roadway_width_m"])
    for r in (road_r-width/2, road_r, road_r+width/2):
        circle((rx, ry), r, "FORD_INTERPRETIVE_ROAD")

    msp.add_line((cx-radius, cy), (cx+radius, cy),
                 dxfattribs={"layer": "FORD_PERIOD_DOCUMENTED"})
    note(cx-14, cy-5, "%.3f m TURNTABLE DIAMETER / 1938 ARCHITECTURAL RECORD" % diameter, 1.1)
    note(-104, -88, "FORD EXPOSITION 1939, WF0014: SCHEMATIC ONLY - NOT AS BUILT", 1.8)
    note(-104, -93, "SOURCE: FMP-EV-FORD-AR1938-01 / NO HISTORIC SITE REGISTRATION", 1.1)
    note(-100, -33, "INDUSTRIAL HALL: WALLS AND HEIGHTS ESTIMATED")
    note(-92, -69, "ENTRANCE HALL: WALLS AND HEIGHTS ESTIMATED")
    note(0, 62, "GARDEN COURT AND SPIRAL: PLACEMENT ESTIMATED")
    note(14, -58, "THREE REINFORCED CONCRETE RAMP TIERS DOCUMENTED; RADII UNKNOWN")

    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(filename)
    reopened = ezdxf.readfile(filename)
    audit = reopened.audit()
    if audit.has_errors or reopened.header["$INSUNITS"] != 6:
        raise ValueError("DXF audit or metre-unit validation failed")
    actual = [e for e in reopened.modelspace().query("CIRCLE")
              if e.dxf.layer == "FORD_PERIOD_DOCUMENTED"]
    if len(actual) != 1 or abs(actual[0].dxf.radius - radius) > 1e-9:
        raise ValueError("Documented 100-foot turntable circle lost")
    return {"file": str(filename), "entities": len(reopened.modelspace()),
            "turntable_diameter_m": diameter, "historically_certified": False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", type=Path, default=PRESET)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = write_reference_plan(json.loads(args.preset.read_text(encoding="utf-8")),
                                  args.output)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
