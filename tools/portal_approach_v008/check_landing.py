import json,hashlib
from pathlib import Path
import numpy as np,trimesh

START=np.array([-27.18689141765125,19.507200241088867,-3.0479999780654907])
FINISH=np.array([-30.25,15.849599838256835,3.048000082373619])
DIRECTION=FINISH-START;DIRECTION[1]=0;DIRECTION/=np.linalg.norm(DIRECTION)
ACROSS=np.array([-DIRECTION[2],0,DIRECTION[0]])

def inspect(path, distance=-.10, height_drop=0):
 s=trimesh.load(path,force='scene',process=False);meshes=[]
 points=np.array([START+ACROSS*t+DIRECTION*distance-[0,height_drop,0] for t in np.linspace(-.875,.875,15)])
 for n in s.graph.nodes_geometry:
  T,g=s.graph[n];m=s.geometry[g].copy();m.apply_transform(T)
  if np.any(m.bounds[1]<points.min(0)-[.2,.4,.2]) or np.any(m.bounds[0]>points.max(0)+[.2,.1,.2]):continue
  meshes.append(m)
 combined=trimesh.util.concatenate(meshes)
 origins=points+[0,.05,0];directions=np.tile([0,-1,0],(len(points),1))
 loc,ray,tri=combined.ray.intersects_location(origins,directions,multiple_hits=True)
 result=[]
 for i,p in enumerate(points):
  hits=loc[ray==i,1];hits=hits[hits<=p[1]+.01]
  top=float(hits.max()) if len(hits) else None
  drop=float(p[1]-top) if top is not None else None
  result.append({'point':p.tolist(),'surface_y':top,'drop_m':drop,'level_landing_support':drop is not None and abs(drop)<.002})
 return {'asset_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'distance_from_stair_start_m':distance,'height_drop_m':height_drop,'probe_count':len(points),'supported':sum(p['level_landing_support'] for p in result),'samples':result,'scope':'15 vertical point rays at declared longitudinal offset and height drop; excludes outermost 50 mm of stair width; level support only, not body collision or Unreal traversal'}

if __name__=='__main__':
 import sys
 report=inspect(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(report,indent=2)+'\n');print(report['supported'],'/',report['probe_count'])
