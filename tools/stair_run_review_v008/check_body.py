"""Discrete body/head surface screen. Stair contacts stay explicit."""
import json,hashlib,argparse
from pathlib import Path
import numpy as np,trimesh
HASH='aefc8b0a83c5e8264b936151a13cb5f7190e69d9e55c28a5141ce84c0fced867'
def inspect(path):
 if hashlib.sha256(path.read_bytes()).hexdigest()!=HASH:raise ValueError('Wrong v008 asset')
 s=trimesh.load(path,force='scene',process=False);world={}
 for n in s.graph.nodes_geometry:
  T,g=s.graph[n];m=s.geometry[g].copy();m.apply_transform(T);world[n]=m
 treads=[world['PROVISIONAL_UpperReturnStair_%02d'%i] for i in range(1,24)]
 c=np.array([m.bounds.mean(0) for m in treads]);c[:,1]=[m.bounds[1,1] for m in treads]
 direction=c[-1]-c[0];direction[1]=0;direction/=np.linalg.norm(direction);across=np.array([-direction[2],0,direction[0]])
 poses=[]
 for i,p in enumerate(c):
  for lateral in [-.4,0,.4]:poses.append(('tread_%02d'%(i+1),p+across*lateral))
 start=np.array([-27.18689141765125,19.507200241088867,-3.0479999780654907]);finish=np.array([-30.25,15.849599838256835,3.048000082373619])
 for label,a,b in [('upper_turn',np.array([-25.1,start[1],start[2]]),start),('lower_turn',finish,np.array([-33.5,finish[1],finish[2]]))]:
  for t in np.linspace(0,1,17):poses.append((label,a*(1-t)+b*t))
 feet=np.array([p for _,p in poses]);heights=np.linspace(.35,1.55,13);points=(feet[:,None,:]+np.array([0,1,0])[None,None,:]*heights[None,:,None]).reshape(-1,3)
 radius=float(np.sqrt(.3**2+.05**2));contacts=[];nearest_head=None
 walking={'PROVISIONAL_UpperLandingToStair','Return_Bridge_Deck','PERISPHERE_UPPER_FLUSH_THRESHOLD'}|{'PROVISIONAL_UpperReturnStair_%02d'%i for i in range(1,24)}
 for n,m in world.items():
  if np.any(m.bounds[1]<points.min(0)-radius) or np.any(m.bounds[0]>points.max(0)+radius):continue
  _,dist,_=trimesh.proximity.closest_point(m,points)
  hit=np.flatnonzero(dist<radius-1e-5)
  for k in hit:
   pose=k//13;level=k%13
   contacts.append({'node':n,'pose':int(pose),'zone':poses[pose][0],'height_above_tread_m':float(heights[level]),'surface_distance_m':float(dist[k]),'walking_surface':n in walking})
  head=dist.reshape(-1,13)[:,-1].min()-radius
  if nearest_head is None or head<nearest_head['margin_m']:nearest_head={'node':n,'margin_m':float(head)}
 return {'asset_sha256':HASH,'poses':len(poses),'spheres':len(points),'body_diameter_m':.6,'nominal_height_m':1.8,'floor_lift_m':.05,'cover_sphere_radius_m':radius,'pose_list':[{'zone':n,'foot':p.tolist()} for n,p in poses],'contacts':contacts,'nonwalking_contacts':sum(not x['walking_surface'] for x in contacts),'walking_contacts':sum(x['walking_surface'] for x in contacts),'nearest_head_surface':nearest_head,'scope':'Discrete surface-only capsule cover at tread centres and straight landing-turn segments. Stair/riser contacts retained. No continuous movement, containment, historical or native Unreal acceptance.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('asset',type=Path);p.add_argument('output',type=Path);a=p.parse_args();r=inspect(a.asset);a.output.write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['contacts','pose_list']});print(sorted({x['node'] for x in r['contacts'] if not x['walking_surface']}))
