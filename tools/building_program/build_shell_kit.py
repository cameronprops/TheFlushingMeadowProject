#!/usr/bin/env python3
"""FMP shell-first architecture extraction from a preserved GLB.

No generated preview is an as-built certification or a native engine test.
Source is NEVER edited. Geometry, unit conversions and SHA validated.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
import trimesh

SOURCE_HASH = 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5'
SHELL_NODES = ('Trylon_Hollow_Exterior','Perisphere_Upper_Removable_Shell','Perisphere_Lower_Removable_Shell')
INTERIOR_NODES = ('Interior_Projection_Liner','Trylon_Lobby_Floor_Envelope','Moving_Platform_1','Moving_Platform_2',
                  'Platform_1_Parapet_R50','Platform_1_Parapet_R58','Platform_2_Parapet_R50','Platform_2_Parapet_R67',
                  'Platform_1_Landing_Hypothesis','Platform_2_Landing_Hypothesis')
CIRCULATION_NODES = ('Return_Bridge_Deck','Helicline_Deck_and_Curved_Soffit','Helicline_Bridge_Transition_Hypothesis',
                     'Escalator_1_Envelope','Escalator_2_Envelope')
STRUCTURE_EXACT = ('Trylon_Face_1_Frame','Trylon_Face_2_Frame','Trylon_Face_3_Frame',
                   'Perisphere_Support_Ring','Helicline_Single_Column_Proxies')
STRUCTURE_PREFIXES = ('Perisphere_Column_','Meridian_Truss_','Latitude_Truss_')
SOURCE_REQUIRED = set(SHELL_NODES) | set(INTERIOR_NODES) | set(CIRCULATION_NODES) | set(STRUCTURE_EXACT)
# Source Y-up to print Z-up, right-handed 90-degree rotation about X.
TO_PRINT = np.array([[1,0,0], [0,0,-1], [0,1,0]],dtype=np.float64)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def group_for(name):
    if name in SHELL_NODES: return 'EXTERIOR_SHELL'
    if name in INTERIOR_NODES: return 'INTERIOR_SHELL_AND_VIEWING'
    if name in CIRCULATION_NODES: return 'GUEST_CIRCULATION_PREVIEW'
    if name in STRUCTURE_EXACT or name.startswith(STRUCTURE_PREFIXES): return 'OPTIONAL_STEEL_STRUCTURE'
    return None


def flatten_node(scene, name):
    transform,mesh_name=scene.graph[name]
    if mesh_name is None: raise ValueError('Expected mesh at node: '+name)
    mesh=scene.geometry[mesh_name].copy()
    mesh.apply_transform(transform)
    return mesh


def print_mesh(mesh, scale_denominator):
    if not mesh.is_watertight:
        raise ValueError('Cannot issue printable mesh for a nonwatertight source shell')
    m=mesh.copy()
    m.vertices=(m.vertices @ TO_PRINT.T) * (1000.0 / scale_denominator)
    lo,hi=m.bounds
    m.vertices[:,0]-=(lo[0]+hi[0])/2
    m.vertices[:,1]-=(lo[1]+hi[1])/2
    m.vertices[:,2]-=lo[2]
    if not m.is_watertight or not m.is_winding_consistent:
        raise ValueError('Print geometry lost manifold winding after conversion')
    return m


def mesh_stats(mesh):
    return {'faces':len(mesh.faces), 'watertight':bool(mesh.is_watertight),
            'winding_consistent':bool(mesh.is_winding_consistent),
            'bounds_size_m':[round(float(x),6) for x in mesh.extents],
            'volume_m3':round(float(abs(mesh.volume)),6)}


def build(source, target, include_structure=True):
    source=Path(source); target=Path(target); target.mkdir(parents=True,exist_ok=True)
    observed_hash=sha256(source)
    if observed_hash!=SOURCE_HASH:
        raise ValueError('Source SHA mismatch. Cannot apply reviewed named-node source map.')
    src=trimesh.load(source,force='scene')
    missing=SOURCE_REQUIRED-set(src.graph.nodes)
    if missing: raise ValueError('Missing expected scene nodes: '+repr(sorted(missing)))
    grouped={key:trimesh.Scene() for key in ('EXTERIOR_SHELL','INTERIOR_SHELL_AND_VIEWING','GUEST_CIRCULATION_PREVIEW','OPTIONAL_STEEL_STRUCTURE')}
    part_records=[];counts={key:0 for key in grouped}
    for name in sorted(src.graph.nodes):
        group=group_for(name)
        if not group:continue
        obj=flatten_node(src,name)
        grouped[group].add_geometry(obj,node_name=name,geom_name=name)
        counts[group]+=1
        part_records.append({'node_name':name,'layer':group,'historical_certified':False,**mesh_stats(obj)})
    if not include_structure:grouped.pop('OPTIONAL_STEEL_STRUCTURE')
    output_files={}
    for kind,sc in grouped.items():
        path=target/('ThemeCenter_'+kind+'.glb')
        sc.export(path)
        readback=trimesh.load(path,force='scene')
        assert len(readback.geometry)>0 and len(readback.graph.nodes)>0
        output_files[kind]={'file':path.name,'bytes':path.stat().st_size,'sha256':sha256(path),'objects':counts[kind]}
    preview=trimesh.Scene()
    for kind in ('EXTERIOR_SHELL','INTERIOR_SHELL_AND_VIEWING','GUEST_CIRCULATION_PREVIEW'):
        for name in sorted(src.graph.nodes):
            if group_for(name)==kind:
                preview.add_geometry(flatten_node(src,name),geom_name=name,node_name=name)
    preview_file=target/'ThemeCenter_ShellFirst_RealTime.glb'
    preview.export(preview_file)
    output_files['UNREAL_SHELL_FIRST_PREVIEW']={'file':preview_file.name,'sha256':sha256(preview_file),'bytes':preview_file.stat().st_size,
                                                'collision_test':'NOT_TESTED_IN_UNREAL'}
    printing=[]
    for name in SHELL_NODES:
        source_mesh=flatten_node(src,name)
        for scale in ([800] if name=='Trylon_Hollow_Exterior' else [800,250,200]):
            part=print_mesh(source_mesh,scale)
            file=f'PRINT_{name}_1to{scale}_mm.stl'
            part.export(target/file,file_type='stl')
            measured_mm=[round(float(x),2) for x in part.extents]
            readback=trimesh.load_mesh(target/file,file_type='stl')
            if not readback.is_watertight:raise ValueError('STL validation failed: '+file)
            printing.append({'source_node':name,'file':file,'scale_denominator':scale,'units':'millimeters_by_contract',
                             'box_mm_xyz':measured_mm,'is_watertight':bool(readback.is_watertight),
                             'is_volume':bool(readback.is_volume), 'is_winding_consistent':bool(readback.is_winding_consistent),
                             'source_geometry_watertight':bool(source_mesh.is_watertight),
                             'printer_fit_requires_check':True,'minimum_wall_thickness_checked':False,
                             'assemblies_require_alignment_and_slicer_check':True,'sha256':sha256(target/file)})
    with (target/'part_inventory.csv').open('w',newline='',encoding='utf8') as f:
        keys=list(part_records[0]);writer=csv.DictWriter(f,fieldnames=keys);writer.writeheader();writer.writerows(part_records)
    profile={'schema':'fmp.shell-first.v1','building_ids':['WF0001','WF0002'],'related_place_ids':['WF0003','WF0004'],
             'source_sha256':observed_hash,'original_source_nodes':len(src.graph.nodes),
             'model_coordinate_system':'meters; source GLB Y-up, unregistered site local',
             'normal_product_layers':['EXTERIOR_SHELL','INTERIOR_SHELL_AND_VIEWING','GUEST_CIRCULATION_PREVIEW'],
             'optional_product_layers':['OPTIONAL_STEEL_STRUCTURE'],
             'layer_counts':counts,'exports':output_files,'print_parts':printing,
             'print_mode':'Mesh samples only; slicer validation, wall measurement, orienting, supports and join design outstanding',
             'source_unmodified':sha256(source)==observed_hash,'realism_status':'INTERPRETIVE_GEOMETRY_USING_PERIOD_CONSTRAINTS',
             'collision_status':'NOT_TESTED','walkthrough_status':'NOT_TESTED',
             'structural_animation_use':'Optional steel layer can feed future construction staging. Sequence and member connections not validated.',
             'unresolved':['evidence-based material/color','interior shell thickness and entrances','3D-print wall and overhang checks',
                           'Trylon 1:200 split/key design for desk printer','historically measured XY and footprint','engine collision']}
    (target/'manifest.json').write_text(json.dumps(profile,indent=2)+'\n',encoding='utf8')
    return profile

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    m=build(args.source,args.out)
    print('Source',m['original_source_nodes'],'nodes; classified',m['layer_counts'])
    print('3D print parts',len(m['print_parts']))
