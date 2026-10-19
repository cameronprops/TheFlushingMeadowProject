#!/usr/bin/env python3
"""FMP Westinghouse 1939 preliminary photographic massing, LOCAL ONLY.

KNOWN FROM PERIOD SOURCES: Tower 150 ft (45.72 m).
REPORTED, NOT INDEPENDENTLY VERIFIED: two wings 55 ft high, 25,200 sq ft
area (may be gross floor area), 120 ft maximum fountain jet.
ASSUMED: EVERY OTHER SIZE and shape parameter, site rotation, topography.
NO geographical placement or 1939/1940 year parity is asserted.
The model is a deliberately separated drafted hypothesis, NOT archival truth.
"""
from pathlib import Path
import json, math, hashlib
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PatchPolygon, Circle as PatchCircle

HERE=Path(__file__).resolve().parent
FEET=0.3048
PARAMS={
 'tower_height_m': 150*FEET,    # 1939 licensed postcard
 'wing_height_m':55*FEET,      # provisional transcription of historic descriptive card
 'central_foyer_height_m':11.5,   # inferred
 'wing_width_m':35.0,        # illustrative, not surveyed
 'wing_depth_m':26.0,        # illustrative, not surveyed
 'wing_front_bulge_m':4.5,   # interpretive
 'wing_center_offset_x_m':30.5, # interpretive
 'rear_link_width_m':38.0,   # interpretive
 'rear_link_depth_m':13.0,   # interpretive
 'forecourt_radius_m':9.0,   # interpretive
 'tower_body_width_m':3.1,   # interpretive
 'tower_footing_y_m':4.0,    # interpretive
 'approx_fountain_jet_peak_m':120*FEET, # reported jet, not modeled solid
 'reported_area_ft2':25200, # secondary transcription, ambiguous GFA/footprint
}
MATS={
 'cream': [207,204,190,255], 'glass': [79,125,146,178],
 'dark': [65,69,80,255], 'metal': [154,161,160,255],
 'pool': [40,103,131,176], 'light': [235,223,176,255],
}
SCENE=trimesh.Scene()
COMPONENTS=[]

def add(name,mesh,color='cream',evidence='PHOTO_INFERRED_GEOMETRY',source=''):
 mesh.visual.vertex_colors=np.tile(MATS[color],(len(mesh.vertices),1))
 mesh.metadata.update(fmp_evidence=evidence,source=source,model_scope='LOCAL_UNREGISTERED')
 SCENE.add_geometry(mesh,node_name=name,geom_name=name)
 COMPONENTS.append(dict(id=name,evidence=evidence,source=source,color=color,
                        triangles=len(mesh.faces)))

def box(name,mins,maxs,color='cream',**kwargs):
 low=np.asarray(mins,float);high=np.asarray(maxs,float)
 m=trimesh.creation.box(extents=(high-low))
 m.apply_translation((high+low)/2)
 add(name,m,color,**kwargs)

def cyl(name,radius,height,center,color='metal',sections=48,**kwargs):
 m=trimesh.creation.cylinder(radius=radius,height=height,sections=sections)
 m.apply_translation(np.asarray(center,float));add(name,m,color,**kwargs)

def prism(name,xy,h,color='cream',**kwargs):
 """A strictly convex planar polygon prism, with stable explicit triangle winding."""
 n=len(xy);vertices=np.array([(x,y,z) for z in (0.0,h) for x,y in xy],float)
 fs=[]
 for j in range(1,n-1):
  fs.extend([(0,j+1,j),(n,n+j,n+j+1)])
 for j in range(n):
  k=(j+1)%n
  fs.extend([(j,k,n+k),(j,n+k,n+j)])
 m=trimesh.Trimesh(vertices=vertices,faces=fs,process=False)
 add(name,m,color,**kwargs)

wing_outlines=[]
for i,side in enumerate((-1,1)):
 cx=side*PARAMS['wing_center_offset_x_m']; w=PARAMS['wing_width_m']; dep=PARAMS['wing_depth_m'];b=PARAMS['wing_front_bulge_m']
 # Front wing elevation is a gentle curved glazed bow; rear links to shared hall.
 # Polygon ordered counterclockwise from rounded front left to right, then rear.
 xs=np.linspace(cx-w/2,cx+w/2,21)
 curve=[(float(x),float(-b*math.sin(math.pi*(x-(cx-w/2))/w))) for x in xs]
 outline=curve+[(cx+w/2,dep),(cx-w/2,dep)]
 wing_outlines.append(outline)
 prism(f'WH39_WING_{"WEST" if side==-1 else "EAST"}_SHELL',outline,PARAMS['wing_height_m'],
       evidence='REPORTED_HEIGHT_PHOTO_INFERRED_FOOTPRINT',source='PERIOD_POSTCARD_DIMENSIONS_AND_LOC_EXTERIOR')
 # Lightly tinted glazing segments follow exposed bow on front. No assertion of exact bays.
 for k in range(20):
  p0=np.asarray(curve[k]);p1=np.asarray(curve[k+1]);d=p1-p0; length=np.linalg.norm(d)
  if length<1e-7:continue
  # Quad has tiny 3D thickness; facade rises from 1 m to parapet.
  normal=np.array([-d[1],d[0]]) / length
  # Polyline front spans increasing X with interior to its left => outward to its right.
  outward=-normal
  v0=p0+outward*.10;v1=p1+outward*.10
  glass=trimesh.Trimesh(vertices=[[v0[0],v0[1],1.4],[v1[0],v1[1],1.4],
                                [v1[0],v1[1],PARAMS['wing_height_m']-1.5],
                                [v0[0],v0[1],PARAMS['wing_height_m']-1.5]],
                        faces=[[0,1,2],[0,2,3]],process=False)
  add(f'WH39_{"W" if side==-1 else "E"}_GLASS_{k:02}',glass,'glass',
      evidence='PHOTO_CONSTRAINED_BAY_COUNT_UNKNOWN')
 # Model a thin uninterrupted curved coping (actual detailing not measured).
 for k in range(20):
  p0=curve[k];p1=curve[k+1]; a=np.array([*p0,PARAMS['wing_height_m']]);q=np.array([*p1,PARAMS['wing_height_m']]);
  vec=q-a;length=np.linalg.norm(vec)
  bar=trimesh.creation.box(extents=[length,.38,.45]);bar.apply_transform(trimesh.transformations.rotation_matrix(math.atan2(vec[1],vec[0]),[0,0,1]));bar.apply_translation((a+q)/2)
  add(f'WH39_{"W" if side==-1 else "E"}_COPING_{k:02}',bar,'cream',evidence='PHOTOGRAPHIC_DETAIL_APPROX')
 # Transverse facade horizontal bands on 3 levels, count interpretive.
 for level in [5.2,10.6]:
  for k in range(20):
   p0=np.array([*curve[k],level]);p1=np.array([*curve[k+1],level]);vec=p1-p0;L=np.linalg.norm(vec)
   beam=trimesh.creation.box(extents=[L,.13,.16]);beam.apply_transform(trimesh.transformations.rotation_matrix(math.atan2(vec[1],vec[0]),[0,0,1]));beam.apply_translation((p0+p1)/2)
   add(f'WH39_{"W" if side==-1 else "E"}_MULLION_{int(level*10)}_{k:02}',beam,'metal',evidence='PHOTO_CONSTRAINED_SPACING_INTERPRETIVE')

# Rear crosspiece closes the horseshoe as the archive description suggests.
box('WH39_REAR_CONNECTOR',[-19.5,22,0],[19.5,35,PARAMS['central_foyer_height_m']],
    evidence='HORSESHOE_MASSING_PHOTO_INFERRED')
# Foyer glazing at front of connector
box('WH39_CENTRAL_GLAZED_FOYER',[-14.5,21.7,1.0],[14.5,22,10], 'glass',evidence='PHOTO_INFERRED')
# Bridge / covered central hall fascia
box('WH39_REAR_ROOFLINE',[-19.5,34,10.7],[19.5,36,11.8],evidence='PHOTO_INFERRED')
# Time Capsule / tower assembly, iconic vertical feature
h=PARAMS['tower_height_m']; y=PARAMS['tower_footing_y_m']
box('WH39_SINGING_TOWER_SPINE',[-1.55,y-1.2,0],[1.55,y+1.2,h],'light',
    evidence='PERIOD_POSTCARD_HEIGHT_PHOTO_INFERRED_BODY',source='LICENSED_1939_POSTCARD_150FT')
box('WH39_SINGING_TOWER_FRONT_LIGHT',[-1.18,y-1.33,2],[1.18,y-1.19,h-1.0],'glass',evidence='PHOTO_INFERRED')
for i,z in enumerate([10.5,19.7,29.0,38.2,44.2]):
 # Vertical emphasis rings observed, but count/heights/diameter remain interpretive.
 radius=4.5-0.045*z
 for j in range(32):
  t0=j*2*math.pi/32;t1=(j+1)*2*math.pi/32
  p0=np.array([radius*math.cos(t0),y+radius*math.sin(t0),z]);p1=np.array([radius*math.cos(t1),y+radius*math.sin(t1),z]);
  v=p1-p0;L=np.linalg.norm(v)
  rail=trimesh.creation.box(extents=[L,.11,.18]);rail.apply_transform(trimesh.transformations.rotation_matrix(math.atan2(v[1],v[0]),[0,0,1]));rail.apply_translation((p0+p1)/2)
  add(f'WH39_TOWER_RING_{i}_{j:02}',rail,'metal',evidence='PHOTO_INFERRED_RING_LEVEL_AND_DIAMETER')
# Forecourt circular water basin at tower base, center approximated.
cyl('WH39_FOUNTAIN_POOL_BASE',PARAMS['forecourt_radius_m'],.16,(0,-5,-.1),'pool',evidence='PHOTO_CONFIRMED_FOUNTAIN_FORM_ESTIMATED_DIMENSION')
cyl('WH39_FOUNTAIN_CENTER_PEDESTAL',1.05,1.8,(0,-5,.9),'cream',evidence='PHOTO_INFERRED_FOUNTAIN_EQUIPMENT')
# 1938 capsule geographical site is deliberately not placed at this model origin,
# because capsule-to-pavilion local transform is not yet established.

# Declared 25,200 sq ft is uncertain whether floor area or footprint; our massing area is not calibrated to it.
# Figure is recorded as reported reference value only.
asset=HERE/'Westinghouse_1939_Exterior_Impression_v001.glb'
SCENE.export(asset)
models=dict(
 format='FMP_ARCHITECTURAL_DRAFT_V001',pavilion='WF0020',year=1939,
 datum='UNREGISTERED_LOCAL_XY_AND_UNRESOLVED_Z',coordinate_system='LOCAL_M_Z_UP',
 source_controls=['1939 licensed postcard 150ft tower','1939 or 1940 LOC exterior photograph','CCA tower and fountain photograph'],
 provisional_measurements=PARAMS,
 dimensions_certainty={'tower_height_m':'PERIOD_POSTCARD','wing_height_m':'SECONDARY_POSTCARD_TRANSCRIPTION',
                       'reported_area_ft2':'SECONDARY_POSTCARD_TRANSCRIPTION_AREA_DEFINITION_UNKNOWN',
                       'all_other_parameters':'MODEL_INTERPRETATION'},
 design_intent='Geometric study preserving Westinghouse pavilion silhouette; NOT surveyed as-built architecture',
 phase='PHOTOGRAPHIC_EXTERIOR_SCHEMATIC',building_location='NOT_ATTACHED_TO_THEME_CENTER_OR_WORLD',
 components=COMPONENTS,source_rights='References are links only; no copied source photograph embedded',
 fact_sources=['https://www.cardcow.com/152381/westinghouse-electric-building-exposition-1939-ny-worlds-fair/',
 'https://www.loc.gov/pictures/item/2018750438/',
 'https://www.cca.qc.ca/en/search/details/collection/object/3706',
 'https://www.cca.qc.ca/en/search/details/collection/object/3707',
 'https://www.som.com/projects/new-york-worlds-fair-1939/'],
)
models['mesh_sha256']=hashlib.sha256(asset.read_bytes()).hexdigest()
(HERE/'Westinghouse_1939_Draft_Manifest_v001.json').write_text(json.dumps(models,indent=2)+'\n')

fig,ax=plt.subplots(figsize=(11.7,7.5),dpi=165)
for i,outline in enumerate(wing_outlines):
 ax.add_patch(PatchPolygon(outline,closed=True,facecolor='#cad4d8',edgecolor='#273d4c',linewidth=2.3))
ax.add_patch(PatchPolygon([(-19.5,22),(19.5,22),(19.5,35),(-19.5,35)],facecolor='#cad4d8',edgecolor='#273d4c',linewidth=2))
ax.add_patch(PatchCircle((0,4),radius=2.5,facecolor='#e2b971',edgecolor='#273d4c'))
ax.add_patch(PatchCircle((0,-5),radius=9,facecolor='#a0c9dd',edgecolor='#528da4',lw=2))
ax.annotate('SINGING TOWER\n150 ft [period postcard]',(0,4),xytext=(14,-18),arrowprops={'arrowstyle':'->'},fontsize=9)
ax.text(-30,10,'WEST HALL\n[shape inferred]',fontsize=9,ha='center',va='center')
ax.text(30,10,'EAST HALL\n[shape inferred]',fontsize=9,ha='center',va='center')
ax.text(0,28,'REAR CONNECTOR\n[inferred]',fontsize=9,ha='center',va='center')
ax.text(0,-5,'FOUNTAIN',fontsize=8,ha='center',va='center')
ax.set_title('WESTINGHOUSE ELECTRIC BUILDING · 1939\nArchitectural hypothesis · schematic plan · NOT SURVEY-REGISTERED',loc='left',fontsize=14,fontweight='bold')
ax.set_aspect('equal');ax.set_xlim(-58,58);ax.set_ylim(-27,47);ax.set_xlabel('Draft local X (m) · provisional');ax.set_ylabel('Draft local Y (m) · provisional');ax.grid(alpha=.13)
fig.text(.09,.025,'DRAFT ONLY: wing dimensions, outline, opening, connector, tower offsets and basin are photogrammetric hypotheses.\nOnly the 150-ft tower height is supported by the period postcard; area/wing-height figures require archive verification.',fontsize=8)
fig.tight_layout(rect=[0,.07,1,1]);fig.savefig(HERE/'Westinghouse_1939_Schematic_Plan_v001.png');fig.savefig(HERE/'Westinghouse_1939_Schematic_Plan_v001.svg');plt.close(fig)

fig,ax=plt.subplots(figsize=(11.7,6.5),dpi=165)
from matplotlib.patches import Rectangle
for cx in (-30.5,30.5):
 ax.add_patch(Rectangle((cx-17.5,0),35,55*FEET,facecolor='#c4d4d9',edgecolor='#283844',lw=2))
 for x in np.linspace(cx-15,cx+15,9):ax.plot([x,x],[1,14.5],color='#577f91',lw=.65)
 for y0 in [5.2,10.6]:ax.plot([cx-17.5,cx+17.5],[y0,y0],color='#577f91',lw=.85)
ax.add_patch(Rectangle((-1.55,0),3.1,h,facecolor='#e4c69f',edgecolor='#273d4c',lw=2))
for z in [10.5,19.7,29,38.2,44.2]:
 ax.plot([-4.2,4.2],[z,z],color='#788a99',lw=2)
ax.set_title('WESTINGHOUSE ELECTRIC BUILDING · 1939\nFront elevation silhouette · tower 45.72 m · wing 16.76 m (unverified)',loc='left',fontsize=13)
ax.set_aspect('equal');ax.set_xlim(-53,53);ax.set_ylim(-3,51)
ax.set_xlabel('Draft frontage (m) · interpretive');ax.set_ylabel('Height above model datum (m)');ax.grid(alpha=.15)
fig.text(.09,.02,'Tower height from 1939 licensed postcard. Wing height from secondary card transcription. All widths/spacing interpretive.',fontsize=8)
fig.tight_layout(rect=[0,.05,1,1]);fig.savefig(HERE/'Westinghouse_1939_Schematic_Elevation_v001.png');fig.savefig(HERE/'Westinghouse_1939_Schematic_Elevation_v001.svg');plt.close(fig)
print(json.dumps(dict(glb=str(asset),bytes=asset.stat().st_size,components=len(COMPONENTS),tower_height_m=h,assumed_wing_span_m=96,verified_source_heights='150ft tower only',trimesh_geometries=len(SCENE.geometry)),indent=2))
