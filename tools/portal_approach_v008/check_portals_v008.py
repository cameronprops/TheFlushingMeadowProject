import json,hashlib
from pathlib import Path
import numpy as np,trimesh
from glb_tools import read_glb
from validation_gate import require_clear, sha256
R=Path(__file__).parent.parent/'portal_build'
r=json.loads((R/'output/portal_manifest.json').read_text());path=Path(__file__).parent/'ThemeCenter_UpperLanding_v008.glb'
s=trimesh.load(path,force='scene',process=False)
d,b=read_glb(path);old,ob=read_glb(R/'inputs/ThemeCenter_v006.glb')
assert bytes(b[:len(ob)])==bytes(ob)
assert d['meshes'][:len(old['meshes'])]==old['meshes']
assert d['materials'][:len(old['materials'])]==old['materials']
for before,after in zip(old['nodes'],d['nodes']):
 for k in ['name','matrix','translation','rotation','scale','children']:assert before.get(k)==after.get(k)
 if before.get('name') not in r['disabled']+r['replaced']:assert before==after
world={}
for n in s.graph.nodes_geometry:
 T,g=s.graph[n];m=s.geometry[g].copy();m.apply_transform(T);world[n]=m
for p in r['parts']:
 name=p.get('replacement_node') or p['name']
 m=world[name];assert m.is_watertight and m.is_winding_consistent,name
assert all(c['all_inside_jamb_x_depth'] for c in r['brace_cap_contacts'])
checks=[]
for p in r['portals']:
 y,z=p['floor_y'],p['center_z'];xlo,xhi=p['x_range'];points=[]
 for x in np.linspace(xlo-.12,xhi+.12,17):
  for dz in [-.5,0,.5]:
   for h in np.linspace(.35,1.55,13):points.append([x,y+h,z+dz])
 pts=np.array(points);radius=np.sqrt(.3**2+.05**2)
 hits=[];near=[]
 for n,m in world.items():
  if np.any(m.bounds[1]<pts.min(0)-radius) or np.any(m.bounds[0]>pts.max(0)+radius):continue
  _,dist,_=trimesh.proximity.closest_point(m,pts)
  idx=np.where(dist<radius-1e-5)[0]
  if len(idx):hits.append({'node':n,'samples':len(idx),'min_surface_distance':float(dist.min()),'worst_center':pts[int(dist.argmin())].tolist()})
  near.append(n)
 checks.append({'portal':p['id'],'poses':51,'sphere_samples':len(pts),'body_diameter':.6,'height':1.8,'floor_lift':.05,'surface_contacts':hits})
out={'asset_sha256':sha256(path),'preservation':'PASS','added_solids':'PASS','brace_jamb_connections':'PASS','screens':checks,'scope':'Discrete sphere cover body surface screen; not continuous Unreal traversal or structural certification'}
(Path(__file__).parent/'portal_validation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

require_clear(out, path, [p['id'] for p in r['portals']])
