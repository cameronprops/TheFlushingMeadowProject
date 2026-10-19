import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from fit_site_registration import fit_registration


class RegistrationTests(unittest.TestCase):
    def points(self):
        return [dict(control_id=str(i),source_x=x,source_y=y,target_x=-2*y+100,
                     target_y=2*x+200,role='fit' if i<4 else 'check')
                for i,(x,y) in enumerate([(0,0),(10,0),(10,10),(0,10),(3,4),(8,6)])]

    def run_fit(self,rows):
        return fit_registration(rows,'SYNTHETIC_TEST','LOCAL_TEST_ONLY','m',0.01)

    def test_known_transform_and_inverse(self):
        r=self.run_fit(self.points())
        self.assertAlmostEqual(r['scale'],2)
        self.assertAlmostEqual(r['rotation_degrees'],90)
        self.assertEqual(r['status'],'WITHIN_LIMIT_WITH_CHECKS')
        self.assertFalse(r['survey_verified'])
        inv=r['inverse_matrix']
        self.assertAlmostEqual(inv[0][0]*(-8)+inv[0][1]*6,3)
        self.assertAlmostEqual(inv[1][0]*(-8)+inv[1][1]*6,4)

    def test_check_point_does_not_change_fit(self):
        points=self.points();points[-1]['target_x']+=5
        r=self.run_fit(points)
        self.assertAlmostEqual(r['scale'],2)
        self.assertEqual(r['status'],'RESIDUAL_LIMIT_EXCEEDED')

    def test_no_independent_checks(self):
        self.assertEqual(self.run_fit(self.points()[:4])['status'],'INSUFFICIENT_INDEPENDENT_CHECKS')

    def test_degenerate_controls(self):
        points=self.points()
        for row in points:row['source_y']=0
        with self.assertRaises(ValueError):self.run_fit(points)

    def test_bad_coordinates_and_ids(self):
        for field,value in [('source_x',float('nan')),('control_id','1'),('role','unknown')]:
            points=self.points();points[0][field]=value
            with self.assertRaises(ValueError):self.run_fit(points)

    def test_reflection_fails_residual_gate(self):
        points=self.points()
        for row in points:row['target_x']=row['source_x'];row['target_y']=-row['source_y']
        with self.assertRaises(ValueError):self.run_fit(points)


if __name__=='__main__':unittest.main()
