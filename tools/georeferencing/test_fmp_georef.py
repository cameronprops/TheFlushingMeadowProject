import unittest
from fmp_georef import fit

class GeoreferenceTests(unittest.TestCase):
 def test_affine_and_holdout(self):
  points=[(0,0),(10,0),(0,10),(10,10),(5,15),(14,7)]
  rows=[dict(id=str(i),role="control" if i<4 else "check",pixel_x=str(x),pixel_y=str(y),
             world_x_m=str(3*x+2*y+100),world_y_m=str(-x+4*y+200),crs="EPSG:26918")
        for i,(x,y) in enumerate(points)]
  r=fit(rows)
  self.assertLess(r["check_rmse_m"],1e-7)
  self.assertFalse(r["certified"])
 def test_collinear_rejected(self):
  rows=[dict(id=str(i),role="control" if i<3 else "check",pixel_x=str(i),pixel_y=str(i),
             world_x_m=str(i),world_y_m=str(i),crs="EPSG:26918") for i in range(5)]
  with self.assertRaises(ValueError):fit(rows)
 def test_no_holdout_rejected(self):
  rows=[dict(id=str(i),role="control",pixel_x=str(i),pixel_y=str(i*i),
             world_x_m=str(i),world_y_m=str(i*i),crs="EPSG:26918") for i in range(4)]
  with self.assertRaises(ValueError):fit(rows)

if __name__=="__main__":unittest.main()
