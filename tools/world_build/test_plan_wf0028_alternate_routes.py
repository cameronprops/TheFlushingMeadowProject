import unittest
from plan_wf0028_alternate_routes import plan_route

class TestPlanner(unittest.TestCase):
    def test_open_path(self):
        r=plan_route([0,0,10,10],[],[1,1],[9,9])
        self.assertEqual(r["status"],"CANDIDATE_ONLY")
        self.assertGreater(r["length_m"],0)
    def test_endpoint_blocked(self):
        r=plan_route([0,0,10,10],[{"id":"wall","bounds":[0,0,2,2]}],[1,1],[8,8])
        self.assertEqual(r["status"],"ENDPOINT_BLOCKED")
    def test_impassable_barrier(self):
        r=plan_route([0,0,10,10],[{"id":"wall","bounds":[4,0,6,10]}],[1,5],[9,5])
        self.assertEqual(r["status"],"NO_ROUTE_AT_RESOLUTION")
    def test_detour(self):
        r=plan_route([0,0,10,10],[{"id":"wall","bounds":[4,2,6,8]}],[1,5],[9,5])
        self.assertEqual(r["status"],"CANDIDATE_ONLY")
        self.assertGreater(r["length_m"],8)

if __name__=="__main__":
    unittest.main()
