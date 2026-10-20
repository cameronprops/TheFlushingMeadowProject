import numpy as np,trimesh,json,hashlib,sys
from pathlib import Path
from tools.world_build.audit_helicline_join import world_mesh
from tools.world_build.audit_transition_clearance import sphere_screen,HIDDEN
if len(sys.argv)!=3:raise SystemExit('usage: python -m tools.world_build.scan_trylon_opening SOURCE.glb REPORT.json')
source=Path(sys.argv[1])
assert hashlib.sha256(source.read_bytes()).hexdigest()=='a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5', 'Unknown source'
s=trimesh.load(source,force='scene');meshes=[]
lo=np.array([-39,14,-6]);hi=np.array([-34,24,6])
for node in s.graph.nodes_geometry:
 if node in HIDDEN:continue
 m=world_mesh(s,node)
 if np.any(m.bounds[1]<lo) or np.any(m.bounds[0]>hi):continue
 tri=m.triangles;mask=np.all(tri.max(axis=1)>=lo,axis=1)&np.all(tri.min(axis=1)<=hi,axis=1)
 if mask.any():meshes.append((node,trimesh.Trimesh(vertices=m.vertices,faces=m.faces[mask],process=False)))
results=[]
for y in np.arange(14,22.01,.5):
 for z in np.arange(-4,4.01,1):
  centers=np.array([[x,y+.05+h,z+o] for x in np.linspace(-38,-35,13) for o in [-.6,0,.6] for h in np.linspace(.3,1.5,13)])
  hits=[]
  for n,m in meshes:
   if m.bounds[1,1]<y+.04 or m.bounds[0,1]>y+1.86:continue
   d=float(sphere_screen(m,centers,.30413812651491096).min())
   if d<0:hits.append({'node':n,'clearance_m':d})
  results.append({'floor_y_m':float(y),'center_z_m':float(z),'blockers':hits})
  if not hits:print('CLEAR',y,z,flush=True)
json.dump({'body_radius_m':.3,'body_height_m':1.8,'crossing_x_range_m':[-38,-35],'candidates':results,'limitations':'Discrete straight crossings only; not exhaustive path search or historical proof'},open(sys.argv[2],'w'),indent=2)
print('candidates',len(results),'clear',sum(not r['blockers'] for r in results))
