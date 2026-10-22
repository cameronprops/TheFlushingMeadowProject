"""Photo solver tests are synthetic. No historical photograph has been fitted yet."""
from pathlib import Path
import copy,importlib.util,unittest
import cv2
import numpy as np
spec=importlib.util.spec_from_file_location('solver',Path(__file__).with_name('solve_theme_center_photo_pose_v001.py'))
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class TestPhotoPose(unittest.TestCase):
 def setUp(self):
  k=np.array([[1100.,0,800],[0,1100,600],[0,0,1]])
  pts=np.array([[-10.,0.,-5],[-10.,5.,5],[5.,0.,10],[10.,12.,10],[0.,7.,-10],[-2.,15.,2],[12.,6.,-4],[0.,-3.,8],[3.,9.,2]])
  rv=np.array([.04,-.03,.02]);tv=np.array([4.,-2.,80.]);pixels=cv2.projectPoints(pts,rv,tv,k,None)[0].reshape(-1,2)
  self.d={'model_sha256':mod.SOURCE_SHA,'camera_intrinsics_status':'MEASURED_OR_CALIBRATED',
          'photo':{'source_url':'https://example.org/actual-archival-photo.jpg','credit':'Synthetic test only','local_image_sha256':'a'*64},
          'camera_matrix_px':k.tolist(),'image_dimensions_px':[1600,1200],
          'correspondences':[{'feature_id':str(i),'world_xyz_m':w.tolist(),'image_uv_px':p.tolist()} for i,(w,p) in enumerate(zip(pts,pixels))]}
 def test_exact_synthetic_camera_pose(self):
  r=mod.solve(self.d)
  self.assertEqual(r['inliers'],9)
  self.assertLess(r['reprojection_rmse_px'],.00001)
  self.assertEqual(r['measured_historic_architecture'],False)
 def test_refuse_missing_intrinsics(self):
  self.d['camera_intrinsics_status']='UNKNOWN'
  with self.assertRaisesRegex(mod.PhotoCalibrationError,'camera intrinsics required'):mod.solve(self.d)
 def test_refuse_less_than_six_points(self):
  self.d['correspondences']=self.d['correspondences'][:5]
  with self.assertRaisesRegex(mod.PhotoCalibrationError,'At least 6'):mod.solve(self.d)
 def test_refuse_planar_degeneracy(self):
  for row in self.d['correspondences']:row['world_xyz_m'][1]=0
  with self.assertRaisesRegex(mod.PhotoCalibrationError,'non-coplanar'):mod.solve(self.d)
 def test_refuse_invalid_model(self):
  self.d['model_sha256']='bad'
  with self.assertRaisesRegex(mod.PhotoCalibrationError,'Model GLB identity'):mod.solve(self.d)
 def test_refuse_no_photographic_provenance(self):
  self.d['photo']['source_url']=''
  with self.assertRaisesRegex(mod.PhotoCalibrationError,'provenance'):mod.solve(self.d)
 def test_refuse_points_off_photo(self):
  self.d['correspondences'][0]['image_uv_px']=[1800,0]
  with self.assertRaisesRegex(mod.PhotoCalibrationError,'image bounds'):mod.solve(self.d)
if __name__=='__main__':unittest.main()
