#!/usr/bin/env python3
"""Incremental FMP GLB catalogue refresh with preserved previous versions.

Read explicitly registered *.fmp-model.json manifests only. Do not rewrite
GLBs or invent geometry, historical registration, printability, or walkthrough
certification. Any changed mesh or node selection creates a new model asset;
the active release points at the new revision. Old source records remain.
"""
from __future__ import annotations
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import time

try:
    from .ingest_glb import inspect, digest, read_csv, FIELDS, ENV_FIELDS, MEDIA_FIELDS, LINK_FIELDS
except ImportError:  # Direct CLI launch from this folder
    from ingest_glb import inspect, digest, read_csv, FIELDS, ENV_FIELDS, MEDIA_FIELDS, LINK_FIELDS

ROOT = Path(__file__).resolve().parents[2]
RELEASE_FIELDS = (
    'release_key','building_id','period_year','logical_role','active_media_id',
    'source_path','source_sha256','up_axis','selected_nodes','observed_utc','status'
)
TABLE_FILES = (
    ('master_media_assets.csv', MEDIA_FIELDS, 'media_id'),
    ('master_building_media.csv', LINK_FIELDS, 'link_id'),
    ('master_model_components.csv', FIELDS, 'component_id'),
    ('master_building_envelopes.csv', ENV_FIELDS, 'envelope_id'),
    ('master_active_model_releases.csv', RELEASE_FIELDS, 'release_key'),
)
YEAR_SET={1939,1940,1964,1965,2026}
SAFE_ID=re.compile(r'^[A-Za-z0-9_-]{1,100}$')

def manifest_files(model_root: Path):
    return sorted(Path(model_root).rglob('*.fmp-model.json')) if Path(model_root).exists() else []

def read_manifest(path: Path, repo_root: Path):
    data=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data,dict):
        raise ValueError(f'{path}: JSON object required')
    required=['building_id','year','up','role','glb']
    if any(k not in data for k in required):
        raise ValueError(f'{path}: missing {sorted(set(required)-set(data))}')
    building=str(data['building_id']); year=int(data['year'])
    up=data['up'];role=str(data['role'])
    if not SAFE_ID.fullmatch(building) or not SAFE_ID.fullmatch(role):
        raise ValueError(f'{path}: unsafe building or role')
    if year not in YEAR_SET or up not in ('X','Y','Z'):
        raise ValueError(f'{path}: invalid period year or up axis')
    nodes=data.get('nodes')
    if nodes is not None and (
        not isinstance(nodes,list) or not nodes
        or any(not isinstance(n,str) or not n for n in nodes)
        or len(set(nodes))!=len(nodes)
    ):
        raise ValueError(f'{path}: nodes must be a unique nonempty name list')
    glb=(path.parent/str(data['glb'])).resolve()
    if not glb.is_file() or glb.suffix.lower()!='.glb':
        raise FileNotFoundError(f'{path}: registered GLB missing: {glb}')
    source_path=os.path.relpath(glb,Path(repo_root).resolve()).replace('\\','/')
    return dict(glb=glb,source_path=source_path,building=building,
        year=year,up=up,role=role,nodes=nodes,asset_uri=str(data.get('asset_uri') or ''),
        scope=str(data.get('envelope_scope') or 'SELECTED_MODEL_COMPONENTS'))

def csv_text(fields,rows):
    import io
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n')
    writer.writeheader()
    writer.writerows(sorted(rows,key=lambda row:row[fields[0]]))
    return stream.getvalue()

def add_row(index,key,row,fields,immutable=False):
    item={f:'' if row.get(f) is None else str(row[f]) for f in fields}
    identity=item[key];old=index.get(identity)
    if immutable and old is not None and old!=item:
        raise ValueError(f'Immutable model asset/component collision: {key}={identity}')
    index[identity]=item

def refresh_registered_models(model_root: Path,catalog_dir: Path,
                              repo_root: Path=ROOT,dry_run=False,observed_utc=None):
    """Scan models, validate all before writing catalog CSVs; restore on error."""
    repo_root=Path(repo_root).resolve();catalog_dir=Path(catalog_dir)
    manifests=manifest_files(model_root)
    if not manifests:
        return dict(manifests=0,changed=0,models_scanned=0,components_added=0,
                    material_names=[],status='NO_REGISTERED_MODELS')
    datasets={name:read_csv(catalog_dir/name,fields)
              for name,fields,key in TABLE_FILES}
    if any(not (catalog_dir/name).exists() for name,fields,key in TABLE_FILES):
        raise FileNotFoundError('Required canonical master catalog files missing')
    indexes={name:{row[key]:dict(row) for row in datasets[name]}
             for name,fields,key in TABLE_FILES}
    seen=set();changed=0;parts=0;scanned=0;materials=set()
    timestamp=observed_utc or datetime.now(timezone.utc).isoformat()
    for path in manifests:
        m=read_manifest(path,repo_root)
        release_key=f'RELEASE-{m["building"]}-{m["year"]}-{m["role"]}'
        if release_key in seen:
            raise ValueError('Duplicate active source role in manifests: '+release_key)
        seen.add(release_key)
        sha=digest(m['glb'])
        option_hash=hashlib.sha256(json.dumps({
            'nodes':sorted(m['nodes']) if m['nodes'] else None,
            'up':m['up'],'scope':m['scope'],'role':m['role'],
        },sort_keys=True).encode('utf-8')).hexdigest()[:8]
        asset=(f'MDL-{m["building"]}-{m["year"]}-{m["role"]}'
               f'-{sha[:12]}-{option_hash}')
        previous=indexes['master_active_model_releases.csv'].get(release_key)
        if previous and previous['active_media_id']==asset and previous['source_sha256']==sha:
            continue
        result=inspect(m['glb'],m['building'],m['year'],m['up'],asset,
                       select=m['nodes'],role=m['role'],
                       expected_sha=sha,scope=m['scope'])
        scanned+=1
        if digest(m['glb'])!=sha:
            raise RuntimeError('Source GLB changed during scan: '+str(m['glb']))
        for row in result['components']:
            add_row(indexes['master_model_components.csv'],'component_id',
                    row,FIELDS,immutable=True)
        parts+=len(result['components'])
        materials.update(result['materials'])
        add_row(indexes['master_building_envelopes.csv'],'envelope_id',
                result['envelope'],ENV_FIELDS,immutable=True)
        media=dict(
            media_id=asset,title=f'{m["building"]} {m["year"]} {m["role"]} {sha[:12]}',
            kind='3D_GLB',period_year=m['year'],uri=m['asset_uri'],
            repo_path='',mime_type='model/gltf-binary',sha256=sha,
            rights_status='PROJECT_SOURCE_RIGHTS_REVIEW',
            acquisition_status='LOCAL_MODEL_INSPECTED',
            notes='A local file is not proof of Google Drive backup or public distribution.'
        )
        add_row(indexes['master_media_assets.csv'],'media_id',media,
                MEDIA_FIELDS,immutable=True)
        link=dict(link_id='LINK-'+asset,building_id=m['building'],
                  media_id=asset,period_year=m['year'],
                  role='REGISTERED_MODEL_VERSION',component_id='',
                  notes='See master_active_model_releases for current version')
        add_row(indexes['master_building_media.csv'],'link_id',link,
                LINK_FIELDS,immutable=True)
        release=dict(release_key=release_key,building_id=m['building'],
            period_year=m['year'],logical_role=m['role'],
            active_media_id=asset,source_path=m['source_path'],
            source_sha256=sha,up_axis=m['up'],
            selected_nodes=json.dumps(sorted(m['nodes'])) if m['nodes'] else '',
            observed_utc=timestamp,
            status='MODEL_OBSERVED_NOT_HISTORIC_CERTIFIED')
        add_row(indexes['master_active_model_releases.csv'],'release_key',
                release,RELEASE_FIELDS)
        changed+=1
    summary=dict(manifests=len(manifests),changed=changed,
                 models_scanned=scanned,components_added=parts,
                 material_names=sorted(materials),
                 status='DRY_RUN' if dry_run else ('UPDATED' if changed else 'UNCHANGED'))
    if not changed or dry_run:return summary
    content={name:csv_text(fields,list(indexes[name].values()))
             for name,fields,key in TABLE_FILES}
    with tempfile.TemporaryDirectory(prefix='.fmp-model-refresh-',dir=catalog_dir) as tmp:
        stage=Path(tmp)
        for name,value in content.items():
            (stage/name).write_text(value,encoding='utf-8')
        written=[]
        try:
            for name in content:
                shutil.copy2(catalog_dir/name,stage/(name+'.backup'))
                os.replace(stage/name,catalog_dir/name)
                written.append(name)
        except Exception:
            for name in reversed(written):
                os.replace(stage/(name+'.backup'),catalog_dir/name)
            raise
    return summary

def main():
    p=argparse.ArgumentParser(description=__doc__)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--once',action='store_true')
    mode.add_argument('--watch',action='store_true')
    p.add_argument('--model-root',type=Path,default=ROOT/'models/incoming')
    p.add_argument('--catalog-dir',type=Path,default=ROOT/'catalog')
    p.add_argument('--interval',type=float,default=4)
    p.add_argument('--dry-run',action='store_true')
    a=p.parse_args()
    if a.watch and a.interval<1:
        raise ValueError('Minimum polling interval: one second')
    def go():
        result=refresh_registered_models(a.model_root,a.catalog_dir,dry_run=a.dry_run)
        if result['changed']:print(json.dumps(result,indent=2),flush=True)
        return result
    if a.once:
        print(json.dumps(go(),indent=2))
    else:
        print('FMP GLB watcher: registered sidecar models only.')
        try:
            while True:
                try:go()
                except Exception as exc:
                    print('Model update blocked; previous catalog retained:',exc,flush=True)
                time.sleep(a.interval)
        except KeyboardInterrupt:
            print('Model watcher stopped.')

if __name__=='__main__':main()
