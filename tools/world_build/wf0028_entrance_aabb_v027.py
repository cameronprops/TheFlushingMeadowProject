#!/usr/bin/env python3
"""WF0028 v027 model-space entrance AABB diagnostic, no structural edits.
Usage: python wf0028_entrance_aabb_v027.py <v026.glb> <out.json>
"""
import json,hashlib,sys
import numpy as np
import trimesh

def bounds(scene,node):
 t,g=scene.graph.get(node)
 mesh=scene.geometry[g].copy()
 mesh.apply_transform(t)
 return mesh.bounds

def analyze(file):
 s=trimesh.load(file,force="scene")
 entry=sorted(n for n in s.graph.nodes_geometry if n.startswith("V026_PROVISIONAL_ALIGNED_"))
 walls=["SCIENCE_HALL_SOUTH_WALL_L","SCIENCE_HALL_SOUTH_WALL_R","SCIENCE_HALL_ENTRY_LINTEL"]
 rows=[]
 for n in entry:
  b=bounds(s,n)
  for w in walls:
   q=bounds(s,w)
   delta=np.minimum(b[1],q[1])-np.maximum(b[0],q[0])
   rows.append({"node":n,"wall":w,"positive_aabb_overlap":bool(np.all(delta>1e-5)),
                "intersection_extent_m":[float(x) for x in np.maximum(0,delta)]})
 hit={r["node"] for r in rows if r["positive_aabb_overlap"]}
 return {"classification":"INTERPRETIVE","model_node_count":len(s.graph.nodes_geometry),
         "entrance_references":len(entry),"references_with_aabb_overlap":len(hit),
         "pairwise_aabb_candidates":sum(r["positive_aabb_overlap"] for r in rows),
         "not_a_mesh_boolean_or_historical_measurement":True,"pairs":rows}
if __name__=="__main__":
 if len(sys.argv)!=3: raise SystemExit("Usage: script input.glb output.json")
 with open(sys.argv[2],"w") as f:json.dump(analyze(sys.argv[1]),f,indent=2)
