import vtk, numpy as np, trimesh
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
from collections import OrderedDict
ROOT=Path('/mnt/data/trylon_arch_render')
s=trimesh.load(ROOT/'FMP_ThemeCenter_Assembled_Runtime_v005.glb',force='scene')
P=(36/255,63/255,76/255); BLUE=(50/255,112/255,138/255)
COL={'shell':(0.65,0.73,0.76),'steel':(0.24,0.36,0.47),'deck':(0.89,0.59,0.25),'bridge':(0.34,0.62,0.62),'ramp':(0.63,0.52,0.35),'sphere':(0.85,0.83,0.78),'source':(0.80,0.34,0.32)}

named={
'shell':['Trylon_Hollow_Exterior__RUNTIME_SHARED_APERTURES_v004'],
'steel':['Trylon_Face_1_Frame','Trylon_Face_2_Frame','Trylon_Face_3_Frame__RUNTIME_SHARED_APERTURES_v004'],
'deck':[f'PROVISIONAL_ReturnViaTrylon_{i:02d}' for i in range(1,5)],
'bridge':['Return_Bridge_Deck'],
'ramp':['PROVISIONAL_Helicline_Surface_Transition_r3'],
'sphere':['Perisphere_Lower_Removable_Shell__UNREAL_PORTALS_v001']
}

def get_poly(name):
 t,geom=s.graph[name]
 if geom is None:
  geom=name
 m=s.geometry[geom].copy();m.apply_transform(t)
 pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(np.ascontiguousarray(m.vertices,dtype='float64'),deep=True))
 faces=vtk.vtkCellArray(); ar=np.c_[np.full(len(m.faces),3,dtype=np.int64),m.faces].ravel();faces.SetCells(len(m.faces),numpy_to_vtkIdTypeArray(ar,deep=True))
 pd=vtk.vtkPolyData();pd.SetPoints(pts);pd.SetPolys(faces)
 return pd

def actor_poly(poly,color,opacity=1,clip_top=None,clip_bottom=None,wire=False):
 if clip_top is not None:
  pl=vtk.vtkPlane();pl.SetOrigin(0,clip_top,0);pl.SetNormal(0,-1,0)
  cutter=vtk.vtkClipPolyData();cutter.SetInputData(poly);cutter.SetClipFunction(pl);cutter.InsideOutOff();cutter.Update();poly=cutter.GetOutput()
 if clip_bottom is not None:
  pl=vtk.vtkPlane();pl.SetOrigin(0,clip_bottom,0);pl.SetNormal(0,1,0)
  cutter=vtk.vtkClipPolyData();cutter.SetInputData(poly);cutter.SetClipFunction(pl);cutter.InsideOutOff();cutter.Update();poly=cutter.GetOutput()
 mp=vtk.vtkPolyDataMapper();mp.SetInputData(poly)
 act=vtk.vtkActor();act.SetMapper(mp);prop=act.GetProperty();prop.SetColor(*color);prop.SetOpacity(opacity)
 prop.SetAmbient(0.24);prop.SetDiffuse(0.68);prop.SetSpecular(0.12);prop.SetSpecularPower(15)
 if wire:prop.EdgeVisibilityOn();prop.SetEdgeColor(.25,.3,.35);prop.SetLineWidth(.5)
 return act

def add_scene(renderer,mode='after',clip_top=28,clip_bottom=None,focus=False):
 if mode=='before':
  nodes={k:v.copy() for k,v in named.items()}
  nodes['steel'][2]='Trylon_Face_3_Frame'
 else:nodes=named
 for cat,names in nodes.items():
  for name in names:
   if focus and cat=='sphere':continue
   if focus and cat=='shell': opacity=0.12
   elif cat=='shell':opacity=0.28
   elif cat=='sphere':opacity=0.50
   else:opacity=0.99 if cat in ['deck','bridge','ramp'] else .87
   renderer.AddActor(actor_poly(get_poly(name),COL[cat],opacity,clip_top,clip_bottom))

def tube(renderer,points,color=(0.10,0.78,0.71),radius=.105,opacity=1):
 pp=vtk.vtkPoints();line=vtk.vtkPolyLine();line.GetPointIds().SetNumberOfIds(len(points))
 for i,p in enumerate(points):pp.InsertNextPoint(*p);line.GetPointIds().SetId(i,i)
 cells=vtk.vtkCellArray();cells.InsertNextCell(line)
 pd=vtk.vtkPolyData();pd.SetPoints(pp);pd.SetLines(cells)
 f=vtk.vtkTubeFilter();f.SetInputData(pd);f.SetRadius(radius);f.SetNumberOfSides(10);f.CappingOn();f.Update()
 renderer.AddActor(actor_poly(f.GetOutput(),color,opacity))

def sphere(renderer,center,rad=.22,color=(0.04,.75,.57)):
 src=vtk.vtkSphereSource();src.SetCenter(*center);src.SetRadius(rad);src.SetThetaResolution(15);src.SetPhiResolution(15);src.Update()
 renderer.AddActor(actor_poly(src.GetOutput(),color,1))

def box(renderer,center,size,color=(0.13,.79,.54),opacity=.16):
 src=vtk.vtkCubeSource();src.SetCenter(*center);src.SetXLength(size[0]);src.SetYLength(size[1]);src.SetZLength(size[2]);src.Update()
 p=vtk.vtkPolyDataMapper();p.SetInputConnection(src.GetOutputPort());a=vtk.vtkActor();a.SetMapper(p)
 q=a.GetProperty();q.SetColor(*color);q.SetOpacity(opacity);q.EdgeVisibilityOn();q.SetEdgeColor(*color);q.SetLineWidth(3)
 renderer.AddActor(a)

# Walkpath centerline derived from v004 site route, approximate waypoints. Distinguish plotted route from geometry.
P0=[-35.90,15.97,3.048];P1=[-46.6683,15.97,3.048];P2=[-46.6683,15.97,-3.15];P3=[-35.60,15.97,-3.15];P4=[-32.72,15.97,-9.051]

def route(renderer):
 for a,b in zip([P0,P1,P2,P3],[P1,P2,P3,P4]):tube(renderer,[a,b],color=(.00,.88,.82),radius=.12)
 for p in [P0,P1,P2,P3,P4]:sphere(renderer,p,rad=.22)
 for z in (3.048,-3.15):
  box(renderer,(-36.7,17.0496,z),(3.4,2.4,2.4),opacity=.09)

def capture(label,mode,position,focal,up=(0,1,0),zoom=1,clip_top=29,clip_bottom=None,focus=False,route_enable=True,parallel=False,parallel_scale=17,size=(1400,920)):
 rend=vtk.vtkRenderer();rend.SetBackground(.95,.965,.97);rend.SetBackground2(.84,.90,.93);rend.GradientBackgroundOn()
 add_scene(rend,mode,clip_top=clip_top,clip_bottom=clip_bottom,focus=focus)
 if route_enable:route(rend)
 light=vtk.vtkLight();light.SetPosition(-11,55,55);light.SetFocalPoint(-40,16,0);light.SetIntensity(.8);rend.AddLight(light)
 light2=vtk.vtkLight();light2.SetPosition(-77,30,-25);light2.SetFocalPoint(-40,16,0);light2.SetIntensity(.35);rend.AddLight(light2)
 cam=rend.GetActiveCamera();cam.SetPosition(*position);cam.SetFocalPoint(*focal);cam.SetViewUp(*up);cam.ParallelProjectionOn() if parallel else cam.ParallelProjectionOff()
 if parallel:cam.SetParallelScale(parallel_scale)
 else:cam.SetViewAngle(34)
 cam.Zoom(zoom)
 w=vtk.vtkRenderWindow();w.SetOffScreenRendering(True);w.SetAlphaBitPlanes(1);w.SetMultiSamples(4);w.AddRenderer(rend);w.SetSize(*size);w.Render()
 filt=vtk.vtkWindowToImageFilter();filt.SetInput(w);filt.SetScale(1);filt.SetInputBufferTypeToRGB();filt.ReadFrontBufferOff();filt.Update()
 writer=vtk.vtkPNGWriter();writer.SetFileName(str(ROOT/(label+'.png')));writer.SetInputConnection(filt.GetOutputPort());writer.Write()
 print('SAVED',label+'.png',flush=True)

if __name__=='__main__':
 capture('01_trylon_return_exterior', 'after',(-9,28,30),(-40,17,1), zoom=1.13,clip_top=38,size=(1500,920))
 capture('02_trylon_return_section', 'after',(-29,31,27),(-40,17,-1),zoom=1.3,clip_top=22,clip_bottom=14,focus=True,size=(1500,920))
 capture('03_trylon_plan','after',(-41,63,0),(-41,17,-.7),up=(0,0,-1),clip_top=20,clip_bottom=14,parallel=True,parallel_scale=17,size=(1500,920))
 capture('04_before_frame', 'before',(-22,24,29),(-40,17,0),zoom=1.35,clip_top=23,clip_bottom=14,focus=True,size=(1500,920))
 capture('05_after_frame', 'after',(-22,24,29),(-40,17,0),zoom=1.35,clip_top=23,clip_bottom=14,focus=True,size=(1500,920))

def front(mode='after',frameOnly=False):
 rend=vtk.vtkRenderer();rend.SetBackground(.93,.95,.97)
 def mesh(name,cat,alpha=1):rend.AddActor(actor_poly(get_poly(name),COL[cat],alpha,clip_top=26,clip_bottom=7))
 if not frameOnly:
  mesh('Trylon_Hollow_Exterior__RUNTIME_SHARED_APERTURES_v004','shell',.95)
 for n in ['Trylon_Face_1_Frame','Trylon_Face_2_Frame']:
  if not frameOnly:mesh(n,'steel',.70)
 mesh('Trylon_Face_3_Frame' if mode=='before' else 'Trylon_Face_3_Frame__RUNTIME_SHARED_APERTURES_v004','steel',.98)
 if not frameOnly:
  for n in named['deck']:mesh(n,'deck',.96)
  mesh('Return_Bridge_Deck','bridge',.96)
 route(rend)
 cam=rend.GetActiveCamera();cam.SetPosition(12,20,0);cam.SetFocalPoint(-39.5,17,0);cam.SetViewUp(0,1,0);cam.ParallelProjectionOn();cam.SetParallelScale(10.5)
 light=vtk.vtkLight();light.SetPosition(20,38,35);light.SetFocalPoint(-40,17,0);light.SetIntensity(.88);rend.AddLight(light)
 w=vtk.vtkRenderWindow();w.SetOffScreenRendering(True);w.SetSize(1400,900);w.AddRenderer(rend);w.SetMultiSamples(4);w.Render()
 p=vtk.vtkWindowToImageFilter();p.SetInput(w);p.Update();wr=vtk.vtkPNGWriter();f=f'06_{mode}_'+('steel_only' if frameOnly else 'exterior')+'.png';wr.SetFileName(str(ROOT/f));wr.SetInputConnection(p.GetOutputPort());wr.Write();print('SAVED',f,flush=True)

if __name__=='__main__':
 front('before',True)
 front('after',True)
 front('after',False)
