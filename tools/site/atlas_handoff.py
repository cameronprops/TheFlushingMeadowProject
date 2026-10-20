#!/usr/bin/env python3
"""FMP Fairground Atlas: validate pixel-traced layouts and export source-gated handoffs.

Usage:
    python tools/site/atlas_handoff.py validate session.json
    python tools/site/atlas_handoff.py csv session.json --out atlas_placements.csv
    python tools/site/atlas_handoff.py catalog --database out/flushing_meadows.sqlite --out atlas_asset_catalog.json
    python tools/site/atlas_handoff.py unreal --database out/flushing_meadows.sqlite --out unreal_spawn_manifest.json
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import sqlite3
from pathlib import Path

ERA={1939,1940,1964,1965,2026}
TYPES={'BUILDING','EXHIBIT','FOUNTAIN','WATER','GARDEN','TREE','FURNISHING','SCULPTURE','STREET','PATH','SERVICE','UTILITY','SITE_FEATURE','OTHER'}
COLUMNS=('placement_id','era_year','entity_type','entity_id','display_name','layer_id',
         'source_map_id','source_uri','geometry_kind','pixel_vertices_json',
         'projected_vertices_json','frame_id','placement_status','historical_evidence',
         'uncertainty_m','variant','rotation_deg','height_offset_m','asset_role','note')

class InvalidAtlas(ValueError): pass

def validate(doc:dict, maps:dict|None=None)->list[dict]:
    if not isinstance(doc,dict) or doc.get('schema')!='fmp.fairground-atlas.session.v1':
        raise InvalidAtlas('Not an FMP Fairground Atlas session v1')
    rows=doc.get('placements')
    if not isinstance(rows,list):raise InvalidAtlas('placements must be an array')
    source_maps={x['id']:x for x in doc.get('reference_maps',[]) if isinstance(x,dict) and x.get('id')}
    if len(source_maps)!=len(doc.get('reference_maps',[])):
        raise InvalidAtlas('Duplicate or malformed map source IDs')
    if maps is not None:
        for name,x in source_maps.items():
            ref=maps.get(name)
            if ref is None or ref['era_year']!=int(x.get('year',-1)) or ref['source_uri']!=(x.get('url') or ''):
                raise InvalidAtlas('Source map ID/URL/era not in canonical database: '+name)
    good=[];seen=set();seen_entity=set()
    for i,x in enumerate(rows):
        if not isinstance(x,dict):raise InvalidAtlas(f'{i}: placement must be object')
        pid=x.get('placement_id');yr=x.get('era_year');t=x.get('entity_type');kind=x.get('geometry_kind')
        if not isinstance(pid,str) or not pid or pid in seen:raise InvalidAtlas('Missing or repeated placement ID')
        seen.add(pid)
        if yr not in ERA or t not in TYPES or not x.get('entity_id'):
            raise InvalidAtlas(f'{pid}: illegal year, type or asset identity')
        if kind not in ('POINT','LINE','POLYGON'):raise InvalidAtlas(f'{pid}: unknown geometry kind')
        if x.get('placement_status')!='RASTER_TRACE':
            raise InvalidAtlas(f'{pid}: browser layouts must be unregistered RASTER_TRACE')
        if x.get('coordinate_frame')!='RASTER_PIXELS':
            raise InvalidAtlas(f'{pid}: browser coordinates must be raster pixels')
        source=source_maps.get(x.get('source_map_id'))
        if source is None or source.get('year')!=yr:
            raise InvalidAtlas(f'{pid}: unknown map or mixed fair year')
        if x.get('source_uri')!=(source.get('url') or '') and not x.get('source_uri'):
            raise InvalidAtlas(f'{pid}: archival source URL required')
        vertices=x.get('vertices')
        least={'POINT':1,'LINE':2,'POLYGON':3}[kind]
        if not isinstance(vertices,list) or len(vertices)<least or (kind=='POINT' and len(vertices)!=1):
            raise InvalidAtlas(f'{pid}: incorrect number of vertices')
        for pt in vertices:
            if (not isinstance(pt,list) or len(pt)!=2 or
                any(not isinstance(n,(float,int)) or isinstance(n,bool)
                    or not math.isfinite(n) for n in pt)):
                raise InvalidAtlas(f'{pid}: nonfinite or nonnumeric pixel coordinate')
            raster=source.get('raster_metadata')
            if raster and (pt[0]<0 or pt[1]<0 or
                           pt[0]>raster['width'] or pt[1]>raster['height']):
                raise InvalidAtlas(f'{pid}: point lies outside the referenced raster')
        key=(yr,t,x['entity_id'],x.get('variant','AS_RESEARCHED'))
        if key in seen_entity:raise InvalidAtlas(f'{pid}: same object already placed in this era')
        seen_entity.add(key)
        good.append(x)
    return good

def to_csv(doc:dict, target:Path, maps:dict|None=None)->int:
    rows=validate(doc,maps)
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=COLUMNS)
        w.writeheader()
        for x in rows:
            w.writerow({'placement_id':x['placement_id'],'era_year':x['era_year'],
               'entity_type':x['entity_type'],'entity_id':x['entity_id'],
               'display_name':x.get('display_name') or x['entity_id'],
               'layer_id':x.get('layer_id') or 'ATLAS_'+x['entity_type'],
               'source_map_id':x['source_map_id'],'source_uri':x.get('source_uri',''),
               'geometry_kind':x['geometry_kind'],
               'pixel_vertices_json':json.dumps(x['vertices'],separators=(',',':')),
               'projected_vertices_json':'','frame_id':'',
               'placement_status':'RASTER_TRACE',
               'historical_evidence':x.get('historical_evidence','NOT_YET_REVIEWED'),
               'uncertainty_m':'','variant':'AS_RESEARCHED','rotation_deg':'',
               'height_offset_m':'','asset_role':x.get('asset_role',''),
               'note':x.get('note','')})
    return len(rows)

def registry(connection:sqlite3.Connection)->dict:
    connection.row_factory=sqlite3.Row
    assets=[]
    for r in connection.execute("""SELECT b.building_id,b.classification,s.display_name,s.year_candidates
      FROM building_dossiers b JOIN reconstruction_subjects s ON s.subject_id=b.building_id"""):
        assets.append(dict(entity_id=r['building_id'],display_name=r['display_name'],
                           entity_type='BUILDING',
                           years=str(r['year_candidates'] or '1939-1940'),source='building_dossiers'))
    for r in connection.execute('SELECT feature_id,canonical_name,feature_kind FROM site_network_features'):
        yr='1939' if '1939' in r['feature_id'] else '1964'
        assets.append(dict(entity_id=r['feature_id'],display_name=r['canonical_name'],
                           entity_type='PATH' if r['feature_kind']=='PEDESTRIAN_PATH' else 'STREET',
                           years=yr,source='site_network_features'))
    for r in connection.execute("""SELECT i.instance_id,i.era_year,t.historical_label,c.category_family
      FROM site_amenity_instances i JOIN site_amenity_types t ON i.type_id=t.type_id
      JOIN site_amenity_categories c ON t.category_id=c.category_id"""):
        kind={'WATER_FEATURE':'FOUNTAIN','CIVIC_ART':'SCULPTURE'}.get(r['category_family'],'FURNISHING')
        assets.append(dict(entity_id=r['instance_id'],display_name=r['historical_label'],
                           entity_type=kind,years=str(r['era_year']),source='site_amenity_instances'))
    for r in connection.execute('SELECT area_id,era_year,historical_name FROM horticulture_areas'):
        assets.append(dict(entity_id=r['area_id'],display_name=r['historical_name'],
                           entity_type='GARDEN',years=str(r['era_year']),source='horticulture_areas'))
    unique={(a['entity_id'],a['entity_type']):a for a in assets}
    return {'schema':'fmp.atlas-asset-registry.v1','assets':list(unique.values()),
            'warning':'Asset presence and year eligibility do not establish site coordinates'}

def unreal(connection:sqlite3.Connection)->dict:
    connection.row_factory=sqlite3.Row
    ready=[]
    for r in connection.execute('SELECT * FROM atlas_unreal_ready ORDER BY era_year,placement_id'):
        row=dict(r)
        geom=json.loads(row['projected_vertices_json'])
        if not isinstance(geom,list) or not geom:raise InvalidAtlas('Missing projected coordinates')
        points=[]
        for pt in geom:
            if len(pt) not in (2,3) or not all(isinstance(v,(int,float)) and
                 math.isfinite(v) for v in pt):
                raise InvalidAtlas('Invalid projected point in approved placement')
            z=pt[2] if len(pt)==3 else row['origin_z_m']
            points.append([round((pt[0]-row['origin_e_m'])*100,4),
                           round((pt[1]-row['origin_n_m'])*100,4),
                           round((z-row['origin_z_m'])*100,4)])
        ready.append({'id':row['placement_id'],'entity_id':row['entity_id'],
          'entity_type':row['entity_type'],'year':row['era_year'],
          'source_map_id':row['source_map_id'],'layer':row['layer_id'],
          'shape':row['geometry_kind'],'unreal_vertices_cm':points,
          'frame_id':row['frame_id'],'crs':row['projected_crs'],
          'evidence':row['historical_evidence'],'uncertainty_m':row['uncertainty_m'],
          'asset_role':row['asset_role'],
          'certification':'REVIEWED_PLACEMENT_ONLY_NOT_HOST_TESTED'})
    return {'schema':'fmp.atlas-unreal-handoff.v1','ready_placements':ready,
      'project_units':'centimetres','up':'Z','site_frames':'per placement',
      'warning':'Importing locations does not certify Unreal assets, collision, or historical geometry'}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('action',choices=('validate','csv','catalog','unreal'))
    ap.add_argument('session',nargs='?')
    ap.add_argument('--database',type=Path)
    ap.add_argument('--out',type=Path)
    args=ap.parse_args()
    db=None
    if args.database:
        db=sqlite3.connect(args.database);db.row_factory=sqlite3.Row
    try:
        if args.action in ('validate','csv'):
            if not args.session:ap.error('session JSON required')
            doc=json.loads(Path(args.session).read_text(encoding='utf-8'))
            allowed=None
            if db:
                allowed={r['map_id']:dict(r) for r in db.execute('SELECT * FROM atlas_reference_maps')}
            if args.action=='validate':
                print(json.dumps({'valid_traces':len(validate(doc,allowed)),'runtime_approved':0},indent=2))
            else:
                if not args.out:ap.error('--out required for csv')
                print('Exported draft traces:',to_csv(doc,args.out,allowed))
        else:
            if not db or not args.out:ap.error('--database and --out required')
            data=registry(db) if args.action=='catalog' else unreal(db)
            args.out.parent.mkdir(parents=True,exist_ok=True)
            args.out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
            print('Wrote',args.out)
    finally:
        if db:db.close()
if __name__=='__main__':main()
