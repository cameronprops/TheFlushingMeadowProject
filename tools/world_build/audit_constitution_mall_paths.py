"""Constitution Mall pedestrian-topology diagnostic, not an Unreal navigation test.

Works on the existing generator's individual scene components. Coordinates are
interpretive model-local Y-up metres. Connections at rectangle edges count only
when the plan overlap has positive width. Floor elevation differences are reported
but do not establish accessibility, slope, collision, or historical authenticity.
"""
import argparse
import json
from collections import deque

from tools.world_build.build_constitution_mall_v002 import generate

WALK_TYPES = {"PEDESTRIAN_PATH", "PEDESTRIAN_CROSSING", "PLAZA"}
LEVEL_TOLERANCE_M = 0.15
PLAN_TOLERANCE_M = 0.001


def walking_surfaces(items=None):
    if items is None:
        items = generate().items
    result = []
    for item in items:
        if item["kind"] not in WALK_TYPES:
            continue
        v = item["vertices"]
        result.append({
            "name": item["name"], "kind": item["kind"],
            "x0": float(v[:, 0].min()), "x1": float(v[:, 0].max()),
            "z0": float(v[:, 2].min()), "z1": float(v[:, 2].max()),
            "top_y": float(v[:, 1].max()),
        })
    return sorted(result, key=lambda d: d["name"])


def contact(a, b, plan_tolerance=PLAN_TOLERANCE_M,
            level_tolerance=LEVEL_TOLERANCE_M):
    x_overlap = min(a["x1"], b["x1"]) - max(a["x0"], b["x0"])
    z_overlap = min(a["z1"], b["z1"]) - max(a["z0"], b["z0"])
    # One planar axis may touch at its endpoint, but the other needs width.
    touching = ((x_overlap >= -plan_tolerance and z_overlap > plan_tolerance)
                or (z_overlap >= -plan_tolerance and x_overlap > plan_tolerance))
    vertical_delta = abs(a["top_y"] - b["top_y"])
    return {
        "plan_contact": bool(touching),
        "height_difference_m": round(vertical_delta, 6),
        "within_screening_level": bool(vertical_delta <= level_tolerance),
        "screened_connection": bool(touching and vertical_delta <= level_tolerance),
    }


def audit(items=None):
    surfaces = walking_surfaces(items)
    graph = {a["name"]: set() for a in surfaces}
    contacts = []
    level_mismatches = []
    for i, a in enumerate(surfaces):
        for b in surfaces[i+1:]:
            c = contact(a, b)
            if c["plan_contact"]:
                record = {"a": a["name"], "b": b["name"], **c}
                contacts.append(record)
                if c["screened_connection"]:
                    graph[a["name"]].add(b["name"])
                    graph[b["name"]].add(a["name"])
                else:
                    level_mismatches.append(record)
    components = []
    unseen = set(graph)
    while unseen:
        root = sorted(unseen)[0]
        queue = deque([root])
        unseen.remove(root)
        found = []
        while queue:
            node = queue.popleft()
            found.append(node)
            for neighbor in sorted(graph[node] & unseen):
                unseen.remove(neighbor)
                queue.append(neighbor)
        components.append(sorted(found))
    return {
        "audit": "model_local_horizontal_surfaces_only",
        "historically_registered": False,
        "unreal_navigation_tested": False,
        "collision_checked": False,
        "plan_tolerance_m": PLAN_TOLERANCE_M,
        "level_screen_tolerance_m": LEVEL_TOLERANCE_M,
        "surfaces": surfaces,
        "surface_count": len(surfaces),
        "contacts": contacts,
        "level_mismatches": level_mismatches,
        "connected_components": components,
        "component_count": len(components),
        "unconnected_surfaces": sorted(name for name, links in graph.items() if not links),
        "limitations": [
            "Axis-aligned top-face boxes only; not a walkable polygon/navmesh test.",
            "Does not detect walls, plan obstructions, parapets, water or clearance.",
            "Does not include the preserved Theme Center or terrain under the mall.",
            "Elevation screen is arbitrary and cannot establish a safe accessible path.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Write full diagnostic JSON")
    args = parser.parse_args()
    report = audit()
    if args.output:
        from pathlib import Path
        p = Path(args.output)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "surface_count": report["surface_count"],
        "component_count": report["component_count"],
        "unconnected_surfaces": report["unconnected_surfaces"],
        "level_mismatches": len(report["level_mismatches"]),
        "unreal_navigation_tested": False,
    }, indent=2))


if __name__ == "__main__":
    main()
