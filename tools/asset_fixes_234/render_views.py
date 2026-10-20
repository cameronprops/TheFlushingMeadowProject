"""Deterministic raster views of existing mesh geometry, no generated imagery."""
import os
os.environ['PYOPENGL_PLATFORM']='egl'
import numpy as np,trimesh,pyrender
np.infty=np.inf
from PIL import Image,ImageDraw
from pathlib import Path
OUT=Path(__file__).parent/'output'
SRC=Path(__file__).parent/'inputs/ThemeCenter_v005.glb'
def camera(eye,target):
 z=np.asarray(eye)-target;z=z/np.linalg.norm(z);x=np.cross([0,1,0],z);x=x/np.linalg.norm(x);y=np.cross(z,x)
 p=np.eye(4);p[:3,:3]=np.stack([x,y,z],axis=1);p[:3,3]=eye;return p

def render(path,name,eye,target,cut=False,scenic=False):
 s=trimesh.load(path,force='scene',process=False);r=pyrender.Scene(bg_color=[.07,.09,.12,1],ambient_light=[.4,.4,.4])
 for n in s.graph.nodes_geometry:
  t,g=s.graph[n];m=s.geometry[g].copy();m.apply_transform(t)
  if scenic:
   if not any(k in n for k in ['03 /','04 /','05 /','06 /','07 /']):continue
  else:
   if not any(k in n for k in ['Trylon','Helicline','Return_Bridge','ReturnVia','Surface_Transition']):continue
   if cut and 'Hollow_Exterior' in n:continue
   # Local architectural crop; faces outside the review box are omitted.
   for axis,lo,hi in [(0,-45,-20),(1,13,24),(2,-12,12)]:
    normal=np.zeros(3);normal[axis]=1;origin=np.zeros(3);origin[axis]=lo
    m=m.slice_plane(origin,normal,cap=False)
    origin[axis]=hi;m=m.slice_plane(origin,-normal,cap=False)
   if not len(m.faces):continue
  col=[.73,.76,.8,1]
  if 'RUNTIME_SHARED' in n:col=[1,.57,.18,1]
  if 'ReturnVia' in n or 'Surface_Transition' in n:col=[.1,.7,.85,1]
  mat=pyrender.MetallicRoughnessMaterial(baseColorFactor=col,metallicFactor=0,roughnessFactor=.8,doubleSided=False)
  r.add(pyrender.Mesh.from_trimesh(m,material=mat,smooth=False))
 if scenic:
  bounds=r.bounds;target=bounds.mean(axis=0);span=np.max(bounds[1]-bounds[0]);eye=target+np.array([.3,.9,1.2])*span
 pose=camera(np.array(eye),np.array(target));r.add(pyrender.PerspectiveCamera(yfov=np.radians(55),znear=.05,zfar=1000),pose=pose)
 r.add(pyrender.DirectionalLight(color=np.ones(3),intensity=3),pose=pose)
 ren=pyrender.OffscreenRenderer(1400,1000);im,depth=ren.render(r);ren.delete()
 image=Image.fromarray(im);d=ImageDraw.Draw(image);d.rectangle((0,0,1400,85),fill=(15,20,28));d.text((24,16),name,fill='white',font_size=27)
 d.text((24,52),'ACTUAL MESH | orange: runtime replacements | cyan: provisional path | grey: retained geometry',fill='white',font_size=18)
 d.rectangle((0,955,1400,1000),fill=(15,20,28));d.text((24,967),'Local crop. '+('Trylon exterior shell hidden for cutaway. ' if cut else '')+'Provisional architecture; not Unreal or historical certification.',fill='white',font_size=17)
 image.save(OUT/(name+'.png'))
 print(name, 'visible pixels',int((depth>0).sum()))
render(SRC,'01_Trylon_entry',[-28,18,7],[-36.7,17,3])
render(SRC,'02_Trylon_frame_cutaway',[-47,23,9],[-36.7,16.8,0],True)
render(SRC,'03_Helicline_exit',[-29,18,-8],[-36.7,17,-3.15])
render(SRC,'04_Scenic_before',[0,58,100],[0,0,0],scenic=True)
render(OUT/'ThemeCenter_WindingRepair_v006.glb','05_Scenic_after',[0,58,100],[0,0,0],scenic=True)
