"""Provisional runtime-only transition; preserves source and print meshes."""
import hashlib,json,sys,tempfile
from pathlib import Path
import numpy as np
import trimesh
try:
    from tools.world_build.audit_helicline_join import world_mesh,vertical_surface,SOURCE_SHA
    from tools.world_build.build_theme_center_guest_flow_v002 import generate_v002
    from tools.world_build.build_theme_center_guest_flow_v001 import box_segment
except ImportError:
    from audit_helicline_join import world_mesh,vertical_surface,SOURCE_SHA
    from build_theme_center_guest_flow_v002 import generate_v002
    from build_theme_center_guest_flow_v001 import box_segment

NAME='PROVISIONAL_Helicline_Surface_Transition_r3'

def build(source,out):
    source,out=Path(source),Path(out)
    if hashlib.sha256(source.read_bytes()).hexdigest()!=SOURCE_SHA:
        raise ValueError('Unknown source revision')
    out.mkdir(parents=True,exist_ok=True)
    original=trimesh.load(source,force='scene')
    helix=world_mesh(original,'Helicline_Deck_and_Curved_Soffit')
    floor=float(world_mesh(original,'Return_Bridge_Deck').bounds[1,1])
    endpoint=np.array([-32.5,floor,-9.5])
    start=np.array([-35.6,floor,-3.15])
    direction=endpoint-start; direction/=np.linalg.norm(direction)
    across=np.array([-direction[2],0,direction[0]])
    # Replace the final 0.5 m of the flat route and extend 0.5 m over the ramp.
    entry=endpoint-.5*direction
    exitpoint=endpoint+.5*direction
    along=np.linspace(0,1,21); lateral=np.linspace(-1.05,1.05,43)
    top=[]; gaps=[]; exit_heights=[]
    for side in lateral:
        p=exitpoint+side*across
        hit=vertical_surface(helix,p[[0,2]],floor)
        if hit is None:raise ValueError('Unsupported transition exit')
        exit_heights.append(hit['surface_y_m'])
    for t in along:
        for j,side in enumerate(lateral):
            p=entry+t*direction+side*across
            hit=vertical_surface(helix,p[[0,2]],floor)
            if hit is None:raise ValueError('Unsupported transition footprint')
            if t==0 and hit['surface_y_m']>floor+1e-5:
                raise ValueError('Ramp protrudes above entry')
            # Avoid placing the transition surface below the existing ramp.
            p[1]=max(floor*(1-t)+exit_heights[j]*t,hit['surface_y_m'])
            gaps.append(p[1]-hit['surface_y_m']);top.append(p)
    top=np.array(top); n=len(top); cols=len(lateral); faces=[]
    for i in range(len(along)-1):
        for j in range(cols-1):
            a=i*cols+j;b=a+cols
            faces.extend([[a,b,b+1],[a,b+1,a+1]])
    # Close a 160 mm vertical-thickness preview solid, not a printable approval.
    top_faces=np.array(faces)
    faces.extend((top_faces[:,::-1]+n).tolist())
    boundary=list(range(cols))+[i*cols+cols-1 for i in range(1,len(along))]
    boundary+=list(range(n-2,n-cols-1,-1))+[i*cols for i in range(len(along)-2,0,-1)]
    for a,b in zip(boundary,boundary[1:]+boundary[:1]):
        faces.extend([[a,b,b+n],[a,b+n,a+n]])
    bottom=top-[0,.16,0]
    mesh=trimesh.Trimesh(vertices=np.vstack([top,bottom]),faces=faces,process=False)
    mesh.fix_normals()
    if not mesh.is_watertight or not mesh.is_winding_consistent:raise ValueError('Invalid transition solid')
    mesh.visual.face_colors=[170,175,180,255]
    with tempfile.TemporaryDirectory() as temp:
        previous=generate_v002(source,Path(temp))
        overlay=trimesh.load(Path(temp)/previous['output_runtime_glb'],force='scene')
    old='PROVISIONAL_ReturnViaTrylon_04'
    _,key=overlay.graph[old]
    overlay.delete_geometry(key)
    overlay.add_geometry(box_segment(start,entry,width=2.10),node_name=old,geom_name=old)
    overlay.add_geometry(mesh,node_name=NAME,geom_name=NAME)
    path=out/'ThemeCenter_1939_GuestFlow_Trim_v003.glb'
    path.write_bytes(overlay.export(file_type='glb'))
    # Evaluate slopes on actual triangulated surface, not just centerline endpoints.
    normals=mesh.face_normals[:len(top_faces)]
    slopes=np.linalg.norm(normals[:,[0,2]],axis=1)/np.abs(normals[:,1])
    report={'schema':'fmp.helicline-transition.v003','source_sha256':SOURCE_SHA,
      'source_unchanged':hashlib.sha256(source.read_bytes()).hexdigest()==SOURCE_SHA,
      'runtime_glb':path.name,'runtime_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'units':'MODEL_LOCAL_Y_UP_METRES','width_m':2.1,'length_m':1.0,
      'entry_center_m':entry.tolist(),'exit_center_m':exitpoint.tolist(),
      'entry_floor_y_m':floor,'exit_y_range_m':[min(exit_heights),max(exit_heights)],
      'sample_count':len(top),'max_surface_slope_ratio':float(max(slopes)),
      'sampled_ramp_penetration_max_m':float(max(0,-min(gaps))),
      'watertight':bool(mesh.is_watertight),'winding_consistent':bool(mesh.is_winding_consistent),
      'replaced_node':old,'new_node':NAME,'status':'PROVISIONAL_RUNTIME_ONLY',
      'integration':'Use this complete overlay instead of r2; hide original lower Perisphere shell and legacy shortcut as before.',
      'acceptance':'OPEN_WHOLE_SCENE_BODY_CLEARANCE_AND_UNREAL',
      'limits':['Grid samples do not certify continuous face clearance',
                'No whole-scene obstruction or capsule sweep performed',
                'Transition undersurface intentionally overlaps ramp for runtime preview',
                'Not historically measured, not print approved']}
    (out/'Helicline_Transition_v003.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: build_helicline_transition.py SOURCE.glb OUT')
    print(json.dumps(build(sys.argv[1],sys.argv[2]),indent=2))
