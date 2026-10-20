"""Hermetic regression tests for read-only Theme Center mesh audit semantics."""
import json
import pathlib
import struct
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import trimesh
from tools.world_build import audit_theme_center_mesh_v005 as audit


def sample_doc():
    return {
        "nodes": [{"mesh": 0, "name": "Live"}, {"name": "Disabled"}],
        "meshes": [
            {"primitives": [{"indices": 0, "attributes": {"POSITION": 1}}]},
            {"primitives": [{"indices": 2, "material": 0, "attributes": {"POSITION": 3, "NORMAL": 4}}]},
        ],
        "accessors": [{"count": 6}, {"count": 4}, {"count": 3}, {"count": 3}, {"count": 3}],
        "materials": [{"name": "Unreferenced"}],
    }


class DocumentAuditTests(unittest.TestCase):
    def test_dormant_mesh_is_preserved_but_not_counted_as_visible(self):
        result = audit.document_summary(sample_doc())
        self.assertEqual(result["gltf_meshes_referenced"], 1)
        self.assertEqual(result["gltf_meshes_unreferenced_preserved"], 1)
        self.assertEqual(result["referenced_triangle_count"], 2)
        self.assertEqual(result["unreferenced_triangle_count_preserved"], 1)
        self.assertEqual(result["active_meshes_without_explicit_material"], 1)
        self.assertEqual(result["active_meshes_without_explicit_normals"], 1)

    def test_missing_mesh_reference_is_rejected(self):
        doc = sample_doc()
        doc["nodes"][0]["mesh"] = 7
        with self.assertRaisesRegex(ValueError, "Broken mesh"):
            audit.document_summary(doc)

    def test_nontriangular_primitive_is_not_counted_as_triangles(self):
        doc = sample_doc()
        doc["meshes"][0]["primitives"][0]["mode"] = 1
        with self.assertRaisesRegex(ValueError, "Non-triangle"):
            audit.document_summary(doc)

    def test_invalid_glb_header_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            path = pathlib.Path(folder) / "bad.glb"
            path.write_bytes(b"BADA" + b"\0" * 32)
            with self.assertRaisesRegex(ValueError, "Not a GLB"):
                audit.gltf_document(path)


class GeometryAuditTests(unittest.TestCase):
    def test_triangle_surface_is_open_not_automatically_collision_failure(self):
        m = trimesh.Trimesh(vertices=np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]]),
                            faces=[[0, 1, 2]], process=False)
        scene = trimesh.Scene()
        scene.add_geometry(m, node_name="TEST_SURFACE", geom_name="TEST_MESH")
        with patch.object(audit, "CRITICAL_RUNTIME", ("TEST_SURFACE",)):
            result = audit.mesh_summary(scene)
        self.assertEqual(result["nonwatertight_visible_mesh_count"], 1)
        self.assertEqual(result["geometry_with_zero_area_triangles"], [])
        self.assertFalse(result["priority_runtime_components"]["TEST_SURFACE"]["watertight"])

    def test_missing_critical_component_is_rejected(self):
        scene = trimesh.Scene()
        scene.add_geometry(trimesh.creation.box(), node_name="FOUND")
        with patch.object(audit, "CRITICAL_RUNTIME", ("MISSING",)):
            with self.assertRaisesRegex(ValueError, "Missing priority runtime"):
                audit.mesh_summary(scene)

    def test_wrong_hash_is_rejected_before_loading_mesh(self):
        with tempfile.TemporaryDirectory() as folder:
            path = pathlib.Path(folder) / "unknown.glb"
            path.write_bytes(b"not trusted")
            with self.assertRaisesRegex(ValueError, "unknown runtime GLB checksum"):
                audit.audit(path, {"sha256": audit.EXPECTED_SHA})


if __name__ == "__main__":
    unittest.main()