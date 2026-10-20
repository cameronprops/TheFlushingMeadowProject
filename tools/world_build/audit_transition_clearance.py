"""Offline sampled capsule surface-clearance screen; never an Unreal certification."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
import trimesh
try:
    from tools.world_build.audit_helicline_join import world_mesh,vertical_surface,SOURCE_SHA
except ImportError:
    from audit_helicline_join import world_mesh,vertical_surface,SOURCE_SHA
OVERLAY_SHA='2a0f46ebe5ac0636f1b319dadb0dd30ea77b561096cf014733fe9bf030b523aa'
HIDDEN={'Perisphere_Lower_Removable_Shell','Helicline_Bridge_Transition_Hypothesis'}

def sphere_screen(mesh,centers,radius):
    """Triangle-surface distance to spheres. Does not detect solid containment."""
    best=np.full(len(centers),np.inf)
    # Bound memory and retain transformed node attribution.
    for start in range(0,len(centers),32):
        _,dist,_=trimesh.proximity.closest_point_naive(mesh,centers[start:start+32])
        best[start:start+32]=dist
    return best-radius

def audit(source,overlay,route="transition",*,expected_overlay_sha=OVERLAY_SHA,extra_hidden=()):
    if route not in ("transition","return"):raise ValueError("Unknown route")
    source,overlay=Path(source),Path(overlay)
    hidden=HIDDEN|set(extra_hidden)
    if hashlib.sha256(source.read_bytes()).hexdigest()!=SOURCE_SHA:raise ValueError('Unknown source')
    if hashlib.sha256(overlay.read_bytes()).hexdigest()!=expected_overlay_sha:raise ValueError('Unknown overlay')
    scenes=[('source',trimesh.load(source,force='scene')),('overlay',trimesh.load(overlay,force='scene'))]
    transition=world_mesh(scenes[1][1],'PROVISIONAL_Helicline_Surface_Transition_r3')
    start=np.array([-32.71935121424215,15.849599838256836,-9.050683803084627])
    end=np.array([-32.28064878575785,15.849599838256836,-9.949316196915373])
    direction=end-start;across=np.array([-direction[2],0,direction[0]])
    radius=.3;height=1.8;floor_lift=.05;axis_step=.1
    # Inflated spheres conservatively cover the continuous vertical capsule axis
    # at each sampled pose. They do NOT cover motion between poses.
    cover_radius=float(np.sqrt(radius**2+(axis_step/2)**2))
    centers=[];poses=[];owners=[]
    for along in np.linspace(.01,.99,21):
        for offset in (-.6,0,.6):
            p=start+along*direction+offset*across
            hit=vertical_surface(transition,p[[0,2]],start[1])
            if hit is None:raise ValueError('Missing route surface')
            p[1]=hit['surface_y_m']+floor_lift
            index=len(poses);poses.append({'foot_xyz_m':p.tolist(),'along_m':float(along),'lateral_m':offset})
            for y in np.linspace(radius,height-radius,13):
                centers.append(p+[0,y,0]);owners.append(index)
    if route=="return":
        centers=[];poses=[];owners=[]
        floor=float(world_mesh(scenes[0][1],'Return_Bridge_Deck').bounds[1,1])
        deck_z=float(world_mesh(scenes[0][1],'Return_Bridge_Deck').bounds[:,2].mean())
        inside_x=float(world_mesh(scenes[0][1],'Trylon_Hollow_Exterior').bounds[:,0].mean())
        points=[[-35.9,floor,deck_z],[inside_x,floor,deck_z],
                [inside_x,floor,-3.15],[-35.6,floor,-3.15],start.tolist()]
        for segment,(a,b) in enumerate(zip(points,points[1:]),1):
            a,b=np.array(a),np.array(b);vector=b-a;length=float(np.linalg.norm(vector))
            direction=vector/length;across=np.array([-direction[2],0,direction[0]])
            slab=world_mesh(scenes[1][1],f'PROVISIONAL_ReturnViaTrylon_{segment:02d}')
            for t in np.linspace(.00001,.99999,int(np.ceil(length/.25))+1):
                for offset in (-.6,0,.6):
                    p=a+t*vector+offset*across
                    hit=vertical_surface(slab,p[[0,2]],floor)
                    if hit is None:raise ValueError('Missing return slab support')
                    p[1]=hit['surface_y_m']+floor_lift
                    index=len(poses);poses.append({'foot_xyz_m':p.tolist(),'segment':segment,
                        'along_m':float(t*length),'lateral_m':offset})
                    for y in np.linspace(radius,height-radius,13):
                        centers.append(p+[0,y,0]);owners.append(index)
    centers=np.array(centers)
    lo=centers.min(axis=0)-cover_radius;hi=centers.max(axis=0)+cover_radius
    checked=[];findings=[]
    for origin,scene in scenes:
        for node in sorted(scene.graph.nodes_geometry):
            if origin=='source' and node in hidden:continue
            m=world_mesh(scene,node)
            if np.any(m.bounds[1]<lo) or np.any(m.bounds[0]>hi):continue
            tri=m.triangles
            mask=np.all(tri.max(axis=1)>=lo,axis=1)&np.all(tri.min(axis=1)<=hi,axis=1)
            if not mask.any():continue
            local=trimesh.Trimesh(vertices=m.vertices,faces=m.faces[mask],process=False)
            clearance=sphere_screen(local,centers,cover_radius)
            checked.append({'origin':origin,'node':node,'triangles_screened':int(mask.sum()),'minimum_surface_clearance_m':float(clearance.min())})
            indices=np.flatnonzero(clearance<0)
            if len(indices):
                worst=int(np.argmin(clearance))
                findings.append({'origin':origin,'node':node,'affected_pose_indices':sorted(set(owners[i] for i in indices)),
                  'worst_pose_index':owners[worst],'sphere_center_m':centers[worst].tolist(),
                  'minimum_surface_clearance_m':float(clearance[worst])})
    return {'schema':'fmp.transition-clearance.v1','source_sha256':SOURCE_SHA,'overlay_sha256':expected_overlay_sha,
      'body_assumption':{'radius_m':radius,'height_m':height,'floor_lift_m':floor_lift,'axis_cover_radius_m':cover_radius,
      'note':'Provisional test body, not a configured Unreal character or accessibility standard'},
      'route':route,'pose_count':len(poses),'poses':poses,'checked_nodes':checked,'findings':findings,
      'hidden_source_nodes':sorted(hidden),'status':'BLOCKERS_FOUND' if findings else 'NO_SAMPLED_SURFACE_CONTACTS',
      'acceptance':'OPEN_NATIVE_COLLISION_AND_CONTINUOUS_SWEEP',
      'limits':['Discrete poses on selected route only; no continuous motion or corner-turn coverage',
       'Surface screen does not detect a capsule entirely inside a closed solid',
       'Inflated axis-cover spheres may conservatively flag near contacts',
       'Source nodes treated as obstacles regardless of future Unreal collision settings',
       'No geometry altered; no Unreal tests performed']}

if __name__=='__main__':
    if len(sys.argv) not in (4,5):raise SystemExit('usage: audit_transition_clearance.py SOURCE OVERLAY REPORT [transition|return]')
    r=audit(sys.argv[1],sys.argv[2],sys.argv[4] if len(sys.argv)==5 else "transition");Path(sys.argv[3]).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('poses','checked_nodes')},indent=2))
