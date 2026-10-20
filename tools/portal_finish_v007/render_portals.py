import os
os.environ['PYOPENGL_PLATFORM']='egl'
import numpy as np
np.infty=np.inf
import trimesh,pyrender
from PIL import Image,ImageDraw
from pathlib import Path
R=Path(__file__).parent;S=trimesh.load(R/'output/ThemeCenter_Framed_Portals_v007.glb',force='scene',process=False)
def render(name,eye,target,region):
 scene=pyrender.Scene(bg_color=[.075,.09,.11,1],ambient_light=[.4,.4,.4])
 for n in S.graph.nodes_geometry:
  T,g=S.graph[n];m=S.geometry[g].copy();m.apply_transform(T)
  lo,hi=region
  if np.any(m.bounds[1]<lo) or np.any(m.bounds[0]>hi):continue
  for axis in range(3):
   v=np.zeros(3);v[axis]=1;o=np.zeros(3);o[axis]=lo[axis];m=m.slice_plane(o,v,cap=False)
   o[axis]=hi[axis];m=m.slice_plane(o,-v,cap=False)
  if not len(m.faces):continue
  color=[.72,.74,.75,1]
  if any(k in n for k in ['JAMB_REVEAL','HEADER_REVEAL']):color=[.24,.30,.32,1]
  elif 'FACE_TRIM' in n:color=[.62,.64,.61,1]
  elif 'INFILL_WALL' in n or 'Shell__UNREAL' in n or 'Hollow_Exterior' in n:color=[.88,.86,.78,1]
  elif 'RETURN' in n and 'RAIL' in n:color=[.3,.38,.4,1]
  elif 'ReturnVia' in n or 'THRESHOLD' in n:color=[.42,.52,.54,1]
  mat=pyrender.MetallicRoughnessMaterial(baseColorFactor=color,roughnessFactor=.8,doubleSided=False)
  scene.add(pyrender.Mesh.from_trimesh(m,material=mat,smooth=False))
 eye=np.array(eye);target=np.array(target);z=eye-target;z=z/np.linalg.norm(z);x=np.cross([0,1,0],z);x/=np.linalg.norm(x);y=np.cross(z,x)
 pose=np.eye(4);pose[:3,:3]=np.stack([x,y,z],axis=1);pose[:3,3]=eye
 scene.add(pyrender.PerspectiveCamera(yfov=np.radians(52),znear=.05,zfar=200),pose=pose)
 scene.add(pyrender.DirectionalLight(color=np.ones(3),intensity=2.8),pose=pose)
 ren=pyrender.OffscreenRenderer(1400,1000);c,d=ren.render(scene);ren.delete()
 im=Image.fromarray(c);draw=ImageDraw.Draw(im);draw.rectangle((0,0,1400,78),fill=(17,22,28));draw.text((24,15),name,fill='white',font_size=27)
 draw.text((24,49),'Actual v007 mesh render | new wall, jambs, headers and returns | provisional architecture',fill='white',font_size=18)
 draw.rectangle((0,960,1400,1000),fill=(17,22,28));draw.text((24,970),'Local section crop. No AI imagery. Historical detailing and Unreal traversal remain unverified.',fill='white',font_size=17)
 dest=R/('output/'+name+'.png');temp=dest.with_suffix('.tmp.png');im.save(temp);Image.open(temp).verify();temp.replace(dest)
 print(name)
if __name__=='__main__':
 render('Trylon_framed_passages',[-28,19,8],[-36.7,17.5,0],(np.array([-43,14,-7]),np.array([-24,24,8])))
 render('Trylon_rail_return',[-32,17.5,-7],[-36.6,16.8,-3.15],(np.array([-39,15,-6]),np.array([-29,20,0])))
 render('Perisphere_lower_portal',[-29,18.5,8],[-22.3,17,3.048],(np.array([-31,14,0]),np.array([-17,21,7])))
 render('Perisphere_upper_portal',[-31,22,-8],[-24.4,20.7,-3.048],(np.array([-33,18,-7]),np.array([-19,24,0])))
