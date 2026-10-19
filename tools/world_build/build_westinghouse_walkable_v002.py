#!/usr/bin/env python3
"""FMP Westinghouse 1939 visitor-access PROXY.

Input: existing source-preserved 329-object Westinghouse exterior v001 GLB.
Output: an accessibility study, not as-built interior reconstruction.
Public entry paths/doors and the floors are *hypothetical* until plans are acquired.
"""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import trimesh

REMOVED_SOLIDS = {'WH39_WING_WEST_SHELL','WH39_WING_EAST_SHELL','WH39_REAR_CONNECTOR'}
FEET = 0.3048
HEIGHT_WING = 55*FEET
HEIGHT_REAR = 11.5

class Builder:
    def __init__(self,scene):
        self.scene=scene
        self.created=[]
    def add(self,name,mesh,category,color):
        if name in self.scene.geometry:
            raise ValueError('Duplicate part ID: '+name)
        mesh.visual.vertex_colors=np.tile(np.asarray(color,dtype=np.uint8),(len(mesh.vertices),1))
        mesh.metadata.update(fmp_build='ACCESS_PREVIEW_ONLY',collision_category=category,
          historical_interior='UNVERIFIED',proposed_accessible=True)
        self.scene.add_geometry(mesh,geom_name=name,node_name=name)
        self.created.append({'id':name,'collision_category':category,'vertex_count':len(mesh.vertices),
                             'triangle_count':len(mesh.faces),'is_historical_measurement':False})
    def slab(self,name,polygon,z,thickness,category,color):
        """Simple polygon fan since footprint is convex; independent triangles."""
        points=np.asarray(polygon,float)
        center=points.mean(axis=0)
        vertices=np.array([(float(p[0]),float(p[1]),level) for level in (z,z+thickness)
                           for p in [*points,center]],dtype=float)
        n=len(points)
        faces=[]
        for k in range(n):
            j=(k+1)%n
            faces.extend([(n,k,j),(2*n+1,n+1+j,n+1+k),
                          (k,j,n+1+j),(k,n+1+j,n+1+k)])
        mesh=trimesh.Trimesh(vertices=vertices,faces=faces,process=False)
        self.add(name,mesh,category,color)
    def wall(self,name,x0,y0,x1,y1,base,top,color):
        length=math.hypot(x1-x0,y1-y0)
        if length<.02:return
        mesh=trimesh.creation.box(extents=[length,.22,top-base])
        mesh.apply_transform(trimesh.transformations.rotation_matrix(math.atan2(y1-y0,x1-x0),[0,0,1]))
        mesh.apply_translation(((x0+x1)/2,(y0+y1)/2,(base+top)/2))
        self.add(name,mesh,'WALL',color)

def divide_edge(builder,prefix,a,b,opening_center,opening_width,top):
    """Leave a generous, provisional full-height opening in the wall section."""
    p=np.asarray(a,float);q=np.asarray(b,float)
    vec=q-p
    d=np.linalg.norm(vec)
    if d<1e-7:raise ValueError('Degenerate edge')
    direction=vec/d
    center=np.asarray(opening_center,float)
    t=np.dot(center-p,direction)
    low=max(0.0,t-opening_width/2)
    high=min(d,t+opening_width/2)
    if not (0.25<low<high<d-0.25):raise ValueError('Opening outside segment')
    s=p+direction*low;e=p+direction*high
    builder.wall(prefix+'_LEFT',*p,*s,0,top,[212,204,191,255])
    builder.wall(prefix+'_RIGHT',*e,*q,0,top,[212,204,191,255])
    return dict(width_m=float(high-low),center_xy=[float(center[0]),float(center[1])],height_m=top,
                historic_status='INFERRED_TEST_PASSAGE_NOT_AS_BUILT')

def build(source_path,out_dir):
    raw=Path(source_path).read_bytes()
    sha=hashlib.sha256(raw).hexdigest()
    scene=trimesh.load(source_path,force='scene')
    if len(scene.geometry)!=329 or not REMOVED_SOLIDS.issubset(scene.geometry):
        raise ValueError('Expected original 329-part Westinghouse schematic; inspect source version')
    input_names=set(scene.geometry)
    for key in sorted(REMOVED_SOLIDS):
        # Removing graph node also clears geometry for independent named nodes.
        scene.delete_geometry(key)
    b=Builder(scene)
    doors=[]
    northing_hypothesis='LOCAL_ONLY_NO_SURVEY_REGISTRATION'
    for side,label in [(-1,'WEST'),(1,'EAST')]:
        cx=side*30.5
        x0,x1=cx-17.5,cx+17.5
        xs=np.linspace(x0,x1,21)
        front=[(float(x),float(-4.5*math.sin(math.pi*(x-x0)/35))) for x in xs]
        polygon=front+[(x1,26.),(x0,26.)]
        b.slab('WH39_ACCESS_'+label+'_FLOOR',polygon,-.20,.20,'WALKABLE_FLOOR',[199,190,166,255])
        b.slab('WH39_ACCESS_'+label+'_ROOF',polygon,HEIGHT_WING-.24,.24,'ROOF',[210,210,196,255])
        # Rather than occupy the glazing as an opaque barrier, trace transparent
        # collision-wall strips except for a 4.4m provisional entry at front.
        for i,(a,c) in enumerate(zip(front[:-1],front[1:])):
            mid=(a[0]+c[0])/2
            if abs(mid-cx)<2.35:
                continue
            b.wall('WH39_ACCESS_'+label+'_FRONTWALL_'+str(i).zfill(2),*a,*c,0,HEIGHT_WING,[168,192,201,94])
        inner_x=x1 if side<0 else x0
        outer_x=x0 if side<0 else x1
        b.wall('WH39_ACCESS_'+label+'_OUTER_SIDE',outer_x,front[0][1] if side<0 else front[-1][1],outer_x,26,0,HEIGHT_WING,[218,214,197,255])
        b.wall('WH39_ACCESS_'+label+'_INNER_SIDE',inner_x,front[-1][1] if side<0 else front[0][1],inner_x,26,0,HEIGHT_WING,[218,214,197,255])
        # Rear door toward connector in the overlap zone near +/-16 metres.
        rear_door_x=-16.5 if side<0 else 16.5
        rear_segment=divide_edge(b,'WH39_ACCESS_'+label+'_BACK',
                                 (x0,26),(x1,26),(rear_door_x,26),4.4,HEIGHT_WING)
        doors.append(dict(id='WH39_ACCESS_'+label+'_REAR_DOOR',**rear_segment))
        doors.append(dict(id='WH39_ACCESS_'+label+'_FRONT_GLAZING_GAP',
                          width_m=4.4,center_xy=[cx,0],height_m=HEIGHT_WING,
                          historic_status='PROVISIONAL_PROXY_OPENING'))
    # Connector y=22..35, x=-19.5..19.5. Side openings lead to rear wing doors.
    rect=[(-19.5,22),(19.5,22),(19.5,35),(-19.5,35)]
    b.slab('WH39_ACCESS_CONNECTOR_FLOOR',rect,-.20,.20,'WALKABLE_FLOOR',[199,190,166,255])
    b.slab('WH39_ACCESS_CONNECTOR_ROOF',rect,HEIGHT_REAR-.24,.24,'ROOF',[213,207,191,255])
    doors.append(dict(id='WH39_ACCESS_CENTRAL_PUBLIC_ENTRY',**divide_edge(b,'WH39_ACCESS_CONNECTOR_FRONT',(-19.5,22),(19.5,22),(0,22),5.0,HEIGHT_REAR)))
    b.wall('WH39_ACCESS_CONNECTOR_BACK',-19.5,35,19.5,35,0,HEIGHT_REAR,[218,214,197,255])
    for side,label in [(-1,'WEST'),(1,'EAST')]:
        x=side*19.5
        doors.append(dict(id='WH39_ACCESS_CONNECTOR_'+label+'_WING_LINK',**divide_edge(b,'WH39_ACCESS_CONNECTOR_'+label+'_SIDE',(x,22),(x,35),(x,26),4.0,HEIGHT_REAR)))
    # Stable engineering waypoints. These are not source-supported floorplans.
    routes=[
      {'id':'WH39_ROUTE_CENTRAL_TO_WEST', 'local_m':[[5,12,0],[5,20,0],[0,25,0],[-16.0,25,0],[-25,20,0],[-30.5,10,0]]},
      {'id':'WH39_ROUTE_CENTRAL_TO_EAST', 'local_m':[[5,12,0],[5,20,0],[0,25,0],[16.0,25,0],[25,20,0],[30.5,10,0]]}
    ]
    out_dir=Path(out_dir)
    out_dir.mkdir(parents=True,exist_ok=True)
    path=out_dir/'Westinghouse_1939_Visitor_Access_Proxy_v002.glb'
    scene.export(path)
    check=trimesh.load(path,force='scene')
    expected=len(input_names)-len(REMOVED_SOLIDS)+len(b.created)
    if len(check.geometry)!=expected:
        raise AssertionError('GLB scene node mismatch; expected %s got %s' %(expected,len(check.geometry)))
    if not set(input_names-REMOVED_SOLIDS).issubset(check.geometry):
        raise AssertionError('Existing exterior geometry unexpectedly lost')
    manifest={'schema':'fmp.walkable-building-proxy.v0.2','building_id':'WF0020','year':1939,
      'status':'VISITOR_ROUTE_GEOMETRY_PROTOTYPE_UNTESTED_IN_UNREAL',
      'source_glb_sha256':sha,'output_glb_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'original_component_count':len(input_names),'removed_blocking_solid_names':sorted(REMOVED_SOLIDS),
      'preserved_original_component_count':len(input_names-REMOVED_SOLIDS),
      'new_accessibility_geometry_count':len(b.created),'total_component_count':len(check.geometry),
      'site_registration':northing_hypothesis,'shared_local_axes':'X_RIGHT_Y_DEPTH_Z_UP_METRES',
      'historical_truth':'150ft tower height sourced; all interior floorplan, openings and walks are test constructs',
      'new_components':b.created,'provisional_doors':doors,'visitor_routes':routes,
      'collision_status':'NOT_ENGINE_TESTED','walkthrough_status':'NOT_ENGINE_TESTED',
      'site_alignment_status':'NOT_SITE_PLACED','appearance_variant_status':'REALISTIC_AND_STYLIZED_PENDING',
      'safety_warning':'Do not use this routing as real emergency egress; a visitor exploration prototype only.'}
    (out_dir/'Westinghouse_Visitor_Access_Proxy_v002.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return path,manifest

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input_glb',type=Path)
    ap.add_argument('--output-dir',type=Path,required=True)
    args=ap.parse_args()
    path,manifest=build(args.input_glb,args.output_dir)
    print(json.dumps({'output':str(path),'components':manifest['total_component_count'],
                      'new':manifest['new_accessibility_geometry_count'],
                      'sha256':manifest['output_glb_sha256']},indent=2))
if __name__=='__main__':main()