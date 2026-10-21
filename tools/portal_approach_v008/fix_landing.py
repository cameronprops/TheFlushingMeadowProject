"""Fit the provisional upper landing to existing stair and rail geometry."""
from pathlib import Path
import hashlib,json,copy
import numpy as np,trimesh
from glb_tools import read_glb,write_glb,append
from check_landing import START,DIRECTION,ACROSS
R=Path(__file__).parent
SOURCE=R.parent/'portal_build/output/ThemeCenter_Framed_Portals_v007.glb'
TARGET=R/'ThemeCenter_UpperLanding_v008.glb'

def build():
 if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!='ef1d417434ec9b1a873a0aecd9a287d96c353bcef9c70f7a70fb1b22af8c0633':raise ValueError('Wrong input')
 s=trimesh.load(SOURCE,force='scene',process=False)
 def world(n):
  T,g=s.graph[n];m=s.geometry[g].copy();m.apply_transform(T);return m
 name='PROVISIONAL_UpperLandingToStair';old=world(name);y=old.bounds[1,1]
 points=[old.vertices[:,[0,2]]]
 for side in ['L','R']:points.append(world('PERISPHERE_UPPER_LANDING_RAIL_'+side).vertices[:,[0,2]])
 points.append(np.array([(START+ACROSS*t)[[0,2]] for t in [-1.025,1.025]]))
 xz=np.concatenate(points);vertices=np.concatenate([np.column_stack([xz[:,0],np.full(len(xz),h),xz[:,1]]) for h in [y-.16,y]])
 slab=trimesh.convex.convex_hull(vertices)
 # A stair-width notch makes a straight landing nosing across the entire first tread.
 cutter=trimesh.creation.box(extents=[10,1,1.85]);cutter.apply_transform(trimesh.geometry.align_vectors([1,0,0],DIRECTION));cutter.apply_translation(START+DIRECTION*5)
 slab=trimesh.boolean.difference([slab,cutter],engine='manifold')
 if not slab.is_watertight or not slab.is_winding_consistent:raise ValueError('Landing solid invalid')
 d,b=read_glb(SOURCE);source_nodes=copy.deepcopy(d['nodes']);prefix=bytes(b)
 node=next(n for n in d['nodes'] if n.get('name')==name)
 primitive=copy.deepcopy(d['meshes'][node['mesh']]['primitives'][0])
 v=np.asarray(slab.vertices,dtype='<f4');vi=append(d,b,v,'VEC3',5126);d['accessors'][vi].update(min=v.min(0).tolist(),max=v.max(0).tolist())
 ni=append(d,b,np.asarray(slab.vertex_normals,dtype='<f4'),'VEC3',5126)
 fi=append(d,b,np.asarray(slab.faces,dtype='<u4').reshape(-1,1),'SCALAR',5125)
 primitive.update(attributes={'POSITION':vi,'NORMAL':ni},indices=fi)
 node['mesh']=len(d['meshes']);node.setdefault('extras',{})['landing_v008']='PROVISIONAL_DIAGONAL_STAIR_JUNCTION'
 d['meshes'].append({'name':'PERISPHERE_UPPER_LANDING_FULL_STAIR_WIDTH_v008','primitives':[primitive]})
 write_glb(TARGET,d,b)
 report={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(TARGET.read_bytes()).hexdigest(),'replaced_node':name,'source_binary_prefix_preserved':bytes(b[:len(prefix)])==prefix,'other_nodes_unchanged':all(a==c for a,c in zip(source_nodes,d['nodes']) if a.get('name')!=name),'watertight':bool(slab.is_watertight),'winding_consistent':bool(slab.is_winding_consistent),'before_bounds':old.bounds.tolist(),'after_bounds':slab.bounds.tolist(),'classification':'PROVISIONAL_RUNTIME_REPAIR','limits':['No historical architecture claim','No structural analysis','No native Unreal traversal']}
 (R/'repair_manifest.json').write_text(json.dumps(report,indent=2)+'\n')
 print(report)
if __name__=='__main__':build()
