import unittest
from facade_constraints_v014 import schedule,FT
class TestFacadeConstraints(unittest.TestCase):
    def test_four(self):self.assertEqual(len(schedule()["items"]),4)
    def test_modern_medicine(self):
        a=schedule()["items"][0]
        self.assertFalse(a["fits_existing_proxy"])
        self.assertAlmostEqual(a["existing_proxy_height_deficit_m"],36*FT-9,4)
    def test_picnic_length(self):
        self.assertAlmostEqual(schedule()["items"][3]["documented_artwork_width_m"],110*FT,4)
    def test_unverified(self):
        self.assertTrue(all(not x["facade_height_verified"] for x in schedule()["items"]))
    def test_margin(self):
        self.assertAlmostEqual(schedule(margin=1)["items"][0]["hypothetical_height_with_margin_m"],36*FT+1,4)
    def test_invalid(self):
        with self.assertRaises(ValueError):schedule(margin=-1)
if __name__=="__main__":unittest.main()
