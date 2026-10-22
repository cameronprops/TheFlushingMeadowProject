"""Read-only sampled support inspection of v008 stair treads and bridge junction."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np,trimesh
EXPECTED='aefc8b0a83c5e8264b936151a13cb5f7190e69d9e55c28a5141ce84c0fced867'

def inspect(path):
 digest=hashlib.sha256(path.read_bytes()).hexdigest()
 if digest!=EXPECTED:raise ValueError('Expected exact v008 scene')
 s=trimesh.load(path,force='scene',process=False);world={}
 for n in s.graph.nodes_geometry:
  T,g=s.graph[n];m=s.geometry[g].copy();m.apply_transform(T);world[n]=m
 treads=[world['PROVISIONAL_UpperReturnStair_%02d'%i] for i in range(1,24)]
 centers=np.array([m.bounds.mean(0) for m in treads]);direction=centers[-1]-centers[0];direction[1]=0;direction/=np.linalg.norm(direction)
 across=np.array([-direction[2],0,direction[0]])
 centers[:,1]=[m.bounds[1,1] for m in treads]
 going=float(np.dot(centers[1]-centers[0],direction));samples=[]
 for i,c in enumerate(centers):
  for lateral in np.linspace(-.75,.75,5):
   for longitudinal in [-.10,0,.10]:samples.append(('tread_%02d'%(i+1),c+across*lateral+direction*longitudinal))
 end=centers[-1]+direction*going/2
 for distance in [.10,.50]:
  for lateral in np.linspace(-.875,.875,15):samples.append(('bridge_after_%.2fm'%distance,end+direction*distance+across*lateral))
 pts=np.array([p for _,p in samples]);meshes=[];names=[]
 for name,m in world.items():
  if np.any(m.bounds[1]<pts.min(0)-[.1,.3,.1]) or np.any(m.bounds[0]>pts.max(0)+[.1,.05,.1]):continue
  meshes.append(m);names.extend([name]*len(m.faces))
 mesh=trimesh.util.concatenate(meshes);origins=pts+[0,.05,0]
 loc,ray,tri=mesh.ray.intersects_location(origins,np.tile([0,-1,0],(len(pts),1)),multiple_hits=True)
 rows=[]
 for i,(label,p) in enumerate(samples):
  indices=np.flatnonzero(ray==i)
  if len(indices):
   k=indices[np.argmax(loc[indices,1])];level=float(loc[k,1]);node=names[tri[k]];error=level-float(p[1])
  else:level=node=error=None
  rows.append({'zone':label,'point':p.tolist(),'surface_y':level,'surface_node':node,'error_m':error,'pass':error is not None and abs(error)<.002})
 return {'asset_sha256':digest,'tread_count':23,'going_m':going,'rises_m':(-np.diff(centers[:,1])).tolist(),'sample_count':len(rows),'supported_count':sum(x['pass'] for x in rows),'max_abs_error_m':max(abs(x['error_m']) for x in rows if x['error_m'] is not None),'samples':rows,'scope':'Discrete vertical surface rays; 15 points per tread and 30 beyond bottom junction. No swept body, headroom, step-controller, structural or historical acceptance.'}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('asset',type=Path);a.add_argument('report',type=Path);args=a.parse_args()
 report=inspect(args.asset);args.report.write_text(json.dumps(report,indent=2)+'\n')
 print({k:v for k,v in report.items() if k not in ['samples','rises_m']})
 for row in report['samples']:
  if not row['pass']:print(row)
 raise SystemExit(0 if report['supported_count']==report['sample_count'] else 1)
