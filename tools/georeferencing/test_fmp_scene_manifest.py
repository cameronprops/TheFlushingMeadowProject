import math
import unittest
from fmp_scene_manifest import make_scene, _invert_affine, _parse_fit_argument


def fitted(**overrides):
    base = {'crs': 'EPSG:32118', 'certified': False,
            'affine_x': [0.35, -0.04, 300000.0],
            'affine_y': [0.02, 0.35, 62000.0],
            'control_rmse_m': 0.2, 'check_rmse_m': 0.7}
    return {**base, **overrides}


def evaluate(x, y, px, py):
    return (x[0]*px+x[1]*py+x[2], y[0]*px+y[1]*py+y[2])


class SceneManifestTests(unittest.TestCase):
    def scene(self, fit=None, **kwargs):
        return make_scene({'1939-XM250': fitted() if fit is None else fit},
                          300050.0, 62025.0, 'SYNTHETIC fixture only', **kwargs)

    def test_canonical_frame_is_explicit(self):
        scene = self.scene()
        self.assertEqual(scene['horizontal']['crs'], 'EPSG:32118')
        self.assertEqual(scene['horizontal']['site_x_positive'], 'east')
        self.assertEqual(scene['engine']['centimetres_per_metre'], 100)
        self.assertEqual(scene['vertical']['status'], 'UNRESOLVED')

    def test_known_pixel_local_metres_and_unreal_centimetres(self):
        m = self.scene()['maps']['1939-XM250']
        local = m['pixel_to_local_site_m']
        unreal = m['pixel_to_unreal_cm']
        x, y = evaluate(local['east_x'], local['north_y'], 200, 120)
        self.assertAlmostEqual(x, 0.35*200-0.04*120-50, places=9)
        self.assertAlmostEqual(y, 0.02*200+0.35*120-25, places=9)
        ux, uy = evaluate(unreal['x'], unreal['y'], 200, 120)
        self.assertAlmostEqual(ux, x*100, places=7)
        self.assertAlmostEqual(uy, y*100, places=7)

    def test_inverse_roundtrip(self):
        m = self.scene()['maps']['1939-XM250']
        x = m['pixel_to_local_site_m']['east_x']
        y = m['pixel_to_local_site_m']['north_y']
        ix = m['local_site_m_to_pixel']['u']
        iy = m['local_site_m_to_pixel']['v']
        for point in [(0, 0), (1024, 768), (5529.17, 3590.4)]:
            local = evaluate(x, y, *point)
            recovered = evaluate(ix, iy, *local)
            for a, b in zip(point, recovered):
                self.assertAlmostEqual(a, b, places=7)

    def test_quality_unassessed_without_threshold(self):
        qa = self.scene()['maps']['1939-XM250']['qa']
        self.assertEqual(qa['status'], 'UNASSESSED')
        self.assertFalse(qa['historically_certified'])

    def test_quality_thresholds_do_not_certify(self):
        self.assertEqual(self.scene(max_check_rmse_m=1)['maps']['1939-XM250']['qa']['status'],
                         'NUMERIC_PASS_NOT_CERTIFIED')
        self.assertEqual(self.scene(max_check_rmse_m=.5)['maps']['1939-XM250']['qa']['status'],
                         'NUMERIC_FAIL')

    def test_mixed_crs_fails(self):
        with self.assertRaisesRegex(ValueError, 'EPSG:32118'):
            self.scene(fitted(crs='EPSG:26918'))

    def test_foot_crs_fails(self):
        with self.assertRaises(ValueError):
            self.scene(fitted(crs='EPSG:2263'))

    def test_singular_transform_fails(self):
        with self.assertRaisesRegex(ValueError, 'Noninvertible'):
            self.scene(fitted(affine_y=[.70, -.08, 62000]))

    def test_invalid_origin_fails(self):
        with self.assertRaises(ValueError):
            make_scene({'a': fitted()}, math.nan, 62000, 'source')
        with self.assertRaises(ValueError):
            make_scene({'a': fitted()}, 300000, 62000, '')

    def test_invalid_rmse_fails(self):
        with self.assertRaises(ValueError):
            self.scene(fitted(check_rmse_m=float('inf')))
        with self.assertRaises(ValueError):
            self.scene(max_check_rmse_m=0)

    def test_auto_certification_claim_rejected(self):
        with self.assertRaisesRegex(ValueError, 'certification'):
            self.scene(fitted(certified=True))

    def test_multiple_maps(self):
        scene = make_scene({'1939': fitted(), '1964': fitted(affine_x=[.4,.01,301000])},
                           300000, 62000, 'SYNTHETIC')
        self.assertEqual(set(scene['maps']), {'1939', '1964'})

    def test_duplicate_map_restriction_not_in_make_scene(self):
        with self.assertRaises(ValueError):
            make_scene({'bad/name': fitted()}, 300000, 62000, 'SYNTHETIC')

    def test_no_maps_rejected(self):
        with self.assertRaises(ValueError):
            make_scene({}, 300000, 62000, 'SYNTHETIC')

    def test_source_arg(self):
        n, path = _parse_fit_argument('1939=tmp/fit.json')
        self.assertEqual(n, '1939')
        self.assertEqual(str(path), 'tmp/fit.json')
        with self.assertRaises(ValueError):
            _parse_fit_argument('missing-equal-sign')

    def test_inverse_matrix_mathematics(self):
        x, y = [.3, .1, 700], [.2, .4, -100]
        ix, iy = _invert_affine(x, y)
        for pt in [(1, 2), (300, -200)]:
            self.assertAlmostEqual(evaluate(ix, iy, *evaluate(x, y, *pt))[0], pt[0], places=8)
            self.assertAlmostEqual(evaluate(ix, iy, *evaluate(x, y, *pt))[1], pt[1], places=8)


if __name__ == '__main__':
    unittest.main()
