"""Render a read-only actual GLB section; not a reconstruction of missing architecture."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
import trimesh
from scipy.spatial import ConvexHull
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
SHA='de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439'
NODES={
 'trylon':'Trylon_Hollow_Exterior__RUNTIME_SHARED_APERTURES_v004',
 'lower_sphere':'Perisphere_Lower_Removable_Shell__UNREAL_PORTALS_v001',
 'upper_sphere':'Perisphere_Upper_Removable_Shell',
 'lobby':'Trylon_Lobby_Floor_Envelope',
 'escalator_1':'Escalator_1_Envelope','escalator_2':'Escalator_2_Envelope',
 'treads_1':'Escalator_1_Tread_Proxies','treads_2':'Escalator_2_Tread_Proxies',
 'bridge':'Return_Bridge_Deck'}
def transformed_vertices(scene,node):
 if node not in scene.graph.nodes_geometry:raise ValueError('Missing scene geometry: '+node)
 transform,geometry=scene.graph[node]
 return trimesh.transform_points(scene.geometry[geometry].vertices,transform)
def xy_hull(arr):
 points=arr[:,:2]
 return points[ConvexHull(points).vertices]
def run(path,out):
 path,out=Path(path),Path(out)
 if hashlib.sha256(path.read_bytes()).hexdigest()!=SHA:raise ValueError('Unknown runtime GLB SHA256')
 scene=trimesh.load(path,force='scene')
 vertices={k:transformed_vertices(scene,n) for k,n in NODES.items()}
 records={k:{'node':NODES[k],'bbox_min_m':v.min(axis=0).round(6).tolist(),'bbox_max_m':v.max(axis=0).round(6).tolist()} for k,v in vertices.items()}
 b=records['bridge'];thickness=b['bbox_max_m'][1]-b['bbox_min_m'][1]
 report={'schema':'fmp.theme-center.bridge-entry-model-gap.v001','sha256':SHA,'model_frame':'unregistered Y-up metres','records':records,'bridge_deck_bbox_y_thickness_m':round(thickness,6), 'status':{'bridge_arched_soffit':'NOT_MODELED','public_entrance_canopy':'NOT_MODELED','lobby_paneling':'NOT_VERIFIED','native_unreal':'NOT_TESTED'},'limits':['XY projection is not a photograph or a section of built history','The earlier v006 return-portal experiment does not substitute for the ground entrance','Never use previous AI illustration as reference']}
 out.mkdir(parents=True,exist_ok=True)
 (out/'GLB_BRIDGE_ENTRY_MEASUREMENTS_v001.json').write_text(json.dumps(report,indent=2)+'\n')
 fig,ax=plt.subplots(figsize=(14,8),dpi=160)
 fig.patch.set_facecolor('#faf9f6');ax.set_facecolor('#faf9f6')
 for k,col in [('trylon','#ddd8ce'),('lower_sphere','#ededeb'),('upper_sphere','#ededeb')]:
  ax.add_patch(Polygon(xy_hull(vertices[k]),closed=True,facecolor=col,edgecolor='#a8a9a7',alpha=.84,lw=1.0))
 for k,col in [('escalator_1','#327ca1'),('escalator_2','#bc6e29')]:
  ax.add_patch(Polygon(xy_hull(vertices[k]),closed=True,facecolor=col,edgecolor=col,alpha=.13))
 for k,col in [('treads_1','#327ca1'),('treads_2','#bc6e29')]:
  v=vertices[k];ax.plot(v[:,0],v[:,1],'.',ms=1.8,color=col,alpha=.55)
 for k,col in [('lobby','#776aa2'),('bridge','#20866c')]:
  ax.add_patch(Polygon(xy_hull(vertices[k]),closed=True,facecolor=col,edgecolor=col,alpha=.9,lw=1.2))
 labels=[('A   ESCALATOR 1   /   model proxy',(-32,9),(-62,25),'#327ca1'),
         ('B   ESCALATOR 2   /   model proxy',(-35,12),(-62,18),'#bc6e29'),
         ('C   RETURN BRIDGE: FLAT DECK ONLY',(-29,15.8),(-65,32),'#14715e'),
         ('D   PUBLIC ENTRANCE: CANOPY/SIGN MISSING',(-45,0),(-67,6),'#aa302b')]
 for label,at,xy,col in labels:
  ax.annotate(label,xy=at,xytext=xy,color=col,fontsize=10,arrowprops={'arrowstyle':'->','color':col,'lw':1.2})
 ax.text(-69,54,'ACTUAL v005 GLB  |  SOURCE GEOMETRY ONLY',fontweight='bold',fontsize=14,color='#202b32')
 ax.text(-69,51,'Projected model vertices, not a rendering of 1939 historical finishes',fontsize=10,color='#5a5d61')
 ax.set(xlim=(-70,32),ylim=(-2,57),xlabel='Model X / metres',ylabel='Model Y height / metres')
 ax.set_aspect('equal',adjustable='box');ax.grid(ls=':',alpha=.45)
 fig.subplots_adjust(top=.96,left=.06,bottom=.12,right=.99)
 fig.text(.06,.03,'Exact v005 SHA256: '+SHA[:28]+'…  ·  Flat deck thickness: %.4f m  ·  Missing architectural arch NOT invented'%(thickness),fontsize=9,color='#5b5c5a')
 fig.savefig(out/'GLB_REAL_SECTION_v001.png',dpi=180,facecolor=fig.get_facecolor());fig.savefig(out/'GLB_REAL_SECTION_v001.svg',facecolor=fig.get_facecolor());plt.close(fig)
 return report
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('glb');ap.add_argument('out');args=ap.parse_args();res=run(args.glb,args.out)
 print(json.dumps({'sha':res['sha256'],'components':len(res['records']),'bridge_deck_thickness_m':res['bridge_deck_bbox_y_thickness_m']},indent=2))
