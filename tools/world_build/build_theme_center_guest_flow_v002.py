#!/usr/bin/env python3
"""FMP v002: source-preserving Theme Center portals, handrails and alignment.

Inputs: vetted 510-node source GLB, metres/Y-up. Output: separate runtime-only
open-shell overlay + watertight CAD cutters (NOT applied to printable shells).
All exit portal/headroom/stair details are INTERPRETIVE, not 1939 as-built.
Usage: python3 tools/world_build/build_theme_center_guest_flow_v002.py SOURCE.glb OUT_DIR
"""
from __future__ import annotations
import hashlib,json,math,sys,tempfile
from pathlib import Path
import numpy as np
import trimesh

try:
    from tools.world_build.build_theme_center_guest_flow_v001 import generate,SOURCE_SHA
except ImportError:
    from build_theme_center_guest_flow_v001 import generate,SOURCE_SHA

BLUE=(157,184,202,255)
GOLD=(196,166,103,255)

def source_mesh(scene,node):
    T,g=scene.graph[node]
    m=scene.geometry[g].copy()
    m.apply_transform(T)
    return m

def add_box(scene,name,pos,dims,color):
    mesh=trimesh.creation.box(extents=dims)
    mesh.apply_translation(pos)
    mesh.visual.face_colors=color
    scene.add_geometry(mesh,node_name=name,geom_name=name)

def add_rail(scene,name,a,b,diameter=.065):
    a,b=np.asarray(a,float),np.asarray(b,float)
    vector=b-a
    length=float(np.linalg.norm(vector))
    if length<1e-3:raise ValueError("Degenerate handrail")
    mesh=trimesh.creation.cylinder(radius=diameter/2,height=length,sections=12)
    mesh.apply_transform(trimesh.geometry.align_vectors([0,0,1],vector/length))
    mesh.apply_translation((a+b)/2)
    mesh.visual.face_colors=BLUE
    scene.add_geometry(mesh,node_name=name,geom_name=name)

def surface_x(y,z,cy=32.6136,r=27.432):
    residual=r*r-(y-cy)**2-z*z
    if residual<=0:raise ValueError("Opening beyond modeled sphere")
    return -math.sqrt(residual)

def generate_v002(source:Path,out:Path,print_scales=(250,800)):
    source,out=Path(source),Path(out)
    out.mkdir(parents=True,exist_ok=True)
    original_sha=hashlib.sha256(source.read_bytes()).hexdigest()
    if original_sha!=SOURCE_SHA:
        raise ValueError("Unknown original Theme Center source hash")
    scene=trimesh.load(source,force="scene")
    required=("Trylon_Hollow_Exterior","Perisphere_Upper_Removable_Shell",
      "Perisphere_Lower_Removable_Shell","Platform_1_Landing_Hypothesis",
      "Platform_2_Landing_Hypothesis","Return_Bridge_Deck",
      "Helicline_Deck_and_Curved_Soffit")
    missing=set(required)-set(scene.graph.nodes)
    if missing:raise ValueError("Source nodes missing: "+str(sorted(missing)))

    with tempfile.TemporaryDirectory(prefix="fmp_tc_v001_") as temp:
        v1=generate(source,Path(temp))
        runtime=trimesh.load(Path(temp)/v1["unreal_overlay"],force="scene")
    added=[]
    def box(name,pos,size):
        add_box(runtime,name,pos,size,GOLD)
        added.append(name)
    def rail(name,a,b,diameter=.065):
        add_rail(runtime,name,a,b,diameter=diameter)
        added.append(name)

    lower=source_mesh(scene,"Platform_1_Landing_Hypothesis").bounds.mean(axis=0)
    upper=source_mesh(scene,"Platform_2_Landing_Hypothesis").bounds.mean(axis=0)
    bridge=source_mesh(scene,"Return_Bridge_Deck").bounds.mean(axis=0)
    lower[1]=source_mesh(scene,"Platform_1_Landing_Hypothesis").bounds[1,1]
    upper[1]=source_mesh(scene,"Platform_2_Landing_Hypothesis").bounds[1,1]
    bridge[1]=source_mesh(scene,"Return_Bridge_Deck").bounds[1,1]
    cutters=trimesh.Scene()
    portals=[]
    for tag,point in (("LOWER",lower),("UPPER",upper)):
        landing_name="Platform_1_Landing_Hypothesis" if tag=="LOWER" else "Platform_2_Landing_Hypothesis"
        floor_y=float(source_mesh(scene,landing_name).bounds[1,1])
        y,z=floor_y+1.2,float(point[2])
        width,height,t=2.35,2.4,.15
        xx=surface_x(y,z)
        x=xx+.08
        for side,side_offset in (("N",-1),("S",1)):
            box("INTERPRETIVE_"+tag+"_PORTAL_JAMB_"+side,
                (x,y,z+side_offset*(width+t)/2),(.22,height+t,t))
        box("INTERPRETIVE_"+tag+"_PORTAL_HEAD",
            (x,y+(height+t)/2,z),(.22,t,width+2*t))
        box("INTERPRETIVE_"+tag+"_PORTAL_SILL_GUIDE",
            (x,y-height/2-.03,z),(.22,.06,width+2*t))
        cutter=trimesh.creation.box(extents=(7.5,height,width))
        cutter.apply_translation((xx,y,z))
        cutters.add_geometry(cutter,node_name="CAD_ONLY_BOOLEAN_CUTTER_"+tag)
        portals.append({"id":"WF0002-1939-"+tag+"-EXIT",
            "center_model_m":[xx,y,z],"width_m":width,"height_m":height,
            "floor_y_model_m":floor_y,"floor_source_node":landing_name,
            "historical_status":"INTERPRETIVE_GEOMETRY",
            "source_node":"Perisphere_Lower_Removable_Shell"})

    start=np.array([-24.70,upper[1],upper[2]],float)
    finish=np.array([-30.25,bridge[1],bridge[2]],float)
    direction=finish-start
    direction[1]=0
    direction/=np.linalg.norm(direction)
    across=np.array([-direction[2],0,direction[0]])
    rail_lines=[]
    for side,sgn in (("L",-1),("R",1)):
        offset=across*sgn*1.85/2
        a=start+offset+[0,1.0,0]
        b=finish+offset+[0,1.0,0]
        rail("INTERPRETIVE_UPPER_EXIT_HANDRAIL_"+side,a,b)
        for j,t in enumerate(np.linspace(0,1,9)):
            point=start*(1-t)+finish*t+offset
            rail("INTERPRETIVE_UPPER_EXIT_POST_"+side+"_%02d"%j,
                point,point+np.array([0,1.0,0]),diameter=.045)
        rail_lines.append([a.tolist(),b.tolist()])

    helix=source_mesh(scene,"Helicline_Deck_and_Curved_Soffit")
    target=np.array([-32.5,float(bridge[1]),-9.5],float)
    distance=np.linalg.norm(helix.vertices-target,axis=1)
    nearest=helix.vertices[int(np.argmin(distance))]
    points=[
      ("TP-1939-LOWER_EXIT","PERISPHERE_LOWER_EXIT",lower),
      ("TP-1939-UPPER_EXIT","PERISPHERE_UPPER_EXIT",upper),
      ("TP-1939-RETURN_BRIDGE","RETURN_BRIDGE",bridge),
      ("TP-1939-HELICLINE_START","HELICLINE_TOP_MODEL_VERTEX",nearest)]
    interactions=[]
    for identifier,role,coord in points:
        p=np.asarray(coord,float)
        interactions.append({"id":identifier,"building_id":"WF0002",
           "period_year":1939,"role":role,
           "xyz_glb_y_up_m":np.around(p,6).tolist(),
           "xyz_unreal_z_up_cm":np.around(p[[0,2,1]]*100,4).tolist(),
           "status":"PROVISIONAL_MODEL_LOCAL_NOT_HISTORICALLY_REGISTERED",
           "interactive_qa":"UNREAL_NOT_TESTED"})

    runtime_file=out/"ThemeCenter_1939_GuestFlow_Trim_v002_r2.glb"
    cutter_file=out/"ThemeCenter_1939_CAD_PortalCutters_v002_r2.glb"
    runtime_file.write_bytes(runtime.export(file_type="glb"))
    cutter_file.write_bytes(cutters.export(file_type="glb"))
    tested_runtime=trimesh.load(runtime_file,force="scene")
    tested_cutters=trimesh.load(cutter_file,force="scene")
    if not all(k in tested_runtime.graph.nodes for k in added):
        raise RuntimeError("Missing expected overlay mesh")
    if len(tested_cutters.geometry)!=2 or not all(x.is_watertight for x in tested_cutters.geometry.values()):
        raise RuntimeError("Portal cutters are not closed")

    print_dims={}
    for label,names in (("Trylon",("Trylon_Hollow_Exterior",)),
                        ("Perisphere",("Perisphere_Upper_Removable_Shell",
                                      "Perisphere_Lower_Removable_Shell"))):
        solids=[source_mesh(scene,name) for name in names]
        lo=np.min([m.bounds[0] for m in solids],axis=0)
        hi=np.max([m.bounds[1] for m in solids],axis=0)
        dims=(hi-lo)*1000
        print_dims[label]={str(n):{"envelope_mm":np.around(dims/n,3).tolist(),
            "min_wall_checked":False,"physical_fit_checked":False} for n in print_scales}
    qa={"source_sha256":original_sha,
      "source_unchanged":original_sha==hashlib.sha256(source.read_bytes()).hexdigest(),
      "runtime_nodes":len(tested_runtime.graph.nodes),
      "added_nodes":len(added),"door_frames":len(portals),
      "solid_print_guides":len(tested_cutters.geometry),
      "helicline_nearest_vertex_error_m":float(np.min(distance)),
      "helicline_proximity_limit_m":0.1,
      "helicline_proximity_pass":bool(np.min(distance)<0.1),
      "helicline_join_acceptance":"OPEN_REQUIRES_SURFACE_AND_BODY_CLEARANCE_CHECK",
      "helicline_target_reference_m":target.tolist(),
      "helix_actual_vertex_m":nearest.tolist(),
      "cannot_certify_navigation":True}
    report={"schema":"fmp.theme-center-guest-flow.v002",
      "geometry_revision":"r2_walking_surface_alignment",
      "source_glb":source.name,"source_hash_sha256":original_sha,
      "building_ids":["WF0001","WF0002"],"related_places":["WF0003","WF0004"],
      "years":[1939],"assembly_geometry":"original source, separate runtime-only overlay",
      "output_runtime_glb":runtime_file.name,
      "output_cad_boolean_guides":cutter_file.name,
      "model_coordinate_frame":"RIGHT_HANDED_Y_UP_METERS_NOT_GEOREGISTERED",
      "unreal_preview_conversion":"[x,z,y] * 100cm; handedness reversal; validate normals and winding",
      "portals":portals,"guiderails":rail_lines,
      "interaction_candidates":interactions,
      "portal_cad_cutters":"UNAPPLIED solid cutter guides; no watertight Boolean result",
      "preserves_source_print_parts":["Trylon_Hollow_Exterior",
        "Perisphere_Upper_Removable_Shell","Perisphere_Lower_Removable_Shell"],
      "print_envelopes":print_dims,"qa":qa,
      "confidence":{"building_outer_shell":"SOURCE_MODEL_MESH",
        "visitor_levels":"INHERITED_MODEL_PROVISIONAL",
        "portal_frames_and_stairs":"INTERPRETIVE_NOT_AS_BUILT",
        "helicline_top_join":"MODEL_VERTEX_PROXIMITY_ONLY"},
      "unreal_native_collision":"NOT_TESTED","print_booleans":"NOT_APPLIED",
      "acceptance_gates":[
       "Trace final period opening, bridge and stair drawings",
       "Site-registration survey and fairground origin",
       "Unreal capsule, navigation, threshold and stair collision tests",
       "Printable duplicated-shell Boolean, closed rims and wall-thickness QA",
       "Physical projection/print alignment independent of visitor scene"]}
    (out/"ThemeCenter_1939_GuestFlow_Contract_v002_r2.json").write_text(
      json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report

if __name__=="__main__":
    if len(sys.argv)!=3:raise SystemExit(__doc__)
    print(json.dumps(generate_v002(Path(sys.argv[1]),Path(sys.argv[2]))["qa"],indent=2))

