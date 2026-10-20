"""Fairground Atlas source-gate tests. Run python3 -m unittest -v tests.test_fairground_atlas
Synthetic pixels only; no claimed georeferenced historical locations.
"""
import copy,json,sqlite3,tempfile,unittest
from pathlib import Path
from tools.site.atlas_handoff import InvalidAtlas,validate,to_csv,unreal
from tools.site.atlas_apply_georef import convert as fit_preview
MAP={'id':'ATLAS-1939-GENERAL','year':1939,'url':'https://old-digitalcollections.nypl.org/items/926ff6bc-5ff8-0931-e040-e00a180628c4',
     'status':'UNALIGNED','raster_metadata':{'width':1000,'height':700}}
PLACE={'placement_id':'SYNTHETIC','era_year':1939,'entity_type':'BUILDING','entity_id':'WF0001',
       'display_name':'Trylon','layer_id':'ATLAS_BUILDING','source_map_id':MAP['id'],
       'source_uri':MAP['url'],'geometry_kind':'POLYGON',
       'vertices':[[100,100],[200,100],[200,200]],
       'placement_status':'RASTER_TRACE','coordinate_frame':'RASTER_PIXELS',
       'historical_evidence':'PERIOD_PLAN'}
FIT={'certified':False,'coordinate_units':'metres','crs':'EPSG:32118',
     'control_rmse_m':.2,'check_rmse_m':.3,
     'affine_x':[.5,0,300000],'affine_y':[0,-.5,200000]}

def doc():return {'schema':'fmp.fairground-atlas.session.v1',
                  'reference_maps':[copy.deepcopy(MAP)],'placements':[copy.deepcopy(PLACE)]}

class AtlasTests(unittest.TestCase):
 def test_valid_source_pixel_trace(self):self.assertEqual(len(validate(doc())),1)
 def test_era_mismatch_refused(self):
  x=doc();x['placements'][0]['era_year']=1964
  with self.assertRaises(InvalidAtlas):validate(x)
 def test_duplicate_object_refused(self):
  x=doc();x['placements'].append(dict(x['placements'][0],placement_id='SECOND'))
  with self.assertRaises(InvalidAtlas):validate(x)
 def test_out_of_bounds_refused(self):
  x=doc();x['placements'][0]['vertices'][0]=[9999,9999]
  with self.assertRaises(InvalidAtlas):validate(x)
 def test_false_spatial_certification_refused(self):
  x=doc();x['placements'][0]['placement_status']='REGISTERED_REVIEWED'
  with self.assertRaises(InvalidAtlas):validate(x)
 def test_export_remains_pixel_only(self):
  with tempfile.TemporaryDirectory() as td:
   dest=Path(td)/'draft.csv'
   self.assertEqual(to_csv(doc(),dest),1)
   s=dest.read_text()
   self.assertIn('RASTER_TRACE',s)
   self.assertNotIn('REGISTERED_REVIEWED',s)
 def test_georef_holdout(self):
  rows=[{'placement_id':'p','source_map_id':MAP['id'],
         'pixel_vertices_json':'[[0,0],[100,100]]',
         'placement_status':'RASTER_TRACE','note':''}]
  x=fit_preview(FIT,rows,MAP['id'])
  self.assertEqual(x[0]['placement_status'],'PROJECTED_PREVIEW')
  self.assertEqual(json.loads(x[0]['projected_vertices_json']),
                   [[300000,200000],[300050,199950]])
 def test_bad_holdout_refused(self):
  with self.assertRaises(ValueError):fit_preview(dict(FIT,check_rmse_m=99),[],MAP['id'])
 def test_uncertified_unreal_export_empty(self):
  c=sqlite3.connect(':memory:')
  c.execute('CREATE TABLE atlas_unreal_ready(era_year INTEGER,placement_id TEXT)')
  self.assertEqual(unreal(c)['ready_placements'],[])
if __name__=='__main__':unittest.main()
