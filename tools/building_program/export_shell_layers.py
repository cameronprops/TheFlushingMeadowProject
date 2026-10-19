#!/usr/bin/env python3
"""FMP profile-driven layer extraction from existing verified-hash GLBs.

Use to separate exterior, public interior, landscape and animated show assets.
No geometry is reconstructed here; no steel is required; no Unreal host testing.
"""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
import trimesh

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def export(source, profile, out):
    source=Path(source);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    settings=json.loads(Path(profile).read_text())
    hash_value=sha256(source)
    if hash_value!=settings['source_sha256']:
        raise ValueError('Source GLB hash differs from reviewed model')
    scene=trimesh.load(source,force='scene')
    rules=[(re.compile(x['pattern']),x['role']) for x in settings['rules']]
    counts={};products={};unmatched=[];node_map=[]
    for node in sorted(scene.graph.nodes):
        if node=='world':continue
        T,g=scene.graph[node]
        if g is None:continue
        hits=[role for rex,role in rules if rex.search(node)]
        if len(hits)>1:raise ValueError('Ambiguous role for node '+node)
        if not hits:
            unmatched.append(node)
            continue
        role=hits[0]
        target=products.setdefault(role,trimesh.Scene())
        part=scene.geometry[g].copy();part.apply_transform(T)
        target.add_geometry(part,node_name=node,geom_name=node)
        counts[role]=counts.get(role,0)+1
        node_map.append([node,role,len(part.faces),bool(part.is_watertight)])
    if unmatched and settings.get('fail_on_unclassified',True):
        raise ValueError('Unclassified named source parts: '+repr(unmatched[:20]))
    outputs={}
    for role,product in products.items():
        if not product.geometry:continue
        file=f"{settings['building_id']}_{role}.glb"
        product.export(out/file)
        readback=trimesh.load(out/file,force='scene')
        if len(readback.geometry)!=counts[role]:
            raise AssertionError('Expected role asset count mismatch')
        outputs[role]={'file':file,'sha256':sha256(out/file),'nodes':counts[role]}
    with (out/'node_roles.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['node_name','role','faces','watertight']);w.writerows(node_map)
    report={'schema':'fmp.pavilion-layer-export.v1','building_id':settings['building_id'],
            'original_file':source.name,'source_sha256':hash_value,
            'source_mesh_nodes':sum(1 for n in scene.graph.nodes if scene.graph[n][1] is not None),
            'classified_nodes':sum(counts.values()),'unclassified_names':unmatched,
            'outputs':outputs,'model_accuracy':settings['model_accuracy'],
            'steel_required':False,'original_source_unchanged':sha256(source)==hash_value,
            'walkthrough_test':'NOT_TESTED_IN_UNREAL','print_suitability':'NOT_TESTED',
            'source_position_verified':False}
    (out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--model',required=True);p.add_argument('--profile',required=True)
    p.add_argument('--out',required=True);a=p.parse_args()
    print(json.dumps(export(a.model,a.profile,a.out)['outputs'],indent=2))
