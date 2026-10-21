from pathlib import Path
import json
import numpy as np,trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from check_landing import START
R=Path(__file__).parent;plt.rcParams['svg.fonttype']='none'
fig,axes=plt.subplots(1,2,figsize=(12,7),facecolor='#faf9f5')
for ax,path,report,title in zip(axes,[R.parent/'portal_build/output/ThemeCenter_Framed_Portals_v007.glb',R/'ThemeCenter_UpperLanding_v008.glb'],['before.json','after.json'],['BEFORE / v007','AFTER / v008']):
 s=trimesh.load(path,force='scene',process=False)
 for n in s.graph.nodes_geometry:
  if n!='PROVISIONAL_UpperLandingToStair' and not n.startswith('PROVISIONAL_UpperReturnStair_'):continue
  T,g=s.graph[n];m=s.geometry[g].copy();m.apply_transform(T)
  y=m.bounds[1,1]-.08
  lines=trimesh.intersections.mesh_plane(m,[0,1,0],[0,y,0])[:,:,[0,2]]
  ax.add_collection(LineCollection(lines,colors='#173c4a' if n=='PROVISIONAL_UpperLandingToStair' else '#9cacad',linewidths=2 if n=='PROVISIONAL_UpperLandingToStair' else .7))
 data=json.loads((R/report).read_text());pts=np.array([p['point'] for p in data['samples']])
 ax.scatter(pts[:,0],pts[:,2],c=['#29805c' if p['level_landing_support'] else '#c54632' for p in data['samples']],s=28,zorder=5)
 ax.set(xlim=(-28.8,-24.9),ylim=(-4.8,-.6),aspect='equal',xlabel='Model X (m)',ylabel='Model Z (m)')
 ax.set_title(title+'\n'+str(data['supported'])+'/15 probes on level landing',loc='left',fontsize=14,weight='bold')
 ax.set_facecolor('#faf9f5');ax.grid(alpha=.15);ax.set_axisbelow(True)
fig.subplots_adjust(top=.81,bottom=.18,wspace=.24)
fig.text(.08,.94,'PERISPHERE / UPPER STAIR JUNCTION',fontsize=20,weight='bold',color='#173c4a')
fig.text(.08,.89,'Actual mesh plan sections: landing and stair treads',fontsize=12)
fig.text(.08,.09,'Dots: 15 vertical support probes, 100 mm before the first tread. Red = missing level support.',fontsize=10)
fig.text(.08,.055,'Provisional runtime repair. No historical dimensions, structural design or Unreal traversal acceptance.',fontsize=10,color='#934021')
fig.savefig(R/'UpperLanding_Before_After.png',dpi=160);fig.savefig(R/'UpperLanding_Before_After.svg')
