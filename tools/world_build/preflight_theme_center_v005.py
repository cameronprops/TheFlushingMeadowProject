"""Read-only FMP Theme Center v005 handoff preflight, NOT Unreal certification.

Check cross-linked source/provisional manifests, independently calculate numerical
constraints, and (optionally) hash and inspect the exact assembled GLB bytes.
This script modifies no source or runtime model. Stdlib-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import struct
from typing import Any

GATE_PATH = "research/pavilions/theme_center/ENGINE_HANDOFF_GATE_v001.json"
FT_TO_M = 0.3048


class PreflightError(ValueError):
    """A source, geometry, or identity contract was not met."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PreflightError(message)


def close(a: float, b: float, tolerance: float = 1e-8) -> bool:
    return math.isclose(float(a), float(b), rel_tol=0, abs_tol=tolerance)


def check_manifest_set(d: dict[str, Any]) -> dict[str, Any]:
    """Validate existing manifests without promoting interpretive values to history."""
    gate, built, portals, route, transition, runtime = (
        d[k] for k in ("gate", "built", "portals", "route", "transition", "runtime")
    )
    require(gate["schema"] == "fmp.theme-center.engine-handoff-gate.v001", "Unknown handoff schema")
    require(gate["asset_id"] == built["assembly_id"], "Asset identity mismatch")
    require(gate["era"] == built["period_year"] == 1939, "Era mismatch")
    require(runtime["asset"] == gate["runtime_asset"], "Runtime asset identity mismatch")
    sha = runtime["source_sha256"]
    for name, value in (("built", built["base_model"]["sha256"]),
                        ("portals", portals["source_sha256"]),
                        ("route", route["source_sha256"]),
                        ("transition", transition["source_sha256"])):
        require(sha == value, f"{name}: source hash disagrees with v005")
    require(runtime["overlay_sha256"] == portals["overlay_sha256"] == route["overlay_sha256"],
            "Overlay hash disagrees among v004, route and assembled v005")
    require(runtime["source_nodes"] == built["base_model"]["expected_nodes"] == 510,
            "Unexpected source node count")
    require(runtime["overlay_nodes"] == 62 and runtime["assembled_nodes"] == 573,
            "Unexpected assembled scene node count")
    require(runtime["assembled_nodes"] == runtime["source_nodes"] + runtime["overlay_nodes"] + 1,
            "Unexpected overlay root count")
    require(runtime["visible_mesh_nodes"] == 558, "Unexpected visible mesh count")
    require(runtime["units"] == "metres" and "Y-up" in runtime["coordinate_frame"],
            "Missing model-local Y-up metre convention")
    require(runtime["source_binary_preserved"] is True and
            runtime["source_materials_and_ids_preserved"] is True,
            "Assembler provenance contract missing")
    require(portals["historical_acceptance"] == "UNVERIFIED" and
            portals["unreal_acceptance"] == "NOT_TESTED", "Portal acceptance incorrectly promoted")
    require(gate["coordinate_contract"]["world_registration_status"] == "UNREGISTERED",
            "The asset must not silently become geographically registered")
    require(route["status"] == "NO_SAMPLED_SURFACE_CONTACTS" and
            route["pose_count"] == 435 and not route["findings"],
            "The cited 435-pose v004 screening does not match this release")
    require(route["acceptance"] == "OPEN_NATIVE_COLLISION_AND_CONTINUOUS_SWEEP",
            "Offline route screening was mistakenly promoted to navigation acceptance")
    require(set(route["hidden_source_nodes"]) == set(portals["hide_source_nodes"]),
            "Route audit and portal overlay disagree on source display exclusions")
    require(set(x["name"] for x in runtime["disabled_source_meshes"]) ==
            set(portals["hide_source_nodes"]), "v005 did not disable exactly v004 superseded meshes")
    require(transition["source_sha256"] == sha and
            transition["status"] == "PROVISIONAL_RUNTIME_ONLY", "Transition lineage/status mismatch")

    constraints = {x["id"]: x for x in built["constraints"]}
    needed = ("F001", "F009", "F010", "F021", "F028", "F058", "F059")
    require(all(x in constraints for x in needed), "Missing historically documented constraints")
    value = lambda key: float(constraints[key]["si_value"])
    trylon = value("F001")
    residual = value("F009") + value("F010") - trylon
    require(close(residual, 0), "Trylon documented section lengths do not close")
    require(close(trylon / FT_TO_M, 610), "Trylon is not the documented 610-ft built version")
    sphere = value("F021")
    require(close(sphere / FT_TO_M, 180), "Perisphere uses a non-built diameter")
    require(close(value("F058") / FT_TO_M, 950), "Helicline length conversion mismatch")
    require(close(value("F059") / FT_TO_M, 18), "Helicline width conversion mismatch")
    require(constraints["F028"]["si_value"] == 32, "Unexpected meridian count")
    require(all(constraints[k]["evidence_status"] == "BUILT_PERIOD_DOCUMENTED" for k in needed),
            "Historically documented reference constraints were downgraded")

    body = route["body_assumption"]
    radius, height, lift = (float(body[k]) for k in ("radius_m", "height_m", "floor_lift_m"))
    require(radius > 0 and height > 2 * radius and lift >= 0, "Invalid provisional body")
    require(len(portals["apertures"]) == 2, "Expected both Trylon return apertures")
    openings = []
    for opening in portals["apertures"]:
        require(opening["status"] == "PREVIEW_ONLY_TOPOLOGY_TEST_NOT_HISTORICAL_DIMENSIONS",
                "Portal incorrectly represented as historically measured")
        depth, vertical, width = [float(v) for v in opening["size_xyz_m"]]
        require(all(math.isfinite(v) and v > 0 for v in (depth, vertical, width)),
                "Invalid portal size")
        available = width - 2 * radius
        upper_margin = vertical - height - lift
        require(available > 0 and upper_margin > 0, "Provisional body larger than nominal opening")
        x, y, z = (float(v) for v in opening["center_xyz_m"])
        require(all(math.isfinite(v) for v in (x, y, z)), "Invalid portal location")
        openings.append({
            "id": opening["id"], "model_center_xyz_m": [x, y, z],
            "preview_unreal_xyz_cm": [100 * x, 100 * z, 100 * y],
            "cut_depth_x_m": depth, "opening_height_y_m": vertical,
            "opening_width_z_m": width,
            "nominal_allowable_capsule_center_width_m": available,
            "nominal_vertical_margin_with_floor_lift_m": upper_margin,
            "interpretive_not_historically_measured": True
        })
    require(close(transition["max_surface_slope_ratio"] * 100, 6.931235987913756, 1e-8),
            "Inherited measured preview ramp-slope snapshot changed")
    return {
        "historical_numeric_checks": {
            "trylon_built_height_m": trylon,
            "trylon_section_closure_residual_m": residual,
            "perisphere_built_diameter_m": sphere,
            "perisphere_radius_m": sphere / 2,
            "meridian_pitch_degrees_if_equally_spaced": 360 / value("F028"),
            "equatorial_arc_spacing_m_if_equally_spaced": math.pi * sphere / value("F028"),
            "helicline_documented_centerline_m": value("F058"),
            "helicline_documented_width_m": value("F059")
        },
        "body_is_test_assumption_not_unreal_character": body,
        "portal_previews": openings,
        "v004_discrete_return_screen": {
            "pose_count": route["pose_count"], "reported_surface_contacts": len(route["findings"]),
            "continuous_collision_tested": False, "unreal_navmesh_tested": False
        },
        "inherited_preview_transition_slope_percent": 100 * transition["max_surface_slope_ratio"]
    }


def validate_glb(path: pathlib.Path, runtime: dict[str, Any]) -> dict[str, Any]:
    """Check actual bytes/hash/glTF structure; no triangulation or GPU evidence."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    require(digest.hexdigest() == runtime["sha256"], "Runtime GLB SHA-256 mismatch")
    b = path.read_bytes()
    require(len(b) >= 28, "Truncated GLB")
    magic, version, total = struct.unpack_from("<III", b, 0)
    require((magic, version, total) == (0x46546C67, 2, len(b)), "Invalid GLB header/length")
    jsize, jkind = struct.unpack_from("<II", b, 12)
    require(jkind == 0x4E4F534A and jsize % 4 == 0, "Missing/unaligned GLB JSON chunk")
    require(20 + jsize + 8 <= len(b), "Truncated JSON/BIN chunks")
    d = json.loads(b[20:20 + jsize])
    bsize, bkind = struct.unpack_from("<II", b, 20 + jsize)
    require(bkind == 0x004E4942 and 28 + jsize + bsize == len(b), "Invalid BIN chunk")
    require(d.get("asset", {}).get("version") == "2.0", "Not a glTF 2.0 scene")
    require(len(d.get("buffers", [])) == 1 and d["buffers"][0]["byteLength"] == bsize,
            "GLB binary length disagrees with buffer metadata")
    nodes = d["nodes"]
    require(len(nodes) == runtime["assembled_nodes"], "Actual GLB node count mismatch")
    require(sum("mesh" in n for n in nodes) == runtime["visible_mesh_nodes"],
            "Actual GLB visible mesh count mismatch")
    meshes = d.get("meshes", [])
    require(all(0 <= n["mesh"] < len(meshes) for n in nodes if "mesh" in n),
            "Node references a missing mesh")
    require(all(0 <= ch < len(nodes) for n in nodes for ch in n.get("children", [])),
            "Node references a missing child")
    for row in runtime["disabled_source_meshes"]:
        n = nodes[row["node"]]
        require(n.get("name") == row["name"] and "mesh" not in n,
                f"Superseded node still visible: {row['name']}")
    ids = [n.get("extras", {}).get("fmp", {}).get("object_id") for n in nodes]
    require(all(ids[i] for i in range(len(nodes) - 1)), "Missing source/overlay object identity")
    require(len(set(ids[:-1])) == len(nodes) - 1, "Duplicate object identity")
    require(nodes[-1].get("name") == "FMP_Provisional_Runtime_v004" and "mesh" not in nodes[-1],
            "Unexpected grouping root or active last mesh")
    return {"status": "EXACT_HASH_AND_STATIC_GLTF_STRUCTURE_VERIFIED",
            "sha256": digest.hexdigest(), "byte_length": len(b),
            "nodes": len(nodes), "visible_mesh_nodes": sum("mesh" in n for n in nodes),
            "engine_imported": False, "continuous_collision_tested": False}


def run(root: pathlib.Path, gate_path: pathlib.Path, glb: pathlib.Path | None = None) -> dict[str, Any]:
    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    docs = {"gate": gate}
    for key, p in gate["source_paths"].items():
        docs[{"built_constraints": "built", "portals": "portals",
              "return_route": "route", "transition": "transition",
              "runtime_manifest": "runtime"}[key]] = json.loads((root / p).read_text(encoding="utf-8"))
    numerical = check_manifest_set(docs)
    actual = validate_glb(glb, docs["runtime"]) if glb is not None else {
        "status": "NOT_EXECUTED_NO_LOCAL_GLB", "engine_imported": False,
        "continuous_collision_tested": False
    }
    return {
        "schema": "fmp.theme-center.engine-handoff-preflight-report.v001",
        "asset_id": gate["asset_id"], "runtime_asset": docs["runtime"]["asset"],
        "expected_runtime_sha256": docs["runtime"]["sha256"],
        "manifest_and_numerical_crosscheck": "PASSED",
        "glb_static_check": actual,
        "numerical_findings": numerical,
        "acceptance": {
            "historical_openings_verified": False,
            "site_registered": False,
            "unreal_import_validated": False,
            "unreal_collision_and_navigation_validated": False,
            "game_dev_package_verified": False
        },
        "note": "Provisional test only. None of these checks certify historical openings, engineered framing, body containment, continuous motion, engine import, or performance."
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[2])
    ap.add_argument("--gate", type=pathlib.Path, default=None)
    ap.add_argument("--glb", type=pathlib.Path, default=None,
                    help="Exact v005 assembled GLB; omitted means metadata-only preflight")
    ap.add_argument("--out", type=pathlib.Path, default=None,
                    help="Optional report path; no source or GLB is ever modified")
    args = ap.parse_args()
    try:
        r = run(args.root, args.gate or args.root / GATE_PATH, args.glb)
    except (PreflightError, KeyError, OSError, json.JSONDecodeError, struct.error) as exc:
        ap.exit(1, f"PREFLIGHT FAILED: {exc}\n")
    data = json.dumps(r, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(data, encoding="utf-8")
    print(data, end="")


if __name__ == "__main__":
    main()