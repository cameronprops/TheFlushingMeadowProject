#!/usr/bin/env python3
"""FMP Ford 1939 procedural v003. Run alongside build_ford_exterior_v002.py.

For printable/closed architectural source components, replaces the original
open-ended spiral deck, generates an explicit multi-level inner column and
cantilever support system, and creates two separate interpretive roadway links.
All dimensions other than documented counts, the Cycle diameter and advertised
length remain provisional. No historic photo rights conveyed by this package.
"""
from __future__ import annotations
import argparse, hashlib, json, math, copy
from pathlib import Path
import numpy as np
import trimesh
import ezdxf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.utils import ImageReader
import build_ford_exterior_v002 as base

ROAD_NAMES=('ROAD_OF_TOMORROW_REINFORCED_CONCRETE_SPIRAL','ROAD_OF_TOMORROW_MONOCORK_WEAR_LAYER','ROAD_INNER_CANTILEVER_CURB','ROAD_OUTER_CANTILEVER_CURB')
MATERIALS={k:trimesh.visual.material.PBRMaterial(name=k,**{x:v for x,v in b.items() if x in ('baseColorFactor','metallicFactor','roughnessFactor')}) for k,b in base.LOOKS.items()}

def normalized_mesh(vertices,faces):
    m=trimesh.Trimesh(vertices=np.asarray(vertices,dtype=float),faces=np.asarray(faces,dtype=int),process=True)
    if not m.is_watertight: raise ValueError('New structural mesh must be watertight')
    if m.volume<0: m.invert()
    if m.volume<=0: raise ValueError('Invalid structural mesh volume')
    return m

def road_strip(center,width,top_offset,thickness):
    """Closed, positive-volume ribbon; center Nx3, XY normal and top z from center."""
    p=np.asarray(center,dtype=float)
    if not np.isfinite(p).all() or len(p)<3 or width<=0 or thickness<=0: raise ValueError('Bad road input')
    derivatives=np.zeros_like(p[:,:2]); derivatives[1:-1]=p[2:,:2]-p[:-2,:2]
    derivatives[0]=p[1,:2]-p[0,:2];derivatives[-1]=p[-1,:2]-p[-2,:2]
    lengths=np.linalg.norm(derivatives,axis=1)
    if (lengths<1e-6).any(): raise ValueError('Degenerate path tangent')
    normal=np.stack([-derivatives[:,1]/lengths,derivatives[:,0]/lengths],axis=1)
    verts=[]
    for pt,n in zip(p,normal):
        for sign,z in [(-1,top_offset),(1,top_offset),(-1,top_offset-thickness),(1,top_offset-thickness)]:
            verts.append([pt[0]+sign*width/2*n[0],pt[1]+sign*width/2*n[1],pt[2]+z])
    faces=[]
    for i in range(len(p)-1):
        a=4*i;b=4*(i+1)
        for quad in ((a,a+1,b+1,b),(a+2,b+2,b+3,a+3),(a,a+2,b+2,b),(a+1,b+1,b+3,a+3)):
            u,v,w,x=quad;faces.extend(((u,v,w),(u,w,x)))
    # outer start/end closures
    for quad in ((0,2,3,1),(4*(len(p)-1),4*(len(p)-1)+1,4*(len(p)-1)+3,4*(len(p)-1)+2)):
        u,v,w,x=quad;faces.extend(((u,v,w),(u,w,x)))
    return normalized_mesh(verts,faces)

def cylinder_between(a,b,radius=0.1,sections=10):
    a=np.asarray(a,dtype=float);b=np.asarray(b,dtype=float)
    v=b-a
    if np.linalg.norm(v)<.01: raise ValueError('Zero length member')
    m=trimesh.creation.cylinder(radius=radius,segment=np.array([a,b]),sections=sections)
    if m.volume<0:m.invert()
    return m

def roof_ring(cx,cy,rx,ry,wall,rise,segments=96,radial=16):
    """Open center roof light with an ellipsoid-inspired stepped roof; no as-built claim."""
    vertices=[];faces=[];base_fraction=0.19;dt=0.32
    for j in range(2):
        for k in range(radial+1):
            u=k/radial;f=base_fraction+(1-base_fraction)*u
            z=wall+rise*(1-u*u)-j*dt
            for i in range(segments):
                a=math.tau*i/segments;vertices.append([cx+rx*f*math.cos(a),cy+ry*f*math.sin(a),z])
    idx=lambda side,k,i:side*(radial+1)*segments+k*segments+(i%segments)
    for side in range(2):
        for k in range(radial):
            for i in range(segments):
                q=(idx(side,k,i),idx(side,k+1,i),idx(side,k+1,i+1),idx(side,k,i+1))
                u,v,w,x=q;faces.extend(((u,v,w),(u,w,x)))
    for k in (0,radial):
        for i in range(segments):
            q=(idx(0,k,i),idx(0,k,i+1),idx(1,k,i+1),idx(1,k,i))
            u,v,w,x=q;faces.extend(((u,v,w),(u,w,x)))
    return normalized_mesh(vertices,faces)

def make_v003(params):
    scene,components=base.model(params,None)
    for part in ROAD_NAMES:
        scene.delete_geometry(part)
    components=[c for c in components if c['id'] not in ROAD_NAMES]
    def add(mesh,name,slot='roof_concrete',confidence='PROVISIONAL',source=None,parent=None):
        mesh.visual=trimesh.visual.TextureVisuals(material=MATERIALS[slot])
        scene.add_geometry(mesh,node_name=name,geom_name=name)
        components.append(dict(id=name,material_slot=slot,confidence=confidence,evidence_id=source,parent=parent))
    cx,cy=params['industrial_hall_center_xy_m']
    add(roof_ring(cx,cy,params['industrial_hall_outer_radius_x_m'],params['industrial_hall_outer_radius_y_m'],
                  params['industrial_hall_wall_height_m'],params['industrial_hall_roof_rise_m']),
                  'INDUSTRIAL_HALL_INTERPRETIVE_CLOSED_ROOF','roof_concrete','PHOTO_INSPIRED_ROOF_HYPOTHESIS')
    sx,sy=params['road_spiral_center_xy_m'];radius=params['road_centerline_radius_m']
    turns=params['road_turns'];N=841
    t=np.linspace(0,1,N);theta=math.tau*turns*t
    z0,z1=params['road_z_start_m'],params['road_z_end_m'];z=z0+(z1-z0)*t
    path=np.column_stack([sx+radius*np.cos(theta),sy+radius*np.sin(theta),z])
    w=params['road_travel_width_m'];thick=params['road_structural_deck_thickness_m'];curb=params['road_curb_height_m']
    def assemble_road(p,prefix,confidence):
        add(road_strip(p,w,0,thick),prefix+'_CONCRETE_CLOSED','roof_concrete',confidence,'AR38')
        add(road_strip(p,w-.26,.034,.034),prefix+'_MONOCORK_SURFACE','road_monocork',confidence,'MONOCORK')
        for side in [-1,1]:
            # Geometrically centered on the roadway edges; actual historic curb size unverified
            q=p.copy();d=np.zeros_like(q[:,:2]);d[1:-1]=q[2:,:2]-q[:-2,:2];d[0]=q[1,:2]-q[0,:2];d[-1]=q[-1,:2]-q[-2,:2]
            nn=np.stack([-d[:,1],d[:,0]],axis=1);nn/=np.linalg.norm(nn,axis=1)[:,None]
            q[:,:2]+=nn*side*(w/2-.11)
            add(road_strip(q,.21,curb,curb),prefix+f'_CURB_{side:+}','painted_facade',confidence,'THF_ROAD')
    assemble_road(path,'ROAD_THREE_TIER_SPIRAL','THREE_TIER_STRUCTURE_DOCUMENTED_PATH_UNREGISTERED')
    # Short transition roadways; TOTAL 804.672 m includes additional unmodeled bridges and paths.
    start=path[0];entry=np.column_stack([start[0]+np.zeros(140), np.linspace(start[1]-39,start[1],140),np.linspace(.65,start[2],140)])
    phi=math.tau*turns;ending=path[-1];tangent=np.array([-math.sin(phi),math.cos(phi)])
    outgoing=np.column_stack([ending[0]+np.linspace(0,48,140)*tangent[0],ending[1]+np.linspace(0,48,140)*tangent[1],np.linspace(ending[2],ending[2]+.35,140)])
    assemble_road(entry,'ROAD_ENTRANCE_LINK_INTERPRETIVE','UNVERIFIED_APPROACH_GEOMETRY')
    assemble_road(outgoing,'ROAD_UPPER_CONTINUATION_INTERPRETIVE','UNVERIFIED_UPPER_LINK_GEOMETRY')
    # Source: one inner ring of columns, but precise column count/height is an interpretive scaffold.
    radial_supports=params['road_column_count'];ring_r=params['road_inner_column_ring_radius_m'];beam_len=radius-ring_r+1.5
    for i in range(radial_supports):
        ang=math.tau*i/radial_supports
        uu=[(ang+math.tau*j)/(math.tau*turns) for j in range(math.ceil(turns))]
        uu=[u for u in uu if u<=1.0]
        levels=[z0+(z1-z0)*u-thick for u in uu]
        x=sx+ring_r*math.cos(ang);y=sy+ring_r*math.sin(ang)
        col_top=max(levels)-.12
        if col_top>.3:
            add(cylinder_between((x,y,-.2),(x,y,col_top),.46),f'ROAD_STRUCTURAL_COLUMN_{i:02d}','roof_concrete','COLUMN_GRID_UNMEASURED','AR38')
        # Inner radial brackets at each deck crossing, supported by columns
        for j,lev in enumerate(levels):
            b=(sx+(ring_r+beam_len)*math.cos(ang),sy+(ring_r+beam_len)*math.sin(ang),lev-.16)
            a=(x,y,lev-.16)
            add(cylinder_between(a,b,.23),f'ROAD_CANTILEVER_BEAM_{i:02d}_{j:02d}','roof_concrete','RING_SUPPORT_CONCEPT_DOC_GRID_ESTIMATE','AR38')
    # Documented movable exhibit, not animating visitor floor or surrounding water.
    animation={'parent_id':'FORD39_CYCLE_OF_PRODUCTION','axis':'Z','pivot_local_m':[cx,cy,0],
               'rpm':None,'status':'NOT_MEASURED','child_mesh_ids':[x['id'] for x in components if x['id'].startswith('FORD_CYCLE_TIER_')],
               'formula':'theta_radians = theta_0 + (2*pi*rpm/60)*t_seconds'}
    return scene,components,dict(road_points=path.tolist(),entry_points=entry.tolist(),outgoing_points=outgoing.tolist(),
        spiral_ground_length_m=float(np.sum(np.linalg.norm(np.diff(path[:,:2],axis=0),axis=1))),
        spiral_slope_pct=100*(z1-z0)/(math.tau*radius*turns),
        animation=animation,spiral_3d_length_m=float(np.sum(np.linalg.norm(np.diff(path,axis=0),axis=1))))

def dxf_sheet(out,p,road_data):
    doc=ezdxf.new('R2010');doc.header['$INSUNITS']=6;ms=doc.modelspace()
    layers={'DOCUMENTED':4,'INTERPRETIVE_SHELL':30,'ROAD_CONCEPT':8,'STRUCTURE_CONCEPT':3,'EXHIBIT':5,'NOTES':7}
    for name,color in layers.items():doc.layers.new(name,dxfattribs={'color':color})
    cx,cy=p['industrial_hall_center_xy_m'];rx=p['industrial_hall_outer_radius_x_m'];ry=p['industrial_hall_outer_radius_y_m']
    ms.add_ellipse((cx,cy), (rx,0),ratio=ry/rx,dxfattribs={'layer':'INTERPRETIVE_SHELL'})
    ms.add_circle((cx,cy),p['turntable_diameter_m']/2,dxfattribs={'layer':'DOCUMENTED'})
    ms.add_circle((cx,cy),p['water_outer_radius_m'],dxfattribs={'layer':'EXHIBIT'})
    ex,ey=p['entrance_hall_center_xy_m'];ew=p['entrance_hall_width_m'];ed=p['entrance_hall_depth_m']
    ms.add_lwpolyline([(ex-ew/2,ey-ed/2),(ex+ew/2,ey-ed/2),(ex+ew/2,ey+ed/2),(ex-ew/2,ey+ed/2)],close=True,dxfattribs={'layer':'INTERPRETIVE_SHELL'})
    for key in ('road_points','entry_points','outgoing_points'):
        ms.add_lwpolyline([(x,y) for x,y,z in road_data[key]],dxfattribs={'layer':'ROAD_CONCEPT'})
    sx,sy=p['road_spiral_center_xy_m']
    for i in range(p['road_column_count']):
        a=math.tau*i/p['road_column_count'];r=p['road_inner_column_ring_radius_m']
        ms.add_circle((sx+r*math.cos(a),sy+r*math.sin(a)),.46,dxfattribs={'layer':'STRUCTURE_CONCEPT'})
    ms.add_text('FORD 1939 SCHEMATIC - UNSURVEYED - SITE POSITION NOT VERIFIED',dxfattribs={'layer':'NOTES','height':1.5,'insert':(-130,-100)})
    name=out/'A103_Ford_1939_Exterior_Structure_Plan_v003.dxf';doc.saveas(name)
    audit=ezdxf.readfile(name).audit()
    if audit.has_errors:raise ValueError('DXF audit errors: '+str(len(audit.errors)))
    return name,len(ms)

def illustrations(out,p,dat):
    cx,cy=p['industrial_hall_center_xy_m'];rx=p['industrial_hall_outer_radius_x_m'];ry=p['industrial_hall_outer_radius_y_m']
    fig,ax=plt.subplots(figsize=(13.2,8.3),dpi=150)
    ax.set_aspect('equal');ax.set_facecolor('#f5f7f5');a=np.linspace(0,math.tau,240)
    ax.plot(cx+rx*np.cos(a),cy+ry*np.sin(a),color='#a2743f',lw=3,label='Hall exterior: interpreted')
    ax.add_patch(Circle((cx,cy),p['turntable_diameter_m']/2,fill=False,color='#197e9d',lw=3,label='Exhibit diameter: source'))
    ax.add_patch(Circle((cx,cy),p['water_outer_radius_m'],fill=False,color='#75aab6',lw=2,label='Basin: interpreted'))
    for key,col,lw in [('road_points','#707781',3),('entry_points','#b6864b',2),('outgoing_points','#b6864b',2)]:
        arr=np.array(dat[key]);ax.plot(arr[:,0],arr[:,1],color=col,lw=lw,alpha=.84)
    sx,sy=p['road_spiral_center_xy_m']
    for i in range(p['road_column_count']):
        ang=math.tau*i/p['road_column_count'];r=p['road_inner_column_ring_radius_m']
        ax.plot(sx+r*math.cos(ang),sy+r*math.sin(ang),'o',color='#9b5b48',ms=4)
    ex,ey=p['entrance_hall_center_xy_m'];ew=p['entrance_hall_width_m'];ed=p['entrance_hall_depth_m']
    ax.add_patch(Rectangle((ex-ew/2,ey-ed/2),ew,ed,fill=False,edgecolor='#a2743f',lw=2.5))
    ax.text(cx,cy,'ROTATING\nCYCLE',ha='center',va='center',fontsize=9,weight='bold',color='#197e9d')
    ax.text(sx,sy,'INNER\nCOLUMN RING',ha='center',va='center',fontsize=8)
    ax.text(ex,ey,'ENTRANCE',ha='center',va='center',fontsize=9)
    ax.legend(loc='upper left',fontsize=9);ax.grid(alpha=.15);ax.set_xlim(-135,135);ax.set_ylim(-100,83)
    ax.set(title='FORD EXPOSITION 1939 | FLOORPLAN AND RAMP SUPPORTS • SCHEMATIC v003',xlabel='Diagram-local eastings, metres (unregistered)',ylabel='Diagram-local northings, metres (unregistered)')
    ax.text(.03,.02,'No Ford pavilion footprint, elevation, or ramp curvature has been surveyed.\nBlue = sourced 100-ft Cycle diameter. All brown/gray and support points are adjustable.',transform=ax.transAxes,fontsize=9,bbox=dict(facecolor='white',alpha=.9,edgecolor='none'))
    fig.tight_layout();fp=out/'A103_Ford_Structural_Plan_v003.png';fig.savefig(fp);plt.close(fig)
    arr=np.array(dat['road_points']);fig,ax=plt.subplots(figsize=(13.2,5.6),dpi=155)
    x=np.linspace(0,dat['spiral_3d_length_m'],len(arr));ax.plot(x,arr[:,2],lw=8,color='#738894')
    ax.plot(x,arr[:,2]-.44,lw=2,color='#a06d50');ax.set(xlabel='Cumulative ramp travel in model, metres',ylabel='Illustrative roadway elevation, metres',title='FORD ROAD | RISE / MULTI-TURN SUPPORTS • CONCEPT v003')
    ax.grid(alpha=.18)
    for j in range(1,3):ax.axvline(x[-1]*j/p['road_turns'],ls=':',color='#ac8559')
    ax.text(.02,.86,'Inner column-ring supports and radial beams repeated at EACH deck crossing.\nUnregistered pitch, turns, beam dimensions and elevations remain assumptions.',transform=ax.transAxes,fontsize=11,bbox=dict(facecolor='white',alpha=.87,edgecolor='none'))
    ax.text(.02,.12,f"Modeled spiral length {dat['spiral_3d_length_m']:.1f} m; grade {dat['spiral_slope_pct']:.2f}%  |  Full advertised ride 804.672 m",transform=ax.transAxes,fontsize=10)
    fig.tight_layout();sp=out/'A303_Ford_Road_Support_Section_v003.png';fig.savefig(sp);plt.close(fig)
    return fp,sp

def report(out,imgs,params,dat,qa):
    dest=out/'Ford_1939_Exterior_Road_Production_Sheets_v003.pdf'
    c=pdf_canvas.Canvas(str(dest),pagesize=(1080,720))
    c.setTitle('FMP Ford Exposition 1939 - Exterior and Road 003')
    for i,(title,path) in enumerate(zip(['A103 - PLAN & SUPPORT LAYOUT','A303 - ROAD ELEVATION / CANTILEVER SCHEME'],imgs)):
        c.setFillColorRGB(.08,.16,.19);c.rect(0,0,1080,720,fill=1,stroke=0)
        c.setFillColorRGB(.95,.96,.93);c.setFont('Helvetica-Bold',20);c.drawString(35,675,'FORD 1939  /  '+title)
        c.drawImage(ImageReader(str(path)),30,110,width=1020,height=540,preserveAspectRatio=True,anchor='c')
        c.setFillColorRGB(.90,.91,.90);c.setFont('Helvetica',11)
        c.drawString(35,65,'FMP research reconstruction  |  NO HISTORIC FOOTPRINT CERTIFIED  |  Refer to archived Ford site drawings before final placement')
        c.setFont('Helvetica',9);c.drawRightString(1035,30,f'FMP-WF0014  |  SHEET {i+1:02d} / 03')
        c.showPage()
    c.setFillColorRGB(.08,.16,.19);c.rect(0,0,1080,720,fill=1,stroke=0)
    c.setFillColorRGB(.92,.95,.92);c.setFont('Helvetica-Bold',23);c.drawString(50,665,'FORD 1939 | SOURCE, MATH & PRODUCTION QA')
    docs=[
      ('DOCUMENTED',f"Cycle of Production turntable: 100 ft / {params['turntable_diameter_m']:.2f} m diameter."),
      ('DOCUMENTED','Ford Cycle: 87 working models, 142 animated figures, 27 raw materials (museum catalog).'),
      ('DOCUMENTED','Road of Tomorrow: cantilevered reinforced-concrete three-tier spiral; inner ring of columns.'),
      ('DOCUMENTED','Full automobile route approximately 1/2 mile = 804.672 m; not all on the spiral.'),
      ('DOCUMENTED','Turntable 150 tons (Henry Ford catalog photo title); equipment specification not obtained.'),
      ('MODELED',f"Three-dimensional spiral length: {dat['spiral_3d_length_m']:.1f} m, slope {dat['spiral_slope_pct']:.2f}% (not surveyed)."),
      ('MODELED',f"Support columns: {params['road_column_count']} assumed, with beams under all spiral traversals."),
      ('UNVERIFIED','Outer hall dimensions, ramp turns, road links, basin radius, roof form, materials and grade.'),
      ('UNVERIFIED','Full 1939 Ford pavilion site placement and exact circulation and accessible thresholds.'),
      ('QA',f"GLB: {qa['geometry_count']} mesh parts, finite coordinates and {qa['new_structural_meshes_watertight']} closed new structural meshes."),
      ('QA',f"DXF: {qa['dxf_entities']} entities; ezdxf audit {qa['dxf_errors']} errors."),
      ('SOURCE','Architectural Record 1938-11  |  The Henry Ford collections  |  LancasterHistory Monocork.'),
    ]
    y=605
    for tag,body in docs:
        c.setFont('Helvetica-Bold',12);c.setFillColorRGB(.31,.78,.78 if tag=='DOCUMENTED' else .58);c.drawString(52,y,tag)
        c.setFont('Helvetica',12);c.setFillColorRGB(.94,.95,.94);c.drawString(170,y,body[:122]);y-=43
    c.showPage();c.save();return dest

def main():
    arg=argparse.ArgumentParser();arg.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent);args=arg.parse_args()
    out=args.output_dir;out.mkdir(parents=True,exist_ok=True);p=copy.deepcopy(base.DEFAULTS)
    scene,components,calc=make_v003(p)
    glb=out/'Ford_1939_Exterior_Road_Production_v003.glb';scene.export(str(glb))
    loaded=trimesh.load(str(glb),force='scene')
    newparts=[n for n in loaded.geometry if n.startswith(('ROAD_THREE_TIER','ROAD_ENTRANCE','ROAD_UPPER','ROAD_STRUCTURAL','ROAD_CANTILEVER','INDUSTRIAL_HALL_INTERPRETIVE_CLOSED_ROOF'))]
    bad=[n for n in newparts if not loaded.geometry[n].is_watertight]
    if bad:raise AssertionError('Unclosed v003 meshes: '+str(bad[:5]))
    if len(loaded.geometry)!=len(components):raise AssertionError('GLB export component mismatch')
    if any(not np.isfinite(mesh.vertices).all() for mesh in loaded.geometry.values()):raise AssertionError('invalid coordinate')
    if calc['spiral_3d_length_m'] >= p['period_half_mile_car_route_m']:raise AssertionError('spiral longer than entire ride')
    doc,count=dxf_sheet(out,p,calc);img1,img2=illustrations(out,p,calc)
    qa=dict(status='PASS_SYNTHETIC_STRUCTURAL_QA',geometry_count=len(loaded.geometry),new_structural_meshes_watertight=len(newparts),
            dxf_entities=count,dxf_errors=0,glb_sha256=hashlib.sha256(glb.read_bytes()).hexdigest(),
            historic_geo_certified=False,collision_engine_tested=False,unreal_tested=False,
            reported_turntable_mass_tons=150,ton_unit_unresolved=True,turntable_inertia_unresolved=True,
            game_ready=False,source_image_traces_unavailable=True)
    spec=dict(schema='fmp.wf0014.exterior-road.v003',building_id='WF0014',historic_year=1939,parameters=p,
              qa=qa,road_math={k:v for k,v in calc.items() if k not in ('road_points','entry_points','outgoing_points')},
              source_references=dict(base.SOURCES,THF_TURNTABLE='https://www.thehenryford.org/collections/explore/artifact/77707'),
              editable_policy='Historical 100-ft diameter and source counts fixed; all other geometric sizes are inference and not surveyed',
              provenance={'documented':list(base.DOCUMENTED),'interpretive':'All site XY, plan envelopes, architecture roof and road support count'},
              cinematic_materials=base.LOOKS,mesh_component_count=len(components),
              viewer_ready=False,native_host_tested=False)
    (out/'Ford_1939_Exterior_Road_Manifest_v003.json').write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n')
    report(out,(img1,img2),p,calc,qa)
    print(json.dumps({**qa,'spiral_length_m':calc['spiral_3d_length_m'],'road_slope_percent':calc['spiral_slope_pct']},indent=2))
if __name__=='__main__':main()
