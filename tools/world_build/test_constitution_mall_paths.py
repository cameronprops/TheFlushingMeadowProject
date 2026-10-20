"""Focused diagnostic tests, independent of native Unreal tests."""
import unittest
from tools.world_build.audit_constitution_mall_paths import contact, audit

def surface(name, x0, x1, z0, z1, top_y=0):
    return dict(name=name, x0=x0, x1=x1, z0=z0, z1=z1, top_y=top_y)

class PlanTopologyTests(unittest.TestCase):
    def test_edge_contact_with_shared_width(self):
        self.assertTrue(contact(surface("a", 0, 5, 0, 3),
                                surface("b", 5, 9, 1, 2))["screened_connection"])

    def test_corner_only_does_not_connect(self):
        self.assertFalse(contact(surface("a", 0, 5, 0, 3),
                                 surface("b", 5, 9, 3, 6))["plan_contact"])

    def test_gap_not_connected(self):
        self.assertFalse(contact(surface("a", 0, 5, 0, 3),
                                 surface("b", 5.1, 9, 1, 2))["plan_contact"])

    def test_elevation_blocks_plan_contact(self):
        r = contact(surface("a", 0, 5, 0, 3),
                    surface("b", 5, 9, 1, 2, 0.25))
        self.assertTrue(r["plan_contact"])
        self.assertFalse(r["screened_connection"])

    def test_diagnostic_honest_about_engine(self):
        report = audit()
        self.assertGreater(report["surface_count"], 0)
        self.assertFalse(report["unreal_navigation_tested"])
        self.assertFalse(report["collision_checked"])
        self.assertFalse(report["historically_registered"])
        self.assertEqual(sum(len(c) for c in report["connected_components"]),
                         report["surface_count"])

if __name__ == "__main__":
    unittest.main()
