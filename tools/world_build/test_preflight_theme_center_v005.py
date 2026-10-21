"""Hermetic, stdlib-only regression tests for the Theme Center engine preflight.

These tests use synthetic fixture data, NOT the Drive production GLB or Unreal.
"""
import copy
import hashlib
import json
import pathlib
import struct
import tempfile
import unittest

from tools.world_build.preflight_theme_center_v005 import (
    PreflightError, check_manifest_set, validate_glb,
)

SHA0 = "a" * 64
SHA1 = "b" * 64


def fixture():
    cs = [
        ("F001", 185.928), ("F009", 146.304), ("F010", 39.624),
        ("F021", 54.864), ("F028", 32), ("F058", 289.56), ("F059", 5.4864),
    ]
    hidden = ["Perisphere_Lower_Removable_Shell", "Helicline_Bridge_Transition_Hypothesis",
              "Trylon_Face_3_Frame", "Trylon_Hollow_Exterior", "Helicline_Rail_-1"]
    return {
        "gate": {"schema": "fmp.theme-center.engine-handoff-gate.v001",
                 "asset_id": "FMP_THEME_CENTER_1939", "era": 1939,
                 "runtime_asset": "FMP_ThemeCenter_Assembled_Runtime_v005.glb",
                 "coordinate_contract": {"world_registration_status": "UNREGISTERED"}},
        "built": {"assembly_id": "FMP_THEME_CENTER_1939", "period_year": 1939,
                  "base_model": {"sha256": SHA0, "expected_nodes": 510},
                  "constraints": [{"id": k, "si_value": v,
                                   "evidence_status": "BUILT_PERIOD_DOCUMENTED"} for k, v in cs]},
        "portals": {"source_sha256": SHA0, "overlay_sha256": SHA1,
                    "historical_acceptance": "UNVERIFIED", "unreal_acceptance": "NOT_TESTED",
                    "hide_source_nodes": hidden,
                    "apertures": [{"id": f"TRYLON_RETURN_{suffix}",
                                   "center_xyz_m": [-36.7, 17.0496, z],
                                   "size_xyz_m": [3.4, 2.4, 2.4],
                                   "status": "PREVIEW_ONLY_TOPOLOGY_TEST_NOT_HISTORICAL_DIMENSIONS"}
                                  for suffix, z in (("ENTRY", 3.048), ("EXIT", -3.15))]},
        "route": {"source_sha256": SHA0, "overlay_sha256": SHA1,
                  "body_assumption": {"radius_m": 0.3, "height_m": 1.8,
                                      "floor_lift_m": 0.05},
                  "pose_count": 435, "findings": [], "hidden_source_nodes": sorted(hidden),
                  "status": "NO_SAMPLED_SURFACE_CONTACTS",
                  "acceptance": "OPEN_NATIVE_COLLISION_AND_CONTINUOUS_SWEEP"},
        "transition": {"source_sha256": SHA0, "status": "PROVISIONAL_RUNTIME_ONLY",
                       "max_surface_slope_ratio": 0.06931235987913756},
        "runtime": {"asset": "FMP_ThemeCenter_Assembled_Runtime_v005.glb",
                    "source_sha256": SHA0, "overlay_sha256": SHA1,
                    "source_nodes": 510, "overlay_nodes": 62, "assembled_nodes": 573,
                    "visible_mesh_nodes": 558, "units": "metres",
                    "coordinate_frame": "right-handed Y-up local, unregistered",
                    "source_binary_preserved": True,
                    "source_materials_and_ids_preserved": True,
                    "disabled_source_meshes": [{"name": name} for name in hidden]},
    }


def synthetic_glb():
    nodes = [
        {"name": "Hidden", "extras": {"fmp": {"object_id": "id-1"}}},
        {"name": "Original", "mesh": 0, "extras": {"fmp": {"object_id": "id-2"}}},
        {"name": "Overlay", "mesh": 1, "extras": {"fmp": {"object_id": "id-3"}}},
        {"name": "FMP_Provisional_Runtime_v004", "children": [2]},
    ]
    doc = {"asset": {"version": "2.0"}, "nodes": nodes,
           "meshes": [{"primitives": []}, {"primitives": []}],
           "buffers": [{"byteLength": 4}], "scenes": [{"nodes": [0, 1, 3]}]}
    raw = json.dumps(doc, separators=(",", ":")).encode("utf-8")
    raw += b" " * (-len(raw) % 4)
    buf = b"\0\0\0\0"
    return (struct.pack("<III", 0x46546C67, 2, 28 + len(raw) + len(buf))
            + struct.pack("<II", len(raw), 0x4E4F534A) + raw
            + struct.pack("<II", len(buf), 0x004E4942) + buf)


class MetadataPreflightTests(unittest.TestCase):
    def test_supported_manifest_contract_and_nominal_width(self):
        d = check_manifest_set(fixture())
        self.assertEqual(d["historical_numeric_checks"]["trylon_section_closure_residual_m"], 0)
        self.assertAlmostEqual(d["portal_previews"][0]["nominal_allowable_capsule_center_width_m"], 1.8)
        self.assertAlmostEqual(d["portal_previews"][0]["nominal_vertical_margin_with_floor_lift_m"], 0.55)
        self.assertEqual(d["v004_discrete_return_screen"]["continuous_collision_tested"], False)
        self.assertAlmostEqual(d["portal_previews"][0]["preview_unreal_xyz_cm"][0], -3670)

    def test_wrong_overlay_release_is_rejected(self):
        f = fixture(); f["route"]["overlay_sha256"] = "c" * 64
        with self.assertRaisesRegex(PreflightError, "Overlay hash"):
            check_manifest_set(f)

    def test_proposal_era_dimensions_are_rejected(self):
        f = fixture(); f["built"]["constraints"][0]["si_value"] = 213.36
        with self.assertRaises(PreflightError):
            check_manifest_set(f)

    def test_interpretive_door_must_stay_unverified(self):
        f = fixture(); f["portals"]["apertures"][0]["status"] = "HISTORICALLY_VERIFIED"
        with self.assertRaises(PreflightError):
            check_manifest_set(f)

    def test_route_clearance_must_not_be_promoted_to_navigation(self):
        f = fixture(); f["route"]["acceptance"] = "UNREAL_NAVMESH_PASSED"
        with self.assertRaises(PreflightError):
            check_manifest_set(f)

    def test_blocked_capsule_is_rejected_at_nominal_portal(self):
        f = fixture(); f["route"]["body_assumption"]["radius_m"] = 1.3
        with self.assertRaises(PreflightError):
            check_manifest_set(f)


class GlbStaticTests(unittest.TestCase):
    def test_synthetic_glb_hash_and_structure(self):
        b = synthetic_glb()
        m = {"sha256": hashlib.sha256(b).hexdigest(), "assembled_nodes": 4,
             "visible_mesh_nodes": 2,
             "disabled_source_meshes": [{"name": "Hidden", "node": 0}]}
        with tempfile.TemporaryDirectory() as t:
            path = pathlib.Path(t) / "synthetic.glb"
            path.write_bytes(b)
            outcome = validate_glb(path, m)
            self.assertEqual(outcome["status"], "EXACT_HASH_AND_STATIC_GLTF_STRUCTURE_VERIFIED")
            self.assertFalse(outcome["engine_imported"])
            path.write_bytes(b + b"x")
            with self.assertRaisesRegex(PreflightError, "SHA-256"):
                validate_glb(path, m)


if __name__ == "__main__":
    unittest.main()
