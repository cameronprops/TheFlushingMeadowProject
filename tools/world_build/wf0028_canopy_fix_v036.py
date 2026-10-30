"""WF0028 v036 canopy geometry correction; all dimensions interpretive."""
import math
import numpy as np
import trimesh
from pathlib import Path
BASE=Path(__file__).parent
scene=trimesh.load(BASE/"wf0028_hippocrates_entrance_reference_v035.glb",file_type="glb",force="scene")
original=set(scene.graph.nodes_geometry)
assert len(original)==38 and "CANOPY" in original
scene.delete_geometry("CANOPY")
W=18.; bow=1.1; R=W*W/(8*bow)+bow/2
wall=lambda x:R-bow-math.sqrt(max(0.,R*R-x*x))
front=wall(0)-1.5
back_offset=.20
z0,z1=3.9-.11,3.9+.11
def prism(a,b):
    points=[(a,front),(b,front),(b,wall(b)+back_offset),(a,wall(a)+back_offset)]
    verts=np.array([(x,y,z) for z in (z0,z1) for x,y in points])
    faces=[]
    for i in range(4):
        j=(i+1)%4
        faces += [(i,j,4+j),(i,4+j,4+i)]
    faces += [(0,2,1),(0,3,2),(4,5,6),(4,6,7)]
    m=trimesh.Trimesh(vertices=verts,faces=faces,process=True)
    trimesh.repair.fix_normals(m)
    assert m.is_watertight and m.volume>0
    return m
xs=np.linspace(-4,4,33)
for i,(a,b) in enumerate(zip(xs[:-1],xs[1:])):
    name=f"CANOPY_CURVED_BACK_SEGMENT_{i:02d}"
    scene.add_geometry(prism(a,b),node_name=name,geom_name=name)
assert len(scene.graph.nodes_geometry)==69
assert original-{"CANOPY"} <= set(scene.graph.nodes_geometry)
assert .20-.27/2>=.06
outfile=BASE/"WF0028_Hippocrates_Canopy_Connection_v036.glb"
outfile.write_bytes(scene.export(file_type="glb"))
assert len(trimesh.load(outfile,file_type="glb",force="scene").graph.nodes_geometry)==69
print("v036 PASS: 69 geometry nodes; interface nominal overlap 0.065 m")
