"""Build four provisional framed portals, wall infill and rail returns on v006.
Game geometry only: no historical or structural certification. Inputs immutable.
"""
from pathlib import Path
import copy,hashlib,json,uuid
import numpy as np
import trimesh
from glb_tools import read_glb,write_glb,append
ROOT=Path(__file__).parent
OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
BASE=ROOT/'inputs/ThemeCenter_v006.glb';ORIGINAL=ROOT/'inputs/Original_staging.glb'
FLOOR=15.849599838256835

def world(s,n):
 t,g=s.graph[n];m=s.geometry[g].copy();m.apply_transform(t);return m

def box(lo,hi):
 lo,hi=np.array(lo),np.array(hi);m=trimesh.creation.box(extents=hi-lo);m.apply_translation((lo+hi)/2);return m

def tube(a,b,r=.0325):
 a,b=np.array(a),np.array(b);v=b-a;m=trimesh.creation.cylinder(radius=r,height=np.linalg.norm(v),sections=16)
 m.apply_transform(trimesh.geometry.align_vectors([0,0,1],v));m.apply_translation((a+b)/2);return m

def build():
 if hashlib.sha256(BASE.read_bytes()).hexdigest()!='b7d59c46d66f26d93873f4ccde5f6bffcc45d4c4f7b5c4a146e888de7d2d3cc9':raise ValueError('Unexpected base model')
 d,b=read_glb(BASE);original_doc=copy.deepcopy(d);old_bin=bytes(b)
 s=trimesh.load(BASE,force='scene',process=False);original=trimesh.load(ORIGINAL,force='scene',process=False)
 if hashlib.sha256(ORIGINAL.read_bytes()).hexdigest()!='a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5':raise ValueError('source hash')
 materials={}
 for key,col in [('wall',[.82,.80,.73,1]),('frame',[.32,.37,.39,1]),('reveal',[.67,.67,.62,1]),('rail',[.39,.44,.47,1]),('floor',[.52,.55,.55,1])]:
  materials[key]=len(d.setdefault('materials',[]));d['materials'].append({'name':'PROVISIONAL_PORTAL_'+key,'pbrMetallicRoughness':{'baseColorFactor':col,'metallicFactor':.25 if key in ['rail','frame'] else 0,'roughnessFactor':.72},'doubleSided':False})
 parts=[];disabled=[];replaced=[];portals=[]
 def add(name,m,mat='wall',replace=None,role='PORTAL_FINISH'):
  if not m.is_watertight or not m.is_winding_consistent:raise ValueError('Invalid solid '+name)
  mi=len(d['meshes']);v=np.asarray(m.vertices,dtype='<f4');f=np.asarray(m.faces,dtype='<u4').reshape(-1,1)
  vi=append(d,b,v,'VEC3',5126);d['accessors'][vi].update(min=v.min(0).tolist(),max=v.max(0).tolist())
  ni=append(d,b,np.asarray(m.vertex_normals,dtype='<f4'),'VEC3',5126);fi=append(d,b,f,'SCALAR',5125)
  d['meshes'].append({'name':name,'primitives':[{'attributes':{'POSITION':vi,'NORMAL':ni},'indices':fi,'material':materials[mat],'mode':4}]})
  if replace:
   n=next(n for n in d['nodes'] if n.get('name')==replace);old=n['mesh'];n['mesh']=mi
   n.setdefault('extras',{})['portal_v007_replacement']={'previous_mesh':old,'name':name,'status':'PROVISIONAL'};replaced.append(replace)
  else:
   idx=len(d['nodes']);d['nodes'].append({'name':name,'mesh':mi,'extras':{'fmp':{'object_id':str(uuid.uuid5(uuid.NAMESPACE_URL,'fmp:portal:v007:'+name)),'evidence_status':'PROVISIONAL','role':role,'year':1939,'units':'metres','engine_tested':False}}});d['scenes'][d.get('scene',0)]['nodes'].append(idx)
  parts.append({'name':name,'replacement_node':replace,'role':role,'bounds':m.bounds.tolist(),'watertight':True,'triangles':len(m.faces)})
 def disable(n):
  node=next(x for x in d['nodes'] if x.get('name')==n);old=node.pop('mesh');node.setdefault('extras',{})['portal_v007_superseded_mesh']=old;disabled.append(n)
 def frame(tag,xlo,xhi,y,z,w):
  h=2.4;t=.22
  # Reveal walls terminate exactly outside the clear aperture, full sleeve depth.
  for side,sg in [('LEFT',-1),('RIGHT',1)]:
   zlo,zhi=(z-w/2-t,z-w/2) if sg<0 else (z+w/2,z+w/2+t)
   add(tag+'_'+side+'_JAMB_REVEAL',box([xlo,y-.12,zlo],[xhi,y+h,zhi]),'frame')
  add(tag+'_HEADER_REVEAL',box([xlo,y+h,z-w/2-t],[xhi,y+h+t,z+w/2+t]),'frame')
  add(tag+'_FLUSH_THRESHOLD',box([xlo,y-.12,z-w/2],[xhi,y+.001,z+w/2]),'floor',role='WALKING_SURFACE')
  # Narrow exterior architrave closes the reveal-to-cladding joint.
  for side,sg in [('LEFT',-1),('RIGHT',1)]:
   zl,zh=(z-w/2-.32,z-w/2-.22) if sg<0 else (z+w/2+.22,z+w/2+.32)
   add(tag+'_'+side+'_FACE_TRIM',box([xlo-.035,y,zl],[xlo+.045,y+h+.32,zh]),'reveal')
  add(tag+'_HEAD_FACE_TRIM',box([xlo-.035,y+h+.22,z-w/2-.32],[xlo+.045,y+h+.32,z+w/2+.32]),'reveal')
  portals.append({'id':tag,'x_range':[xlo,xhi],'floor_y':y,'center_z':z,'width':w,'height':h,'status':'PROVISIONAL_OPEN_DOORWAY_NO_DOOR_LEAF'})
 # Fill source Trylon's large rectangular aperture, following its leaning facade.
 wall=box([-.13,12.162,-4.9068],[.13,24.7188,4.9068])
 wall.vertices[:,0]+= -36.5652+(wall.vertices[:,1]-12.192)*(-.511/12.4968)+.015
 cuts=[box([-40,FLOOR-.12,z-1.42],[-34,FLOOR+2.62,z+1.42]) for z in [3.048000082373619,-3.15]]
 wall=trimesh.boolean.difference([wall,*cuts],engine='manifold');add('TRYLON_PROVISIONAL_TWO_DOOR_INFILL_WALL',wall)
 for tag,z in [('TRYLON_ENTRY',3.048000082373619),('TRYLON_EXIT',-3.15)]:frame(tag,-37.15,-36.15,FLOOR,z,2.4)
 # Source brace cut caps meet the deep solid jambs. Record each cap contact.
 brace=world(s,'Trylon_Face_3_Frame__RUNTIME_SHARED_APERTURES_v004');contacts=[]
 for z in [3.048000082373619,-3.15]:
  for sg in [-1,1]:
   boundary=z+sg*1.2;mask=(np.max(abs(brace.triangles[:,:,2]-boundary),axis=1)<1e-4)
   pts=brace.triangles_center[mask];pts=pts[(abs(pts[:,0]+36.7)<1.7)&(pts[:,1]>=FLOOR)&(pts[:,1]<=FLOOR+2.4)]
   if not len(pts):raise ValueError('Expected cut cap absent')
   contacts.append({'z':boundary,'cap_triangles':len(pts),'all_inside_jamb_x_depth':bool(((pts[:,0]>=-37.15)&(pts[:,0]<=-36.15)).all())})
 # Turn existing cut rail ends outward and back into the new jamb, never across passage.
 rail=world(s,'Helicline_Rail_-1__RUNTIME_SHARED_APERTURES_v004')
 for sg in [-1,1]:
  z=-3.15+sg*1.2;mask=np.max(abs(rail.triangles[:,:,2]-z),axis=1)<1e-4
  tri=rail.triangles_center[mask];tri=tri[(abs(tri[:,0]+36.7)<1.7)&(tri[:,1]>=FLOOR)&(tri[:,1]<=FLOOR+2.4)]
  a=tri.mean(0);a[2]=z; elbow=a+[0,0,sg*.13];anchor=elbow.copy();anchor[0]=-36.8
  add('TRYLON_EXIT_RAIL_RETURN_'+str(sg),trimesh.boolean.union([tube(a,elbow),trimesh.creation.icosphere(subdivisions=2,radius=.0325).apply_translation(elbow),tube(elbow,anchor)],engine='manifold'),'rail',role='RAIL_RETURN')
 # Exact shell apertures replace broad triangle deletion with closed cut reveals.
 shell=world(original,'Perisphere_Lower_Removable_Shell');sc=[];specs=[]
 for tag,landing in [('PERISPHERE_LOWER','Platform_1_Landing_Hypothesis'),('PERISPHERE_UPPER','Platform_2_Landing_Hypothesis')]:
  lm=world(s,landing);y=float(lm.bounds[1,1]);z=float(lm.bounds[:,2].mean());w=2.35
  sc.append(box([-32,y-.12,z-w/2-.22],[-14,y+2.62,z+w/2+.22]))
  # Include rectangle extrema in x, accounting for spherical curvature.
  xs=[-np.sqrt(27.432**2-(yy-32.6136)**2-zz**2) for yy in [y,y+2.4] for zz in [z-w/2,z+w/2]]
  xlo=min(xs)-.20;xhi=max(max(xs)+.30,float(lm.bounds[0,0])+.12)
  specs.append((tag,xlo,xhi,y,z,w));frame(tag,xlo,xhi,y,z,w)
  # Solid exterior collar follows the sphere and closes the flat reveal perimeter.
  surround=box([xlo-.06,y-.15,z-w/2-.5],[xhi,y+2.9,z+w/2+.5])
  inner_sphere=trimesh.creation.icosphere(subdivisions=5,radius=27.40);inner_sphere.apply_translation([0,32.6136,0])
  collar=trimesh.boolean.difference([surround,inner_sphere,sc[-1]],engine='manifold')
  add(tag+'_CURVED_WALL_COLLAR',collar,'wall')
  for part in ['JAMB_N','JAMB_S','HEAD','SILL_GUIDE']:disable('INTERPRETIVE_'+tag.split('_')[-1]+'_PORTAL_'+part)
 # Restore the inherited broad opening perimeter with a local spherical wall patch.
 outer=trimesh.creation.icosphere(subdivisions=5,radius=27.444);outer.apply_translation([0,32.6136,0])
 inner=trimesh.creation.icosphere(subdivisions=5,radius=27.328);inner.apply_translation([0,32.6136,0])
 patch=trimesh.boolean.intersection([outer,box([-32,14,-6.5],[-14,23.5,6.5])],engine='manifold')
 patch=trimesh.boolean.difference([patch,inner],engine='manifold')
 shell=trimesh.boolean.union([shell,patch],engine='manifold')
 shell=trimesh.boolean.difference([shell,*sc],engine='manifold')
 add('PERISPHERE_PRECISE_FRAMED_SHELL_v007',shell,'wall',replace='Perisphere_Lower_Removable_Shell__UNREAL_PORTALS_v001',role='SHELL')
 # Replace superseded single stair and move upper approach outside the full reveal.
 if 'PROVISIONAL_UPPER_EXIT_STAIR' in s.graph.nodes_geometry:disable('PROVISIONAL_UPPER_EXIT_STAIR')
 tag,xlo,xhi,y,z,w=specs[1]
 start=np.array([xlo-1.8,y,z]);finish=np.array([-30.25,FLOOR,3.048000082373619]);v=finish-start;v[1]=0
 length=np.linalg.norm(v);direction=v/length;across=np.array([-direction[2],0,direction[0]])
 add('PERISPHERE_UPPER_OUTER_LANDING',box([start[0]-.15,y-.16,z-w/2],[xlo+.10,y,z+w/2]),'floor',replace='PROVISIONAL_UpperLandingToStair',role='WALKING_SURFACE')
 rise=y-FLOOR;count=23
 for i in range(count):
  a=start+v*i/count;c=start+v*(i+1)/count;a[1]=c[1]=y-rise*(i+1)/count
  m=trimesh.creation.box(extents=(length/count,.16,1.85));m.apply_transform(trimesh.geometry.align_vectors([1,0,0],direction));m.apply_translation((a+c)/2-[0,.08,0])
  add('PERISPHERE_UPPER_REPOSITIONED_TREAD_%02d'%(i+1),m,'floor',replace='PROVISIONAL_UpperReturnStair_%02d'%(i+1),role='WALKING_SURFACE')
 for side,sg in [('L',-1),('R',1)]:
  offset=across*sg*.925;a=start+offset+[0,1,0];c=finish+offset+[0,1,0]
  add('PERISPHERE_UPPER_REPOSITIONED_RAIL_'+side,tube(a,c),'rail',replace='INTERPRETIVE_UPPER_EXIT_HANDRAIL_'+side,role='RAIL_RETURN')
  for j,t in enumerate(np.linspace(0,1,9)):
   q=start*(1-t)+finish*t+offset
   add('PERISPHERE_UPPER_REPOSITIONED_POST_'+side+'_%02d'%j,tube(q,q+[0,1,0],.0225),'rail',replace='INTERPRETIVE_UPPER_EXIT_POST_'+side+'_%02d'%j,role='RAIL_RETURN')
  # Connect diagonal stair rail to landing edge, then into the matching doorway jamb.
  sign=np.sign(a[2]-z);elbow=np.array([a[0],y+1,z+sign*(w/2+.04)]);anchor=np.array([xlo+.10,y+1,elbow[2]])
  add('PERISPHERE_UPPER_LANDING_RAIL_'+side,trimesh.boolean.union([tube(a,elbow),trimesh.creation.icosphere(subdivisions=2,radius=.0325).apply_translation(elbow),tube(elbow,anchor)],engine='manifold'),'rail',role='RAIL_RETURN')
 write_glb(OUT/'ThemeCenter_Framed_Portals_v007.glb',d,b)
 report={'schema':'fmp.framed-portals.v007','input_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'original_sha256':hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(),'portals':portals,'parts':parts,'disabled':disabled,'replaced':replaced,'brace_cap_contacts':contacts,'source_binary_prefix_preserved':bytes(b[:len(old_bin)])==old_bin,'status':'PROVISIONAL_ARCHITECTURE','local_shell_patch':{'outer_radius_m':27.444,'inner_radius_m':27.328,'bounds':[[-32,14,-6.5],[-14,23.5,6.5]],'status':'PROVISIONAL_FIT_TO_INHERITED_SPHERE'},'limits':['No historical door dimensions or finish evidence claimed','No structural load-transfer calculation','No Unreal traversal','No hinged door leaves; openings remain usable'],'output_sha256':hashlib.sha256((OUT/'ThemeCenter_Framed_Portals_v007.glb').read_bytes()).hexdigest()}
 (OUT/'portal_manifest.json').write_text(json.dumps(report,indent=2));print('Built',len(parts),'parts; portals',len(portals));return report
if __name__=='__main__':build()
