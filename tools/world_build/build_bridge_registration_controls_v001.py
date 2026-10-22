"""FMP v005 evidence-registered guide GLB; intentionally NOT reconstructed architecture.

Builds non-destructive bounding-volume wire guides from actual runtime node geometry.
The wire guides are not buildings and must be hidden in game/visitor views.
"""
from __future__ import annotations
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
import trimesh

SOURCE_SHA = 'de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439'
NODES = {
  'PUBLIC_ENTRANCE_LOBBY_REFERENCE_ONLY':'Trylon_Lobby_Floor_Envelope',
  'ESCALATOR_ONE_EXISTING_ENVELOPE':'Escalator_1_Envelope',
  'ESCALATOR_TWO_EXISTING_ENVELOPE':'Escalator_2_Envelope',
  'RETURN_BRIDGE_EXISTING_DECK':'Return_Bridge_Deck',
  'PERISPHERE_RUNTIME_LOWER_SHELL':'Perisphere_Lower_Removable_Shell__UNREAL_PORTALS_v001',
  'TRYLON_RUNTIME_EXTERIOR_SHELL':'Trylon_Hollow_Exterior__RUNTIME_SHARED_APERTURES_v004',
}
COLORS = {
  'PUBLIC_ENTRANCE_LOBBY_REFERENCE_ONLY':(247,190,56,255),
  'ESCALATOR_ONE_EXISTING_ENVELOPE':(23,129,211,255),
  'ESCALATOR_TWO_EXISTING_ENVELOPE':(246,110,50,255),
  'RETURN_BRIDGE_EXISTING_DECK':(17,159,125,255),
  'PERISPHERE_RUNTIME_LOWER_SHELL':(119,113,153,255),
  'TRYLON_RUNTIME_EXTERIOR_SHELL':(107,104,103,255),
}

def transformed_bounds(scene,name):
    """Bounding box from real *world-transformed* mesh vertices; no guessed coordinates."""
    if name not in scene.graph.nodes_geometry: raise ValueError('Missing source node '+name)
    transform,geometry=scene.graph[name]
    vertices=trimesh.transform_points(scene.geometry[geometry].vertices,transform)
    if not np.all(np.isfinite(vertices)): raise ValueError('Nonfinite source positions '+name)
    return np.array([vertices.min(axis=0),vertices.max(axis=0)])

def bbox_segments(bounds):
    """All twelve edges of an axis-aligned box in a Y-up model frame."""
    lo,hi=np.asarray(bounds,dtype=float)
    corners=[]
    for x in (lo[0],hi[0]):
      for y in (lo[1],hi[1]):
        for z in (lo[2],hi[2]): corners.append(np.array([x,y,z]))
    return [(corners[i],corners[j]) for i in range(8) for j in range(i+1,8) if (i^j).bit_count()==1]

def guide_node(bounds,color,radius=0.028):
    parts=[]
    for a,b in bbox_segments(bounds):
        line=b-a; length=float(np.linalg.norm(line))
        if length<radius/2: continue
        cyl=trimesh.creation.cylinder(radius=radius,height=length,sections=8)
        cyl.apply_transform(trimesh.geometry.align_vectors([0,0,1],line/length))
        cyl.apply_translation((a+b)/2)
        parts.append(cyl)
    if not parts: raise ValueError('Empty control box')
    merged=trimesh.util.concatenate(parts)
    merged.visual.vertex_colors=np.tile(np.asarray(color,dtype=np.uint8),(len(merged.vertices),1))
    return merged

def build(source,out):
    source,out=Path(source),Path(out)
    got=hashlib.sha256(source.read_bytes()).hexdigest()
    if got!=SOURCE_SHA:raise ValueError('Source GLB SHA-256 mismatch; refused')
    original=trimesh.load(source,force='scene')
    guides=trimesh.Scene()
    records=[]
    for label,node in NODES.items():
        bb=transformed_bounds(original,node)
        guide=guide_node(bb,COLORS[label])
        name='REFERENCE_ONLY__'+label
        guides.add_geometry(guide,node_name=name,geom_name=name)
        records.append({'label':label,'source_node':node,'type':'EXISTING_NODE_WORLD_AABB',
                        'bbox_min_xyz_m':bb[0].round(6).tolist(),
                        'bbox_max_xyz_m':bb[1].round(6).tolist(),
                        'bbox_center_xyz_m':bb.mean(axis=0).round(6).tolist(),
                        'wire_rgb':list(COLORS[label][:3]),'evidence_status':'DERIVED_FROM_RUNTIME_GLTF_GEOMETRY'})
    out.mkdir(parents=True,exist_ok=True)
    path=out/'FMP_ThemeCenter_Bridge_Registration_Controls_v001.glb'
    guides.export(path)
    check=trimesh.load(path,force='scene')
    expected={'REFERENCE_ONLY__'+x for x in NODES}
    if not expected.issubset(set(check.graph.nodes_geometry)):
        raise AssertionError('GLB node identity loss')
    for k in expected:
        node=next(row for row in records if 'REFERENCE_ONLY__'+row['label']==k)
        probe=transformed_bounds(check,k)
        min_expected=np.asarray(node['bbox_min_xyz_m'])
        max_expected=np.asarray(node['bbox_max_xyz_m'])
        if not (np.allclose(probe[0],min_expected,atol=.032) and np.allclose(probe[1],max_expected,atol=.032)):
            raise AssertionError('Unexpected envelope shift '+k)
    result={'schema':'fmp.bridge-photoregistration-controls.v001','source_name':source.name,
      'source_sha256':SOURCE_SHA,'result_name':path.name,'result_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'units':'metres','model_frame':'right-handed Y-up model-local UNREGISTERED',
      'object_count':len(records),'objects':records,
      'historical_architecture':'NOT_RECONSTRUCTED',
      'arc_profile':'NOT_MEASURED',
      'public_entrance_canopy':'NOT_MEASURED',
      'game_visibility':'HIDE_ALL_CONTROLS',
      'purpose':'Geometrical anchors and reference envelopes for calibrating archival photography against the actual runtime asset.',
      'limits':['Box edges are guide geometry and do not represent as-built wall/steel surfaces.',
        'Escalators are existing approximate model geometry, not actual engineering survey.',
        'No photograph camera calibration performed; no historical profile or fabricated entrance added.',
        'Do not add to any render scene as architectural elements.']}
    (out/'FMP_Bridge_Registration_Controls_v001.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('source');parser.add_argument('out');args=parser.parse_args()
    x=build(args.source,args.out)
    print(json.dumps({'source_hash_verified':True,'guide_objects':x['object_count'],'sha256':x['result_sha256'],'historical_architecture':x['historical_architecture']},indent=2))

if __name__=='__main__':main()
