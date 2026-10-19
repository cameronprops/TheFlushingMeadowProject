#!/usr/bin/env python3
"""FMP WF0014 1939/1940 Ford: source-constrained procedural exterior + road v002.

This is an UNSURVEYED visual and visitor-volume interpretation, not as-built geometry.
Outputs a GLB, PBR surface library, parametric construction schedule, two review
sheets and separate provenance manifest. Use --params to alter all unmeasured sizes.
Dependencies: trimesh, numpy, matplotlib, PIL. No licensed reference photos embedded.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial
from trimesh.visual.texture import TextureVisuals
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

SOURCES={
 'AR38':'https://usmodernist.org/AR/AR-1938-11.pdf',
 'BROCHURE':'https://www.thehenryford.org/collections/explore/artifact/373546',
 'THF_ROAD':'https://www.thehenryford.org/collections/explore/artifact/373201',
 'THF_AERIAL':'https://www.thehenryford.org/collections/explore/artifact/65310',
 'THF_CYCLE':'https://www.thehenryford.org/collections/explore/artifact/47282',
 'THF_1940':'https://askus.thehenryford.org/bibs/faq/445890',
 'MONOCORK':'https://www.lancasterhistory.org/armstrong-worlds-fair-part-1/',
 'FERRISS':'https://www.thehenryford.org/collections/explore/artifact/31119',
}

DEFAULTS={
 'industrial_hall_center_xy_m':[-64,0],
 'industrial_hall_outer_radius_x_m':44.8,
 'industrial_hall_outer_radius_y_m':37.5,
 'industrial_hall_wall_height_m':14,
 'industrial_hall_roof_rise_m':3,
 'entrance_hall_center_xy_m':[-64,-56.5],
 'entrance_hall_width_m':75,
 'entrance_hall_depth_m':38,
 'entrance_hall_wall_height_m':12.5,
 'visitor_entrance_width_m':9,
 'road_spiral_center_xy_m':[63,12],
 'road_inner_column_ring_radius_m':21.2,
 'road_centerline_radius_m':26,
 'road_travel_width_m':4.7,
 'road_turns':2.80,
 'road_z_start_m':1.65,
 'road_z_end_m':10.0,
 'road_column_count':24,
 'road_curb_height_m':0.48,
 'road_structural_deck_thickness_m':0.44,
 'water_outer_radius_m':19.1,
 'turntable_diameter_m':30.48,
 'turntable_tier_radii_m':[15.24,12.5,9,5.2],
 'turntable_tier_heights_m':[0.9,3.4,6.25,9.25],
 'mercury_figure_vertical_extent_m':7.62,
 'period_half_mile_car_route_m':804.672,
 'ford_working_model_count':87,
 'ford_animated_figure_count':142,
 'ford_raw_material_count':27,
}
DOCUMENTED={
 'turntable_diameter_m':{'evidence':'AR38','status':'PERIOD_PRINTED', 'description':'100 foot diameter of Cycle of Production'},
 'mercury_figure_vertical_extent_m':{'evidence':'BROCHURE','status':'PERIOD_PRINTED','description':'25 foot-high Mercury symbol over main entrance'},
 'period_half_mile_car_route_m':{'evidence':'BROCHURE','status':'PERIOD_PRINTED','description':'Half-mile is total vehicle trip, NOT its spiral length'},
 'ford_working_model_count':{'evidence':'THF_CYCLE','status':'MUSEUM_CATALOG','description':'87 working models inside rotating exhibit'},
 'ford_animated_figure_count':{'evidence':'THF_CYCLE','status':'MUSEUM_CATALOG','description':'142 moving miniature figures'},
 'ford_raw_material_count':{'evidence':'THF_CYCLE','status':'MUSEUM_CATALOG','description':'27 kinds of raw materials'},
}
LOOKS={
 'painted_facade':{'baseColorFactor':[0.80,0.85,0.81,1.0],'metallicFactor':0.05,'roughnessFactor':0.53,'source':'BROCHURE','certainty':'VISUAL_ESTIMATE'},
 'glazed_band':{'baseColorFactor':[0.24,0.38,0.43,0.50],'metallicFactor':0.05,'roughnessFactor':0.18,'source':'BROCHURE','certainty':'VISUAL_ESTIMATE'},
 'roof_concrete':{'baseColorFactor':[0.67,0.71,0.68,1.0],'metallicFactor':0.04,'roughnessFactor':0.77,'source':'THF_AERIAL','certainty':'SURFACE_FAMILY_INFERRED'},
 'road_monocork':{'baseColorFactor':[0.20,0.21,0.20,1.0],'metallicFactor':0.00,'roughnessFactor':0.82,'source':'MONOCORK','certainty':'MATERIAL_DOCUMENTED_COLOR_GUESSED'},
 'steel_rail':{'baseColorFactor':[0.60,0.66,0.66,1.0],'metallicFactor':0.78,'roughnessFactor':0.31,'source':'THF_ROAD','certainty':'SURFACE_FAMILY_INFERRED'},
 'water':{'baseColorFactor':[0.07,0.36,0.46,0.7],'metallicFactor':0.02,'roughnessFactor':0.09,'source':'THF_CYCLE','certainty':'VISUAL_ESTIMATE'},
 'exhibit_stage':{'baseColorFactor':[0.60,0.63,0.58,1.0],'metallicFactor':0.12,'roughnessFactor':0.55,'source':'THF_CYCLE','certainty':'VISUAL_ESTIMATE'},
 'garden':{'baseColorFactor':[0.29,0.45,0.27,1],'metallicFactor':0.00,'roughnessFactor':0.96,'source':'THF_AERIAL','certainty':'VISUAL_ESTIMATE'},
 'interpretive_proxy':{'baseColorFactor':[0.91,0.62,0.28,1],'metallicFactor':0.12,'roughnessFactor':0.58,'source':None,'certainty':'UNMEASURED_CONCEPT_PROXY'},
}

def model(params,output):
 s=trimesh.Scene(); components=[]; materials={k:PBRMaterial(name=k, **{x:v for x,v in props.items() if x in ('baseColorFactor','metallicFactor','roughnessFactor')}) for k,props in LOOKS.items()}
 def add(mesh,part,material,confidence,evidence=None,motion=None):
  if not mesh.is_empty:
   mesh.visual=TextureVisuals(material=materials[material])
   s.add_geometry(mesh,node_name=part,geom_name=part)
   components.append({'id':part,'material_slot':material,'confidence':confidence,'evidence_id':evidence,'motion':motion})
 def box(name,c,ext,mat='painted_facade',grade='PHOTO_CONSTRAINED_HYPOTHESIS',source=None):
  mesh=trimesh.creation.box(extents=ext);mesh.apply_translation(c);add(mesh,name,mat,grade,source)
 def span(name,a,b,z,height=.2,depth=.2,mat='steel_rail',grade='PHOTO_CONSTRAINED_HYPOTHESIS'):
  a=np.asarray(a);b=np.asarray(b);d=b-a;L=np.linalg.norm(d)
  if L<.002:return
  m=trimesh.creation.box(extents=[L,depth,height]);m.apply_transform(trimesh.transformations.rotation_matrix(math.atan2(d[1],d[0]),[0,0,1]));m.apply_translation([(a[0]+b[0])/2,(a[1]+b[1])/2,z]);add(m,name,mat,grade)
 def ring(name,cx,cy,z,outer,inner,thickness,mat,segments=112,grade='PROVISIONAL'):
  verts=[];faces=[]
  for i in range(segments):
   a=2*math.pi*i/segments
   for r,h in [(inner,z),(outer,z),(inner,z+thickness),(outer,z+thickness)]:verts.append([cx+r*math.cos(a),cy+r*math.sin(a),h])
  for i in range(segments):
   j=(i+1)%segments
   idx=lambda k,t:4*k+t
   for aa,bb,cc,dd in [(0,1,1+4*0,0),(0,2,2,0),(1,3,3,1),(2,3,3,2)]:
    pass
   for f in [(idx(i,0),idx(i,1),idx(j,1),idx(j,0)),(idx(i,2),idx(j,2),idx(j,3),idx(i,3)),
             (idx(i,0),idx(j,0),idx(j,2),idx(i,2)),(idx(i,1),idx(i,3),idx(j,3),idx(j,1))]:
    faces.extend([(f[0],f[1],f[2]),(f[0],f[2],f[3])])
  add(trimesh.Trimesh(vertices=verts,faces=faces,process=False),name,mat,grade)
 # unit registration: local X/Y is illustration only, Z0 is arbitrary.
 # Broad exterior massing and open visitor volumes -- no solid hall boxes.
 cx,cy=params['industrial_hall_center_xy_m']; rx=params['industrial_hall_outer_radius_x_m'];ry=params['industrial_hall_outer_radius_y_m'];wall=params['industrial_hall_wall_height_m']
 # Oval perimeter as individual panels; intentional wide entry break on south side.
 n=72
 for k in range(n):
  a=2*math.pi*k/n;b=2*math.pi*(k+1)/n
  mx,my=cx+rx*math.cos((a+b)/2),cy+ry*math.sin((a+b)/2)
  if my<cy-ry*.89 and abs(mx-cx)<8.0:continue
  p=(cx+rx*math.cos(a),cy+ry*math.sin(a));q=(cx+rx*math.cos(b),cy+ry*math.sin(b));h=wall
  span(f'INDUSTRIAL_HALL_PERIMETER_{k:02d}',p,q,h/2,height=h,depth=.36,mat='painted_facade')
  if k%2==0:
   span(f'INDUSTRIAL_HALL_GLAZING_BAND_{k:02d}',p,q,5.2,height=2.8,depth=.39,mat='glazed_band')
 # Rooflight/rib structure and high crown. Roof deck is a shallow open fan of radial strips,
 # not a claimed as-built shell profile; occupancy spaces remain inspectable.
 for k in range(0,72,4):
  ang=2*math.pi*k/72
  p=(cx+(rx-1.3)*math.cos(ang),cy+(ry-1.3)*math.sin(ang));q=(cx+5*math.cos(ang),cy+5*math.sin(ang))
  span(f'INDUSTRIAL_ROOF_RIB_{k:02d}',p,q,wall+1.0,height=.38,depth=.40,mat='roof_concrete')
 box('INDUSTRIAL_HALL_FLOOR',(cx,cy,-.19),(2*rx,2*ry,.38),'roof_concrete')
 ex,ey=params['entrance_hall_center_xy_m'];ew=params['entrance_hall_width_m'];ed=params['entrance_hall_depth_m'];eh=params['entrance_hall_wall_height_m']
 box('ENTRANCE_HALL_FLOOR',(ex,ey,-.18),(ew,ed,.36),'roof_concrete')
 for side in [-1,1]:
  x=ex+side*ew/2
  box(f'ENTRANCE_SIDE_WALL_{side:+}',(x,ey,eh/2),(.55,ed,eh),'painted_facade')
 # Front portico broad visitor entrance and curtain glazing to either side
 ymin=ey-ed/2; door=params['visitor_entrance_width_m']
 left=ew/2-door/2
 for sign in (-1,1):
  xx=ex+sign*(door/2+left/2)
  box(f'ENTRANCE_FACADE_SOLID_{sign:+}',(xx,ymin,eh/2),(left,.5,eh),'painted_facade')
  box(f'ENTRANCE_FACADE_WINDOWS_{sign:+}',(xx,ymin-.30,5.2),(max(left-2,1),.06,3.9),'glazed_band')
 box('ENTRANCE_TRANSOM',(ex,ymin,eh-.8),(door,.50,1.6),'painted_facade')
 # back wall, with central opening to industrial hall
 ymax=ey+ed/2
 for sign in (-1,1):
  xx=ex+sign*(door/2+left/2)
  box(f'ENTRANCE_HALL_INNER_WALL_{sign:+}',(xx,ymax,eh/2),(left,.55,eh),'painted_facade')
 box('ENTRANCE_HALL_ROOF_SLICE',(ex,ey,eh+.20),(ew,ed,.4),'roof_concrete')
 # main pylon signage frame and documented 7.62 m Figure VOLUME only (not false detailed statue)
 box('MERCURY_SUPPORT_PYLON_HYP',(ex+27,ymin+5,eh+2.5),(5.2,5.2,5),'painted_facade')
 box('MERCURY_EXACT_HEIGHT_BOUNDING_PROXY_NOT_SCULPTURE',(ex+26.5,ymin+5,eh+6.8+params['mercury_figure_vertical_extent_m']/2),(.32,.32,params['mercury_figure_vertical_extent_m']),'interpretive_proxy','SCALED_EXTENT_ONLY','BROCHURE')
 # Ford lettering placeholder modeled as billboard panel not a trademark font recreation.
 box('FORD_SIGNAGE_PANEL_PROXY',(ex,ymin-.6,eh-1.9),(16,.2,2.5),'interpretive_proxy','SIGNAGE_POSITION_HYPOTHESIS','BROCHURE')
 # Garden area physically separated from roadway turntable.
 box('GARDEN_PLAZA',(55,8,-.08),(108,91,.16),'roof_concrete')
 for k in range(15):
  phi=2*math.pi*k/15; xx=39+31*math.cos(phi); yy=8+29*math.sin(phi)
  body=trimesh.creation.cylinder(radius=.2,height=4.2,sections=10);body.apply_translation([xx,yy,2.1]);add(body,f'GARDEN_TREE_TRUNK_{k:02}', 'interpretive_proxy','ENVIRONMENT_HYPOTHESIS')
  canopy=trimesh.creation.icosphere(subdivisions=1,radius=2.1);canopy.apply_translation([xx,yy,5.2]);add(canopy,f'GARDEN_TREE_CANOPY_{k:02}','garden','ENVIRONMENT_HYPOTHESIS')
 box('GARDEN_ORCHESTRA_PODIUM_HYP',(28,9,.40),(14,11,.8),'painted_facade')
 # Industrial rotating exhibit floating in water: 100 ft diameter is documented; all heights hypotheses.
 ring('INDUSTRIAL_HALL_WATER_MOAT',cx,cy,0.06,params['water_outer_radius_m'],15.65,.13,'water',grade='BASIN_DIMENSIONS_HYPOTHESIS')
 for i,(radius,h) in enumerate(zip(params['turntable_tier_radii_m'],params['turntable_tier_heights_m'])):
  # use opaque shell plates; diameter of broadest tier is documented, tier radii/heights otherwise hypotheses
  ring(f'FORD_CYCLE_TIER_{i:02d}',cx,cy,h,radius,max(0.2,radius-2.3),.42,'exhibit_stage',grade='DIAMETER_DOCUMENTED_TIER_SIZE_INTERPRETIVE')
 for k in range(8):
  phi=2*math.pi*k/8;r=15.4
  body=trimesh.creation.cylinder(radius=.75,height=.4,sections=12);body.apply_translation([cx+r*math.cos(phi),cy+r*math.sin(phi),.4]);add(body,f'PONTOON_VISUAL_PROXY_{k:02d}','interpretive_proxy','COUNT_AND_ARRANGEMENT_HYPOTHESIS','THF_CYCLE')
 # Show object is tagged as a movable parent by ID, but glb leaves pivot for Unreal Blueprints.
 # Road strip with real 3D top/bottom/curbs; uses segmented arc mesh, avoids flattened overall torus.
 sx,sy=params['road_spiral_center_xy_m'];r=params['road_centerline_radius_m'];wide=params['road_travel_width_m'];turns=params['road_turns'];z0=params['road_z_start_m'];z1=params['road_z_end_m'];N=560
 def arc_mesh(r_inner,r_outer,z_offset,thickness):
  vertices=[];faces=[]
  for i in range(N+1):
   u=i/N;ang=2*math.pi*turns*u;z=z0+(z1-z0)*u+z_offset
   for rr,zv in [(r_inner,z),(r_outer,z),(r_inner,z+thickness),(r_outer,z+thickness)]:vertices.append([sx+rr*math.cos(ang),sy+rr*math.sin(ang),zv])
  for i in range(N):
   ix=lambda a,b:4*a+b
   for t in [(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
    v=[ix(i+int(a>=4),a%4) if False else None for a in []]
    # IDs below are local offsets for current/next 4-vector
    v=[4*i+k for k in t]
    faces.extend([[v[0],v[1],v[2]],[v[0],v[2],v[3]]])
  return trimesh.Trimesh(vertices=vertices,faces=faces,process=False)
 inn=r-wide/2;out=r+wide/2
 add(arc_mesh(inn,out,-params['road_structural_deck_thickness_m'],params['road_structural_deck_thickness_m']),
     'ROAD_OF_TOMORROW_REINFORCED_CONCRETE_SPIRAL','roof_concrete','SPIRAL_ALIGNMENT_AND_RADIUS_HYPOTHESIS','AR38')
 add(arc_mesh(inn+.12,out-.12,.0,.035),'ROAD_OF_TOMORROW_MONOCORK_WEAR_LAYER','road_monocork','MATERIAL_SUPPORTED_LAYOUT_UNSURVEYED','MONOCORK')
 add(arc_mesh(inn-.12,inn+.07,.0,params['road_curb_height_m']),'ROAD_INNER_CANTILEVER_CURB','painted_facade','PHOTOGRAPHICALLY_CONSTRAINED','THF_ROAD')
 add(arc_mesh(out-.07,out+.12,.0,params['road_curb_height_m']),'ROAD_OUTER_CANTILEVER_CURB','painted_facade','PHOTOGRAPHICALLY_CONSTRAINED','THF_ROAD')
 # articulated support columns at intervals; actual count unknown, modeled only under road where decks would meet columns.
 column_ring=params['road_inner_column_ring_radius_m']
 count=params['road_column_count']
 for i in range(count):
  angle=2*math.pi*i/count
  u=angle/(2*math.pi*turns) # at base turn - single column height per support, hypothetical
  height=max(.4,z0+(z1-z0)*u-.40)
  x=sx+column_ring*math.cos(angle);y=sy+column_ring*math.sin(angle)
  box(f'ROAD_INNER_SUPPORT_COLUMN_{i:02d}',(x,y,height/2),(.8,.8,height),'roof_concrete','COLUMN_COUNT_AND_GRID_HYPOTHESIS','AR38')
 # independent spectator route (not ride) nearby connecting Garden to exhibition building
 box('GARDEN_PUBLIC_SPINE_PROXY',(0,8,.05),(20,4,.1),'roof_concrete','PUBLIC_CIRCULATION_HYPOTHESIS')
 return s,components

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent);parser.add_argument('--params',type=Path);args=parser.parse_args()
 out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
 p=dict(DEFAULTS)
 if args.params:p.update(json.loads(args.params.read_text()))
 for key in DEFAULTS:
  if key not in p:raise ValueError('Missing param '+key)
 if abs(p['turntable_diameter_m']-30.48)>.00001:raise ValueError('Documented 100-ft turntable cannot be changed silently')
 if p['road_z_start_m']>=p['road_z_end_m'] or p['road_turns']<=1:raise ValueError('Invalid road geometry')
 scene,comps=model(p,out)
 name='Ford_1939_Exterior_Road_Production_v002.glb';scene.export(str(out/name))
 loaded=trimesh.load(str(out/name),force='scene')
 if len(loaded.geometry)!=len(comps):raise AssertionError('Loss of mesh components in export')
 # Derived math: 804.672 m is ENTIRE vehicle road; not a spiral length.
 L=2*math.pi*p['road_centerline_radius_m']*p['road_turns']
 helical=math.hypot(L,p['road_z_end_m']-p['road_z_start_m'])
 pitch=(p['road_z_end_m']-p['road_z_start_m'])/L
 if helical>p['period_half_mile_car_route_m']:raise AssertionError('Spiral proxy exceeds source-reported entire roadway')
 manifest={'schema':'fmp.ford1939.exterior.v002','building_id':'WF0014','year':1939,
 'survey_registered':False,'historical_certification':False,'site_origin':'LOCAL_DIAGRAMMATIC_ONLY',
 'vertical_datum':'UNRESOLVED_GRADE_Z0_IS_ILLUSTRATIVE','parameters':p,'documented_parameter_provenance':DOCUMENTED,
 'all_other_geometry':'PHOTO_INSPIRED_EDITABLE_HYPOTHESIS','source_register':SOURCES,
 'material_slots':LOOKS,'components':comps,
 'animation_spec':{'movable_parent_id':'FORD39_CYCLE_OF_PRODUCTION','unknown_rpm':True,'theta(t)':'theta0 + 2*pi*rpm*t/60','kinematic_geometry':'88? static placeholder diorama figures are NOT modeled in this exterior pass'},
 'road_math':{'total_reported_m':p['period_half_mile_car_route_m'],'spiral_model_2d_length_m':L,'spiral_model_helical_length_m':helical,'remaining_linking_roads_m_hypothesis':p['period_half_mile_car_route_m']-helical,'spiral_grade_percent_model_only':100*pitch,'tier_count_historic':3,'model_turn_count_interpretive':p['road_turns']},
 'quality':{'glb_reloaded':True,'mesh_count':len(loaded.geometry),'mesh_node_count':len(loaded.graph.nodes),'197?':None,'walkability_tested_in_unreal':False,'realistic_materials_lookdev_only':True,'minecraft_export_implemented':False,
 'source_1938_plan_image_acquired':False,'1939_1940_states_separated':True},
 'publication_note':'Do not confuse this scenic reconstruction proxy with as-built construction drawings.'}
 (out/'Ford_1939_Exterior_Road_Parameters_v002.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
 # Site diagram (schematic area geometry): source-based purple dashed measured disk
 fig,ax=plt.subplots(figsize=(13.5,8),dpi=160)
 ax.set_aspect('equal');ax.set_facecolor('#f4f7f6')
 cx,cy=p['industrial_hall_center_xy_m'];rx=p['industrial_hall_outer_radius_x_m'];ry=p['industrial_hall_outer_radius_y_m']
 t=np.linspace(0,2*math.pi,350)
 ax.plot(cx+rx*np.cos(t),cy+ry*np.sin(t),color='#db923f',lw=2.6,label='Hypothetical building envelope')
 circ=Circle((cx,cy),15.24,edgecolor='#0b7c88',fill=False,lw=3.0,label='100-ft documented rotating feature');ax.add_patch(circ)
 ax.add_patch(Circle((cx,cy),p['water_outer_radius_m'],edgecolor='#67b3c8',fill=False,lw=2))
 ex,ey=p['entrance_hall_center_xy_m'];ew=p['entrance_hall_width_m'];ed=p['entrance_hall_depth_m']
 ax.add_patch(Rectangle((ex-ew/2,ey-ed/2),ew,ed,fill=False,edgecolor='#db923f',lw=2.5))
 sx,sy=p['road_spiral_center_xy_m'];tt=np.linspace(0,2*math.pi*p['road_turns'],420)
 for rr in (p['road_centerline_radius_m']-p['road_travel_width_m']/2,p['road_centerline_radius_m']+p['road_travel_width_m']/2):ax.plot(sx+rr*np.cos(tt),sy+rr*np.sin(tt),color='#6e7980',lw=1.7,alpha=.84)
 ax.add_patch(Rectangle((0,-38),110,95,facecolor='#cdddc8',alpha=.32,edgecolor='#618260',lw=1.3))
 ax.text(cx,cy-3,'CYCLE OF\nPRODUCTION',ha='center',va='center',fontsize=10,fontweight='bold')
 ax.text(ex,ey,'ENTRANCE HALL',ha='center',fontsize=9)
 ax.text(42,-27,'GARDEN COURT',ha='center',fontsize=10)
 ax.text(sx,sy,'ROAD\nSPIRAL',ha='center',va='center',fontsize=10)
 ax.add_patch(FancyArrowPatch((cx-15.24,cy+19),(cx+15.24,cy+19),arrowstyle='<->',mutation_scale=13,color='#0b7c88'))
 ax.text(cx,cy+23,'30.48 m — source-backed',ha='center',fontsize=9,color='#0b7c88')
 ax.set_xlim(-124,127);ax.set_ylim(-102,73);ax.grid(alpha=.15)
 ax.set_xlabel('Unregistered local X — metres');ax.set_ylabel('Unregistered local Y — metres')
 ax.set_title('FORD EXPOSITION | PHOTO-CONSTRAINED PLAN / REV 002',fontsize=15,fontweight='bold')
 ax.text(.02,.015,'TEAL: documented turntable only    •    ORANGE: hypothetical envelope    •    GRAY: interpreted roadway',transform=ax.transAxes,fontsize=9,color='#50616b',bbox={'facecolor':'white','edgecolor':'none','alpha':.86})
 fig.tight_layout();fig.savefig(out/'A102_Ford_Exterior_Road_Plan_v002.png');plt.close(fig)
 # schematic ramp sectional diagram x arc-length, not pretending real cross section of circular plan
 fig,ax=plt.subplots(figsize=(13.5,5.8),dpi=160)
 u=np.linspace(0,1,420);long=u*helical;heights=p['road_z_start_m']+(p['road_z_end_m']-p['road_z_start_m'])*u
 ax.plot(long,heights,'#4d6975',lw=12,solid_capstyle='round');ax.plot(long,heights+.025,'#363a3b',lw=3,solid_capstyle='round')
 for k in range(1,4):ax.axhline(p['road_z_start_m']+k*(p['road_z_end_m']-p['road_z_start_m'])/3,c='#7dabb6',ls=':',alpha=.45)
 ax.text(.02,.88,'ROAD: THREE-TIER SPIRAL SUPPORT CONCEPT\nNot a measured 1939 section; levels and 2.8 turns remain estimates',transform=ax.transAxes,fontsize=11,weight='medium')
 ax.text(.02,.1,f"Computed model helical travel: {helical:.1f} m   |   average grade: {100*pitch:.2f}%\nPeriod advertised whole Road of Tomorrow: 804.672 m (not all spiral)",transform=ax.transAxes,fontsize=10)
 ax.set(xlabel='Modeled distance along spiral (metres)',ylabel='Local design elevation (metres)');ax.set_ylim(0,15);ax.grid(alpha=.20);fig.tight_layout();fig.savefig(out/'A302_Ford_Road_Engineering_v002.png');plt.close(fig)
 # reproducibility and checklist
 glb=out/name
 manifest['quality']['model_sha256']=hashlib.sha256(glb.read_bytes()).hexdigest()
 (out/'Ford_1939_Exterior_Road_Parameters_v002.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'status':'PASSED_GLTF_ROUNDTRIP','geometry':len(loaded.geometry),'road_length_m':round(helical,3),'grade_pct':round(100*pitch,3),'output':str(glb)},indent=2))
if __name__=='__main__':main()
