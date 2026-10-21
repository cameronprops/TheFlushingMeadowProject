"""Read-only geometric and import-readiness audit for the exact FMP Theme Center v005 GLB.

Requires numpy and trimesh. A passed audit is NOT an Unreal import, continuous
collision test, art approval, or historical dimension certification.

Usage: python -m tools.world_build.audit_theme_center_mesh_v005 ASSEMBLY.glb --manifest manifest.json --out audit.json
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import pathlib
import struct

import numpy as np
import trimesh

EXPECTED_SHA = "de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439"
CRITICAL_RUNTIME = (
    "Trylon_Face_3_Frame__RUNTIME_SHARED_APERTURES_v004",
    "Trylon_Hollow_Exterior__RUNTIME_SHARED_APERTURES_v004",
    "Helicline_Rail_-1__RUNTIME_SHARED_APERTURES_v004",
    "Helicline_Deck_and_Curved_Soffit",
    "PROVISIONAL_Helicline_Surface_Transition_r3",
    "Perisphere_Lower_Removable_Shell__UNREAL_PORTALS_v001",
    "Perisphere_Upper_Removable_Shell",
    "Return_Bridge_Deck",
)


def gltf_document(path: pathlib.Path) -> dict:
    with path.open("rb") as handle:
        header = handle.read(20)
        if len(header) != 20:
            raise ValueError("Truncated GLB header")
        magic, version, declared, json_length, chunk_type = struct.unpack("<IIIII", header)
        if (magic, version, chunk_type) != (0x46546C67, 2, 0x4E4F534A):
            raise ValueError("Not a GLB 2.0 JSON chunk")
        if declared != path.stat().st_size or json_length % 4:
            raise ValueError("Invalid GLB length/alignment")
        return json.loads(handle.read(json_length))


def document_summary(doc: dict) -> dict:
    """Summarize referenced mesh records, distinct from intentionally retained assets."""
    meshes = doc["meshes"]
    used = {node["mesh"] for node in doc["nodes"] if "mesh" in node}
    if not all(isinstance(i, int) and 0 <= i < len(meshes) for i in used):
        raise ValueError("Broken mesh reference")
    live = [p for i in used for p in meshes[i]["primitives"]]
    def count_triangles(primitives):
        if any(p.get("mode", 4) != 4 for p in primitives):
            raise ValueError("Non-triangle primitive encountered")
        return sum(doc["accessors"][p["indices"]]["count"] // 3 for p in primitives)
    dormant = [p for i, mesh in enumerate(meshes) if i not in used for p in mesh["primitives"]]
    active_attributes = Counter(key for p in live for key in p["attributes"])
    return {
        "gltf_nodes": len(doc["nodes"]),
        "gltf_meshes_total": len(meshes),
        "gltf_meshes_referenced": len(used),
        "gltf_meshes_unreferenced_preserved": len(meshes) - len(used),
        "referenced_triangle_count": count_triangles(live),
        "unreferenced_triangle_count_preserved": count_triangles(dormant),
        "active_meshes_without_explicit_material": sum("material" not in p for p in live),
        "active_meshes_without_explicit_normals": sum("NORMAL" not in p["attributes"] for p in live),
        "active_meshes_with_vertex_colors": active_attributes["COLOR_0"],
        "materials": len(doc.get("materials", [])),
        "images": len(doc.get("images", [])),
        "textures": len(doc.get("textures", [])),
        "all_active_primitives_are_triangles": True,
    }


def mesh_summary(scene: trimesh.Scene) -> dict:
    used = {scene.graph.get(node)[1] for node in scene.graph.nodes_geometry}
    open_geoms, inconsistent, degenerate, nonfinite, tiny = [], [], [], [], []
    component_status = {}
    for name in sorted(used):
        mesh = scene.geometry[name]
        if not np.isfinite(mesh.vertices).all():
            nonfinite.append(name)
        if not mesh.is_watertight:
            open_geoms.append(name)
        if not mesh.is_winding_consistent:
            inconsistent.append(name)
        if len(mesh.faces):
            tris = mesh.vertices[mesh.faces]
            cross = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
            norm_squared = np.einsum("ij,ij->i", cross, cross)
            bad = int(np.count_nonzero(norm_squared <= 1e-18))
            near = int(np.count_nonzero((norm_squared > 1e-18) & (norm_squared <= 1e-12)))
            if bad:
                degenerate.append({"name": name, "triangles": bad})
            if near:
                tiny.append({"name": name, "triangles": near})
    for node in CRITICAL_RUNTIME:
        if node in scene.graph.nodes_geometry:
            key = scene.graph.get(node)[1]
            mesh = scene.geometry[key]
            component_status[node] = {
                "mesh_key": key,
                "triangles": len(mesh.faces),
                "watertight": bool(mesh.is_watertight),
                "consistent_winding": bool(mesh.is_winding_consistent),
            }
    missing = sorted(set(CRITICAL_RUNTIME) - set(component_status))
    if missing:
        raise ValueError("Missing priority runtime components: " + ", ".join(missing))
    return {
        "scene_referenced_geometry_count": len(used),
        "scene_bounds_model_local_y_up_m": scene.bounds.tolist(),
        "scene_units": scene.units,
        "geometry_with_nonfinite_vertices": nonfinite,
        "geometry_with_zero_area_triangles": degenerate,
        "geometry_with_very_small_nonzero_triangles": tiny,
        "nonwatertight_visible_mesh_count": len(open_geoms),
        "nonwatertight_visible_meshes": open_geoms,
        "inconsistent_winding_visible_meshes": inconsistent,
        "priority_runtime_components": component_status,
    }


def audit(path: pathlib.Path, manifest: dict) -> dict:
    path = pathlib.Path(path)
    digest_state = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest_state.update(chunk)
    digest = digest_state.hexdigest()
    if digest != EXPECTED_SHA or digest != manifest["sha256"]:
        raise ValueError("Refusing unknown runtime GLB checksum")
    doc = gltf_document(path)
    summary = document_summary(doc)
    if summary["gltf_nodes"] != manifest["assembled_nodes"]:
        raise ValueError("Node count disagrees with trusted v005 manifest")
    if summary["gltf_meshes_referenced"] != manifest["visible_mesh_nodes"]:
        raise ValueError("Active mesh count disagrees with trusted v005 manifest")
    scene = trimesh.load(path, force="scene", process=False)
    geometry = mesh_summary(scene)
    if summary["referenced_triangle_count"] != sum(len(scene.geometry[scene.graph.get(n)[1]].faces) for n in scene.graph.nodes_geometry):
        raise ValueError("glTF active triangle count disagrees with Trimesh scene")
    return {
        "schema": "fmp.theme-center.static-mesh-audit.v001",
        "asset": manifest["asset"],
        "sha256": digest,
        "asset_bytes": path.stat().st_size,
        "glb_document": summary,
        "geometry": geometry,
        "unreal_coordinate_conversion": {
            "model": "right-handed Y-up metres, not georeferenced",
            "preview_mapping": "[X, Z, Y] * 100 centimetres",
            "basis_determinant": -1,
            "risk": "Axis swap flips handedness; engine normals, winding and backface culling require native validation",
        },
        "interpretation": {
            "intentionally_open_perisphere_portals": True,
            "unused_glb_meshes_retained_for_source_provenance": True,
            "open_render_surfaces_do_not_by_themselves_imply_collision_failure": True,
            "missing_normals_or_material_bindings_require_import_review": True,
            "watertight_print_source_is_separate_and_not_audited_here": True,
        },
        "native_unreal_import": "NOT_TESTED",
        "continuous_capsule_collision": "NOT_TESTED",
        "game_dev_cli_asset_pipeline": "NOT_EXECUTED",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("glb", type=pathlib.Path)
    parser.add_argument("--manifest", type=pathlib.Path, required=True)
    parser.add_argument("--out", type=pathlib.Path)
    args = parser.parse_args()
    with args.manifest.open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    result = audit(args.glb, manifest)
    payload = json.dumps(result, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(json.dumps({"sha256": result["sha256"], "document": result["glb_document"],
                      "nonwatertight_count": result["geometry"]["nonwatertight_visible_mesh_count"],
                      "inconsistent_winding": result["geometry"]["inconsistent_winding_visible_meshes"],
                      "geometry_with_zero_area_triangles": result["geometry"]["geometry_with_zero_area_triangles"]}, indent=2))


if __name__ == "__main__":
    main()
