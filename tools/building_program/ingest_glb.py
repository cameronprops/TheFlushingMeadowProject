#!/usr/bin/env python3
"""Inspect an existing FMP GLB without editing it; export reviewed staging CSV rows.

One explicit building ID, year, coordinate frame, and source GLB per import.
Source-model bounds are NEVER claimed as survey coordinates or finished shells.
Use --node repeatedly to select parts of a shared GLB; omit to index all meshes.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, os, re
from pathlib import Path
import numpy as np
import trimesh

FIELDS = ('component_id','building_id','period_year','model_asset_id','source_node',
          'mesh_key','role','coordinate_frame','min_x_m','min_y_m','min_z_m',
          'max_x_m','max_y_m','max_z_m','vertices','faces','watertight',
          'material_name','roughness','metallic','source_sha256','verification_status')
ENV_FIELDS = ('envelope_id','building_id','period_year','envelope_scope','coordinate_frame',
              'min_x_m','min_y_m','min_z_m','max_x_m','max_y_m','max_z_m',
              'source_geometry_node','source_asset_id','evidence_status','uncertainty_m',
              'site_registered','notes')
MEDIA_FIELDS=('media_id','title','kind','period_year','uri','repo_path','mime_type',
              'sha256','rights_status','acquisition_status','notes')
LINK_FIELDS=('link_id','building_id','media_id','period_year','role','component_id','notes')

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def read_csv(path,fields):
    if not path.exists():return []
    with path.open(newline='',encoding='utf-8-sig') as f:
        rd=csv.DictReader(f)
        if tuple(rd.fieldnames or ())!=tuple(fields):
            raise ValueError(f'Schema mismatch in {path}')
        return list(rd)

def stage_csv(path, fields, new_rows, key):
    """Existing reviewed records survive; only importer-owned IDs get replaced."""
    original=read_csv(path,fields)
    index={r[key]:r for r in original}
    for row in new_rows:index[row[key]]={col:str(row.get(col,'')) for col in fields}
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_name(path.name+'.tmp')
    with temp.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        writer.writerows(sorted(index.values(),key=lambda r:r[key]))
    os.replace(temp,path)
    return len(original),len(index)

def inspect(path,building,year,up,asset_id,select=None,role='MODEL_PART',
            expected_sha=None,scope='SELECTED_MODEL_COMPONENTS'):
    path=Path(path)
    if path.suffix.lower()!='.glb':raise ValueError('GLB input required')
    if year not in (1939,1940,1964,1965,2026):raise ValueError('Unsupported period year')
    if not re.fullmatch('[A-Za-z0-9_-]+',building):raise ValueError('Invalid building ID')
    if not re.fullmatch('[A-Za-z0-9_-]+',asset_id):raise ValueError('Invalid asset ID')
    sha=digest(path)
    if expected_sha and sha!=expected_sha:raise ValueError('Source hash mismatch; refuse stale model')
    scene=trimesh.load(path,force='scene')
    nodes={n for n in scene.graph.nodes if scene.graph[n][1] is not None}
    requested=set(select or nodes)
    missing=requested-nodes
    if missing:raise ValueError('Requested nodes missing: '+', '.join(sorted(missing)))
    if not requested:raise ValueError('No mesh-bearing nodes selected')
    rows=[];minima=[];maxima=[];materials=set()
    for name in sorted(requested):
        tf,mesh_key=scene.graph[name]
        mesh=scene.geometry[mesh_key]
        points=trimesh.transform_points(mesh.vertices,tf)
        if len(points)==0 or not np.isfinite(points).all():
            raise ValueError('Invalid geometry: '+name)
        lo=points.min(axis=0);hi=points.max(axis=0)
        minima.append(lo);maxima.append(hi)
        material=getattr(mesh.visual,'material',None)
        mat_name=getattr(material,'name',None) or mesh.visual.kind or 'none'
        materials.add(str(mat_name))
        rid='MESH-'+hashlib.sha256((building+'|'+str(year)+'|'+asset_id+'|'+name).encode()).hexdigest()[:22]
        rows.append(dict(component_id=rid,building_id=building,period_year=year,
                         model_asset_id=asset_id,source_node=name,mesh_key=mesh_key,
                         role=role,coordinate_frame='SOURCE_GLB_'+up+'_UP',
                         **dict(zip(('min_x_m','min_y_m','min_z_m','max_x_m','max_y_m','max_z_m'),
                                    [format(float(x),'.6f') for x in [*lo,*hi]])),
                         vertices=len(mesh.vertices),faces=len(mesh.faces),
                         watertight=int(mesh.is_watertight),material_name=mat_name,
                         roughness=getattr(material,'roughnessFactor',None) if getattr(material,'roughnessFactor',None) is not None else '',
                         metallic=getattr(material,'metallicFactor',None) if getattr(material,'metallicFactor',None) is not None else '',
                         source_sha256=sha,verification_status='MODEL_OBSERVED_NOT_HISTORIC_CERTIFIED'))
    low=np.min(minima,axis=0);high=np.max(maxima,axis=0)
    bbox=[format(float(v),'.6f') for v in [*low,*high]]
    envelope=dict(envelope_id=f'AUTO-{building}-{year}-{asset_id}',building_id=building,
                  period_year=year,envelope_scope=scope,coordinate_frame='SOURCE_GLB_'+up+'_UP',
                  **dict(zip(ENV_FIELDS[5:11],bbox)),
                  source_geometry_node='|'.join(sorted(requested)) if len(requested)<=3 else f'{len(requested)} selected mesh nodes',
                  source_asset_id=asset_id,evidence_status='SOURCE_MODEL_MEASURED',
                  uncertainty_m='',site_registered=0,
                  notes='Measured GLB visual mesh bounds only; source model may be provisional; not a period site registration.')
    return dict(schema='fmp.glb-inspection.v1',building_id=building,year=year,
                source_file=str(path),source_sha256=sha,file_bytes=path.stat().st_size,
                coordinate_frame='SOURCE_GLB_'+up+'_UP',selected_components=len(rows),
                selected_vertices=sum(int(r['vertices']) for r in rows),
                selected_faces=sum(int(r['faces']) for r in rows),
                watertight_components=sum(int(r['watertight']) for r in rows),
                materials=sorted(materials),bounds_m=bbox,
                components=rows,envelope=envelope,
                reality_check='GLB numerical source-model measurement only, NOT historical as-built or engine/slicer QA')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--glb',required=True,type=Path)
    p.add_argument('--building',required=True)
    p.add_argument('--year',required=True,type=int)
    p.add_argument('--up',required=True,choices=('X','Y','Z'))
    p.add_argument('--asset-id',required=True)
    p.add_argument('--asset-uri',default='')
    p.add_argument('--expected-sha',default=None)
    p.add_argument('--role',default='MODEL_PART')
    p.add_argument('--scope',default='SELECTED_MODEL_COMPONENTS')
    p.add_argument('--node',action='append')
    p.add_argument('--out',required=True,type=Path,help='Staging output (always written)')
    p.add_argument('--catalog-dir',type=Path,default=None,help='Existing repo catalog directory; use only with --apply')
    p.add_argument('--apply',action='store_true',help='Merge staged rows into canonical version-controlled CSV catalogs')
    a=p.parse_args()
    report=inspect(a.glb,a.building,a.year,a.up,a.asset_id,a.node,a.role,a.expected_sha,a.scope)
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'inspection.json').write_text(json.dumps({k:v for k,v in report.items() if k!='components'},indent=2)+'\n')
    stage_csv(a.out/'master_model_components.csv',FIELDS,report['components'],'component_id')
    stage_csv(a.out/'master_building_envelopes.csv',ENV_FIELDS,[report['envelope']],'envelope_id')
    media=dict(media_id=a.asset_id,title=f'{a.building} GLB inspected {a.year}',kind='3D_GLB',
               period_year=a.year,uri=a.asset_uri,repo_path='',mime_type='model/gltf-binary',
               sha256=report['source_sha256'],rights_status='PROJECT_SOURCE_RIGHTS_REVIEW',
               acquisition_status='LOCAL_MODEL_INSPECTED' if not a.asset_uri else 'EXTERNAL_URL_SUPPLIED',
               notes='Generated file record; preserve source model, verify upload URL and publication rights')
    stage_csv(a.out/'master_media_assets.csv',MEDIA_FIELDS,[media],'media_id')
    link=dict(link_id=f'LINK-{a.building}-{a.year}-{a.asset_id}',building_id=a.building,
              media_id=a.asset_id,period_year=a.year,role='MODEL_SOURCE',component_id='',
              notes=f'GLB inspection recorded {len(report["components"])} node meshes')
    stage_csv(a.out/'master_building_media.csv',LINK_FIELDS,[link],'link_id')
    if digest(a.glb)!=report['source_sha256']:raise RuntimeError('Input GLB changed during scan')
    if a.apply:
        if a.catalog_dir is None:raise ValueError('--apply requires --catalog-dir')
        catalog=a.catalog_dir
        if not (catalog/'master_media_assets.csv').exists():
            raise ValueError('Canonical catalog is missing: '+str(catalog))
        for fieldset,name,key in ((MEDIA_FIELDS,'master_media_assets.csv','media_id'),
                                  (LINK_FIELDS,'master_building_media.csv','link_id'),
                                  (FIELDS,'master_model_components.csv','component_id'),
                                  (ENV_FIELDS,'master_building_envelopes.csv','envelope_id')):
            staged=read_csv(a.out/name,fieldset)
            existing=read_csv(catalog/name,fieldset)
            if name=='master_media_assets.csv':
                byid={r[key]:r for r in existing}
                for row in staged:
                    old=byid.get(row[key])
                    if old and old['sha256'] and old['sha256']!=row['sha256']:
                        raise ValueError('Existing media ID has DIFFERENT SHA; create a new versioned asset ID: '+row[key])
                    if old:staged=[r for r in staged if r[key]!=row[key]]
            if staged:stage_csv(catalog/name,fieldset,staged,key)
        print('Applied reviewed model observations to',catalog)
    print(json.dumps({k:v for k,v in report.items() if k not in ('components','envelope','materials')},indent=2))
    print('Wrote staging tables to',a.out,'; review and merge into canonical catalog/*.csv')

if __name__=='__main__':main()
