import unittest,numpy as np,cv2
from wf0028_assess_frame_pairs_v032 import match_pair
class PairTests(unittest.TestCase):
 def test_empty(self):
  im=np.zeros((300,400,3),np.uint8)
  self.assertEqual(match_pair(im,im)['status'],'INSUFFICIENT_FEATURES')
 def test_flat_translation_is_not_depth(self):
  rng=np.random.default_rng(3);a=np.zeros((400,600,3),np.uint8)
  for _ in range(200):cv2.circle(a,(int(rng.integers(40,560)),int(rng.integers(40,360))),3,(255,255,255),-1)
  b=cv2.warpAffine(a,np.float32([[1,0,20],[0,1,8]]),(600,400))
  self.assertEqual(match_pair(a,b)['status'],'PLANAR_OR_ROTATIONAL_AMBIGUITY')
if __name__=='__main__':unittest.main()
