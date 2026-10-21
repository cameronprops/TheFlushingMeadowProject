import json,unittest,hashlib
from pathlib import Path
from check_landing import inspect,START,FINISH
from glb_tools import read_glb
R=Path(__file__).parent
class LandingTests(unittest.TestCase):
 def test_source_defect_reproduced(self):
  self.assertEqual(inspect(R.parent/'portal_build/output/ThemeCenter_Framed_Portals_v007.glb')['supported'],9)
 def test_full_approach_supported(self):
  self.assertEqual(inspect(R/'ThemeCenter_UpperLanding_v008.glb')['supported'],15)
 def test_first_tread_not_covered_by_landing(self):
  report=inspect(R/'ThemeCenter_UpperLanding_v008.glb',.10,(START[1]-FINISH[1])/23)
  (R/'first_tread.json').write_text(json.dumps(report,indent=2)+'\n')
  self.assertEqual(report['supported'],15)
 def test_exact_preservation_except_one_mesh_binding(self):
  a,ab=read_glb(R.parent/'portal_build/output/ThemeCenter_Framed_Portals_v007.glb');b,bb=read_glb(R/'ThemeCenter_UpperLanding_v008.glb')
  self.assertEqual(bytes(ab),bytes(bb[:len(ab)]));self.assertEqual(a['meshes'],b['meshes'][:len(a['meshes'])])
  self.assertEqual(a['materials'],b['materials']);self.assertEqual(len(a['nodes']),len(b['nodes']))
  for x,y in zip(a['nodes'],b['nodes']):
   if x.get('name')!='PROVISIONAL_UpperLandingToStair':self.assertEqual(x,y)
if __name__=='__main__':unittest.main()
