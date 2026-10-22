import numpy as np,trimesh
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
root=Path('/mnt/data/trylon_arch_render')
s=trimesh.load(root/'FMP_ThemeCenter_Assembled_Runtime_v005.glb',force='scene')
try:
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
 bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',23)
 small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
except: font=bold=small=ImageFont.load_default()
W,H=1230,920
zmin,zmax=-13,13; ymin,ymax=9,25
padding_l,padding_t=84,110
scale=min((W-160)/(zmax-zmin),(H-230)/(ymax-ymin))
# y elevation spans ~16m, z ~26m: x image 1070 wide and Y 658 high.
def screen(p):
 return (W/2+(float(p[2]))*scale, H-118-(float(p[1])-ymin)*scale)

def face_list(name,color):
 t,g=s.graph[name];m=s.geometry[g if g else name].copy();m.apply_transform(t)
 faces=[]
 normals=m.face_normals
 for tri,n in zip(m.triangles,normals):
  ymin2,ymax2=tri[:,1].min(),tri[:,1].max()
  if ymax2<ymin or ymin2>ymax:continue
  if all(abs(p[2])>zmax and p[2]*tri[0,2]>0 for p in tri):continue
  if abs(np.cross(tri[1]-tri[0],tri[2]-tri[0])[0])<1e-10:continue
  # no true plane cut needed in image, Pillow clips outside figure naturally
  view=max(0,float(n[0]))
  brightness=0.55 + 0.38*view
  rgba=tuple(int(min(255,max(0,c*brightness))) for c in color)
  faces.append((float(tri[:,0].mean()),[screen(p) for p in tri],rgba))
 return faces

def draw(mode):
 im=Image.new('RGB',(W,H),'#f8fafb');d=ImageDraw.Draw(im)
 d.rectangle((0,0,W,90),fill='#1a3342')
 d.text((42,28),'TRYLON  •  FRONT ELEVATION FROM ACTUAL V005 GLB',font=bold,fill='white')
 d.text((W-340,38),'MODEL-LOCAL  |  NOT HISTORICALLY CERTIFIED',font=small,fill='#b5cbd8')
 for y in [10,12,14,16,18,20,22,24]:
  py=screen([0,y,0])[1];d.line((78,py,W-70,py),fill='#e4e9ed',width=1)
  d.text((20,py-10),f'{y} m',font=small,fill='#647784')
 for z in range(-12,13,2):
  px=screen([0,16,z])[0];d.line((px,100,px,H-100),fill='#edf0f1',width=1)
  d.text((px-20,H-94),f'{z:+d}',font=small,fill='#738795')
 faces=[]
 faces+=face_list('Trylon_Hollow_Exterior__RUNTIME_SHARED_APERTURES_v004',(225,222,211))
 faces+=face_list('Trylon_Face_1_Frame',(92,121,143))
 faces+=face_list('Trylon_Face_2_Frame',(92,121,143))
 faces+=face_list('Trylon_Face_3_Frame' if mode=='before' else 'Trylon_Face_3_Frame__RUNTIME_SHARED_APERTURES_v004',(46,73,91))
 for _,p,col in sorted(faces,key=lambda t:t[0]):
  d.polygon(p,fill=col)
 # Aperture envelopes are analytic overlays; never pretend this is cladding geometry
 for cz,title in [(3.048,'ENTRY'),(-3.15,'EXIT')]:
  ya,yb=17.0496-1.2,17.0496+1.2
  za,zb=cz-1.2,cz+1.2
  x0,y0=screen((0,yb,za));x1,y1=screen((0,ya,zb))
  d.rectangle((x0,y0,x1,y1),outline='#0fba85',width=4)
  d.text((x0+5,y0+8),title,font=small,fill='#067858',stroke_width=1,stroke_fill='white')
 # context
 d.text((88,800),'LIGHT STONE: existing exterior shell    DARK BLUE: modeled face framing',font=font,fill='#264354')
 d.text((88,830),'GREEN RECTANGLES: provisional clearance envelopes, NOT finished doorway construction',font=font,fill='#167b60')
 d.text((88,861),'The existing cladding is open across the central zone; framing is altered in the v004 runtime overlay.',font=small,fill='#405661')
 f=root/('07_source_frame_elevation.png' if mode=='before' else '08_current_frame_elevation.png')
 im.save(f)
 print(f)
 return im
before,after=draw('before'),draw('after')
out=Image.new('RGB',(2460,950),'white');out.paste(before,(0,0));out.paste(after,(1230,0))
d=ImageDraw.Draw(out);d.text((110,905),'SOURCE FRAME (preserved, no longer active)',font=font,fill='#973e3e');d.text((1400,905),'V004 SHARED-APERTURE FRAME (active in v005)',font=font,fill='#167b60')
out.save(root/'09_source_vs_active_frame_elevation.png')
