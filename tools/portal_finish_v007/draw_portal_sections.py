"""Orthographic section plate measured directly from the unchanged v007 GLB."""
import hashlib,json
from pathlib import Path
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['svg.fonttype']='none'
from matplotlib.collections import LineCollection
R=Path(__file__).parent
asset=R/'output/ThemeCenter_Framed_Portals_v007.glb'
manifest=json.loads((R/'output/portal_manifest.json').read_text())
scene=trimesh.load(asset,force='scene',process=False)
world={}
for name in scene.graph.nodes_geometry:
    transform,key=scene.graph[name]
    mesh=scene.geometry[key].copy();mesh.apply_transform(transform);world[name]=mesh
fig,axes=plt.subplots(2,2,figsize=(14,11),facecolor='#faf9f5')
fig.subplots_adjust(left=.065,right=.96,top=.86,bottom=.13,hspace=.42,wspace=.27)
fig.text(.065,.95,'THEME CENTER / PORTAL SECTIONS',fontsize=23,weight='bold',color='#17333f')
fig.text(.065,.912,'v007 runtime geometry  |  Equal-scale sections normal to X  |  Dimensions in metres',fontsize=12)
rows=[]
for ax,p in zip(axes.flat,manifest['portals']):
    name=p['id']; y=p['floor_y'];z=p['center_z'];x=sum(p['x_range'])/2
    selected=[]
    for n,m in world.items():
        if m.bounds[0,0]>x or m.bounds[1,0]<x:continue
        if m.bounds[1,1]<y-.5 or m.bounds[0,1]>y+3.4 or m.bounds[1,2]<z-2 or m.bounds[0,2]>z+2:continue
        lines=trimesh.intersections.mesh_plane(m,[1,0,0],[x,0,0])
        if not len(lines):continue
        lines=lines[:,:,[2,1]]-np.array([z,y])
        lines=lines[~((lines[:,:,0].max(1)<-2)|(lines[:,:,0].min(1)>2)|(lines[:,:,1].max(1)<-.5)|(lines[:,:,1].min(1)>3.4))]
        color='#183c4a' if n.startswith(name) else '#9badae'
        ax.add_collection(LineCollection(lines,colors=color,linewidths=1.15 if n.startswith(name) else .6))
        selected.append(n)
    left=world[name+'_LEFT_JAMB_REVEAL'].bounds[1,2]-z
    right=world[name+'_RIGHT_JAMB_REVEAL'].bounds[0,2]-z
    top=world[name+'_HEADER_REVEAL'].bounds[0,1]-y
    bottom=world[name+'_FLUSH_THRESHOLD'].bounds[1,1]-y
    width=right-left;height=top-bottom
    ax.annotate('',(left,.6),(right,.6),arrowprops=dict(arrowstyle='<->',color='#b2512e',lw=1.1))
    ax.text((left+right)/2,.7,f'{width:.3f} clear',ha='center',fontsize=11,color='#934021',bbox=dict(facecolor='#faf9f5',edgecolor='none',pad=2))
    ax.annotate('',(0,bottom),(0,top),arrowprops=dict(arrowstyle='<->',color='#b2512e',lw=1.1))
    ax.text(.09,1.35,f'{height:.3f}',rotation=90,va='center',fontsize=11,color='#934021',bbox=dict(facecolor='#faf9f5',edgecolor='none',pad=2))
    ax.set(xlim=(-2,2),ylim=(-.5,3.4),aspect='equal',xlabel='Z offset from doorway centre (m)',ylabel='Height above slab datum (m)')
    ax.set_facecolor('#faf9f5');ax.grid(alpha=.15);ax.set_axisbelow(True)
    ax.set_title(name.replace('_',' ')+f'\nSection X = {x:.3f} m',loc='left',fontsize=12,weight='bold',pad=10)
    rows.append(dict(portal=name,section_x=x,clear_width=width,threshold_to_header=height,frame_depth=p['x_range'][1]-p['x_range'][0],section_nodes=selected))
fig.text(.065,.067,'Dark lines: doorway frame. Light lines: intersected surrounding model. Orange: measured clear dimensions.',fontsize=10)
fig.text(.065,.043,'PROVISIONAL MODEL DETAILS. Not surveyed historical doors, construction drawings or Unreal traversal certification.',fontsize=10,color='#934021')
fig.savefig(R/'output/FMP_Portal_Sections_v007.png',dpi=180)
fig.savefig(R/'output/FMP_Portal_Sections_v007.svg')
(R/'output/portal_section_measurements.json').write_text(json.dumps(dict(asset_sha256=hashlib.sha256(asset.read_bytes()).hexdigest(),units='metres',measurements=rows),indent=2)+'\n')
print(json.dumps([{k:v for k,v in r.items() if k!='section_nodes'} for r in rows],indent=2))
