import unittest
from fmp_georef import fit
from fmp_import_nyc_state_plane import convert, US_SURVEY_FOOT_METRES


def sample():
    points = [(2000, 8000), (4000, 8100), (2300, 10700), (7000, 16000),
              (5000, 9000), (2500, 13000)]
    return [dict(id=str(i), role="control" if i < 4 else "check",
                 pixel_x=str(x), pixel_y=str(y),
                 world_x_m=str(300000 + .13*x - .05*y),
                 world_y_m=str(200000 + .05*x + .13*y), crs="EPSG:32118")
            for i, (x, y) in enumerate(points)]


class GeoreferenceTests(unittest.TestCase):
    def test_affine_and_holdout_large_world_coords(self):
        r = fit(sample())
        self.assertLess(r["check_rmse_m"], 1e-7)
        self.assertFalse(r["certified"])
        self.assertEqual(r["coordinate_units"], "metres")

    def test_collinear_rejected(self):
        rows = sample()
        for i, r in enumerate(rows[:4]):
            r["pixel_x"] = str(i * 100)
            r["pixel_y"] = str(i * 100)
        with self.assertRaises(ValueError):
            fit(rows)

    def test_no_holdout_rejected(self):
        with self.assertRaises(ValueError):
            fit([r for r in sample() if r["role"] == "control"])

    def test_foot_based_crs_rejected(self):
        rows = sample()
        for r in rows:
            r["crs"] = "EPSG:2263"
        with self.assertRaisesRegex(ValueError, "US survey feet"):
            fit(rows)

    def test_degrees_crs_rejected(self):
        rows = sample()
        for r in rows:
            r["crs"] = "EPSG:4326"
        with self.assertRaises(ValueError):
            fit(rows)

    def test_nonfinite_rejected(self):
        rows = sample()
        rows[0]["world_x_m"] = "nan"
        with self.assertRaisesRegex(ValueError, "Non-finite"):
            fit(rows)

    def test_duplicate_id_rejected(self):
        rows = sample()
        rows[1]["id"] = rows[0]["id"]
        with self.assertRaisesRegex(ValueError, "unique"):
            fit(rows)

    def test_bad_holdout_reported_not_certified(self):
        rows = sample()
        rows[-1]["world_x_m"] = str(float(rows[-1]["world_x_m"]) + 15)
        r = fit(rows)
        self.assertGreater(r["check_rmse_m"], 5)
        self.assertFalse(r["certified"])

    def test_us_survey_foot_to_meter_import(self):
        rows = [dict(source_crs="EPSG:2263", world_x_ftus="984250", world_y_ftus="1000")]
        converted = convert(rows)[0]
        self.assertAlmostEqual(float(converted["world_x_m"]), 300000, places=6)
        self.assertAlmostEqual(float(converted["world_y_m"]), 1000*US_SURVEY_FOOT_METRES, places=7)
        self.assertEqual(converted["crs"], "EPSG:32118")

    def test_other_crs_no_implicit_conversion(self):
        with self.assertRaises(ValueError):
            convert([dict(source_crs="EPSG:4326", world_x_ftus="984250", world_y_ftus="1000")])

    def test_refuse_overwrite(self):
        with self.assertRaises(ValueError):
            convert([dict(source_crs="EPSG:2263", world_x_ftus="984250", world_y_ftus="1000", world_x_m="500")])

    def test_missing_and_nonfinite_foot_inputs_rejected(self):
        with self.assertRaises(ValueError):
            convert([dict(source_crs="EPSG:2263", world_x_ftus="inf", world_y_ftus="12")])


if __name__ == "__main__":
    unittest.main()
