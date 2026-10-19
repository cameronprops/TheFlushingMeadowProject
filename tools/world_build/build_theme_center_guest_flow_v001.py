#!/usr/bin/env python3
"""FMP: derive 1939 visitor circulation delta from preserved Theme Center GLB.
Source remains untouched; cutout mesh is only for Unreal, never for printing.
Usage: python build_theme_center_guest_flow_v001.py SOURCE.glb OUTPUT_DIRECTORY
"""
import hashlib, json, sys
from pathlib import Path
import numpy as np
import trimesh

SOURCE_SHA='a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5'
NAMES=['Perisphere_Lower_Removable_Shell','Platform_1_Landing_Hypothesis',
       'Platform_2_Landing_Hypothesis','Return_Bridge_Deck','Trylon_Hollow_Exterior',
       'Helicline_Deck_and_Curved_Soffit']

def mesh(scene,name):
    T,key=scene.graph[name]
    out=scene.geometry[key].copy();out.apply_transform(T)
    return out

def box_segment(a,b,width=1.85,thickness=.16):
    a,b=np.array(a,float),np.array(b,float)
    d=b-a;length=np.linalg.norm(d[[0,2]])
    if length<.01: raise ValueError('Degenerate deck segment')
    part=trimesh.creation.box(extents=(length,thickness,width))
    part.apply_transform(trimesh.geometry.align_vectors([1,0,0],[d[0]/length,0,d[2]/length]))
    part.apply_translation((a+b)/2)
    return part

def generate(glb,destination):
    glb=Path(glb);destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    actual=hashlib.sha256(glb.read_bytes()).hexdigest()
    if actual!=SOURCE_SHA:raise RuntimeError('Unknown GLB revision; refuse geometry changes')
    scene=trimesh.load(glb,force='scene')
    if any(k not in scene.graph.nodes for k in NAMES): raise ValueError('Unexpected GLB node set')
    original=mesh(scene,NAMES[0]);low=mesh(scene,NAMES[1]).bounds.mean(axis=0)
    high=mesh(scene,NAMES[2]).bounds.mean(axis=0)
    deck=mesh(scene,NAMES[3]).bounds.mean(axis=0)
    # Interpretation-only openings. The original source GLB is never modified.
    triangles=original.vertices[original.faces]
    remain=np.ones(len(original.faces),bool)
    for yc,zc in ((low[1],low[2]),(high[1],high[2])):
        remain &= ~((triangles[:,:,0].min(axis=1)<-15)&
            (triangles[:,:,1].max(axis=1)>=yc-1.2)&
            (triangles[:,:,1].min(axis=1)<=yc+1.2)&
            (triangles[:,:,2].max(axis=1)>=zc-1.175)&
            (triangles[:,:,2].min(axis=1)<=zc+1.175))
    shell=trimesh.Trimesh(vertices=original.vertices.copy(),faces=original.faces[remain],process=False)
    if shell.is_watertight or remain.all():raise RuntimeError('No portal opening found')
    output=trimesh.Scene()
    output.add_geometry(shell,node_name='Perisphere_Lower_Removable_Shell__UNREAL_PORTALS_v001')
    # Provisional outdoor stairs between the source platform and return bridge.
    start=np.array([-24.70,high[1],high[2]])
    finish=np.array([-30.25,deck[1],deck[2]])
    h=finish-start;h[1]=0
    rise=high[1]-deck[1];count=max(2,round(rise/.16));tread=np.linalg.norm(h[[0,2]])/count
    if rise/count>.18 or tread<.25:raise ValueError('Invalid provisional stair ratio')
    output.add_geometry(box_segment(high,start),node_name='PROVISIONAL_UpperLandingToStair')
    for i in range(count):
        p=start+h*i/count;q=start+h*(i+1)/count
        p[1]=q[1]=high[1]-rise*(i+1)/count
        output.add_geometry(box_segment(p,q),node_name='PROVISIONAL_UpperReturnStair_%02d'%(i+1))
    output.add_geometry(box_segment(finish,finish+[-3,0,0]),node_name='PROVISIONAL_StairBottom')
    # The source shortcut bypasses Trylon. This path passes through the source
    # Trylon's existing east-facing open zone but remains an interpretive guide.
    near=np.array([-35.9,deck[1],deck[2]])
    inside=np.array([mesh(scene,'Trylon_Hollow_Exterior').bounds.mean(axis=0)[0],deck[1],deck[2]])
    turn=np.array([inside[0],deck[1],-3.15]);ex=np.array([-35.6,deck[1],-3.15])
    helix=np.array([-32.5,deck[1],-9.5])
    for i,(a,b) in enumerate([(near,inside),(inside,turn),(turn,ex),(ex,helix)]):
        output.add_geometry(box_segment(a,b,width=2.10),node_name='PROVISIONAL_ReturnViaTrylon_%02d'%(i+1))
    output_glb=destination/'ThemeCenter_1939_Circulation_Portal_Delta_v001.glb'
    output_glb.write_bytes(output.export(file_type='glb'))
    manifest={
      'schema':'fmp.theme.center.guest-flow.v1','buildings':['WF0001','WF0002'],
      'source_file_sha256':actual,'source_unchanged':True,
      'units':'metres','up_axis':'Y','site_registered':False,
      'unreal_overlay':output_glb.name,
      'replace_preview_visual_node_only':'Perisphere_Lower_Removable_Shell',
      'keep_printing_source_nodes':['Perisphere_Lower_Removable_Shell','Perisphere_Upper_Removable_Shell'],
      'hide_legacy_shortcut':'Helicline_Bridge_Transition_Hypothesis',
      'portals':{'count':2,'height_m':2.4,'width_m':2.35,'status':'INTERPRETIVE_NOT_AS_BUILT'},
      'stairs':{'count':count,'drop_m':rise,'tread_m':tread,'riser_m':rise/count,'historical_status':'NOT_SURVEYED'},
      'removed_source_triangles':int((~remain).sum()),
      'route':['TRYLON_ENTRANCE','ESCALATORS','PERISPHERE_VIEWING','LOWER_DIRECT_TO_RETURN_BRIDGE','UPPER_STAIRS_TO_RETURN_BRIDGE','RETURN_THROUGH_TRYLON','HELICLINE_EXIT'],
      'blocked_acceptance':['survey actual portal shapes/levels','verify return route and Helicline landing against plans','Unreal collision and step navigation','no printer wall thickness certification'],
      'certification':'RECONSTRUCTION_PREVIEW_ONLY'
    }
    (destination/'ThemeCenter_1939_Circulation_Short_Manifest_v001.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit(__doc__)
    print(json.dumps(generate(sys.argv[1],sys.argv[2]),indent=2))
