#!/usr/bin/env python3
"""FMP: audit an EXISTING GLB against dated, independently sourced constraints.
Does not rebuild, georeference or change source geometry. Python 3.10+.
Requires trimesh/numpy; matplotlib only for visual projection drawings.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
import trimesh

def bounds(scene, name):
    xform, mesh_id=scene.graph[name]
    if mesh_id is None:
        return None
    mesh=scene.geometry[mesh_id]
    pts=trimesh.transform_points(mesh.vertices, xform)
    lo,hi=pts.min(axis=0),pts.max(axis=0)
    return {'min':lo.tolist(),'max':hi.tolist(),
            'size':(hi-lo).tolist(),'faces':len(mesh.faces),
            'watertight':bool(mesh.is_watertight)}

def component_id(scene, name, assembly_id):
    if assembly_id != 'FMP_THEME_CENTER_1939':
        return assembly_id  # General building: no guessed subassembly ownership.
    n=name
    while n and n!='world':
        if 'DEMOCRACITY' in n.upper():return 'WF0003'
        n=scene.graph.transforms.parents.get(n)
    low=name.lower()
    if low.startswith(('trylon_','escalator_','platform_1_landing','platform_2_landing')) or 'trylon_entry' in low:
        return 'WF0001'
    if low.startswith(('perisphere_','meridian_','latitude_','moving_platform_',
                        'platform_1_parapet','platform_2_parapet')):
        return 'WF0002'
    if low.startswith('helicline_') or 'helicline_terminus' in low:return 'WF0004'
    if low.startswith('return_bridge'):return 'FMP_THEME_CENTER_BRIDGE'
    if name.startswith('90_') or 'pool' in low or 'fairapproach' in low:return 'WF0005'
    return 'UNCLASSIFIED_REVIEW'

def measure(scene, constraint, node_index):
    axis=constraint.get('audit_axis')
    key=constraint['component']
    if axis=='count_matching_nodes':
        names=scene.graph.nodes
        if key=='Moving_Platform_':
            return sum(n in ('Moving_Platform_1','Moving_Platform_2') for n in names)
        if key=='Escalator_':
            return sum(n.startswith('Escalator_') and n.endswith('_Envelope') for n in names)
        return sum(n.startswith(key) for n in names)
    if axis in ('height_y','bbox_ymin') and key in node_index:
        b=node_index[key]
        if b is None:return None
        return b['size'][1] if axis=='height_y' else b['min'][1]
    if axis=='combined_sphere_diameter_x':
        a=node_index.get('Perisphere_Upper_Removable_Shell')
        b=node_index.get('Perisphere_Lower_Removable_Shell')
        if a and b:
            return max(a['max'][0],b['max'][0])-min(a['min'][0],b['min'][0])
    return None

def draw_sheets(scene, output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from scipy.spatial import ConvexHull
    names=scene.graph.nodes
    fig,(plan,elev)=plt.subplots(1,2,figsize=(14,7),layout='constrained')
    for label,part in [('Trylon','Trylon_Hollow_Exterior'),
                       ('Perisphere','Perisphere_Upper_Removable_Shell'),
                       ('Helicline','Helicline_Deck_and_Curved_Soffit'),
                       ('Bridge','Return_Bridge_Deck')]:
        if part not in names:continue
        transform,mesh_name=scene.graph[part]
        points=trimesh.transform_points(scene.geometry[mesh_name].vertices,transform)
        sampled=points[::max(1,len(points)//3000)]
        if label=='Perisphere' and 'Perisphere_Lower_Removable_Shell' in names:
            t,g=scene.graph['Perisphere_Lower_Removable_Shell']
            p2=trimesh.transform_points(scene.geometry[g].vertices,t)
            sampled=np.vstack((sampled,p2[::max(1,len(p2)//3000)]))
        for ax,projection in ((plan,sampled[:,[0,2]]),(elev,sampled[:,[0,1]])):
            if label in ('Trylon','Perisphere'):
                hull=ConvexHull(projection)
                poly=projection[list(hull.vertices)+[hull.vertices[0]]]
                ax.plot(poly[:,0],poly[:,1],linewidth=1.6,label=label)
            else:
                ax.plot(projection[:,0],projection[:,1],'.',ms=.6,label=label)
    plan.set_title('A101 | Source GLB plan projection (X/Z)')
    elev.set_title('A201 | Source GLB elevation (X/Y)')
    plan.set_ylabel('Model-local Z (m)')
    elev.set_ylabel('Height Y (m)')
    for ax in (plan,elev):
        ax.set_aspect('equal',adjustable='datalim')
        ax.set_xlabel('Model-local X (m)')
        ax.grid(alpha=.15)
        ax.legend(loc='best',fontsize=8)
    fig.suptitle('FMP • EXISTING GEOMETRY • NOT SITE-REGISTERED OR AS-BUILT CERTIFIED')
    for ext in ('png','svg'):
        fig.savefig(output/('projection.'+ext),dpi=160)
    plt.close(fig)

def audit(model_path, profile_path, output, drawings=True):
    model_path=Path(model_path);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    profile=json.loads(Path(profile_path).read_text(encoding='utf-8'))
    if profile.get('schema')!='fmp.architecture.constraints.v1':
        raise ValueError('Invalid architectural constraint schema')
    source_hash=hashlib.sha256(model_path.read_bytes()).hexdigest()
    trusted_hash=profile.get('base_model',{}).get('sha256')
    if trusted_hash and source_hash!=trusted_hash:
        raise ValueError('Source GLB bytes differ from the reviewed release; refuse stale node assumptions')
    scene=trimesh.load(model_path,force='scene')
    rows=[];index={};groups={}
    for name in sorted(scene.graph.nodes):
        bbox=bounds(scene,name);group=component_id(scene,name,profile['assembly_id'])
        index[name]=bbox;groups[group]=groups.get(group,0)+1
        rows.append([name,group,scene.graph.transforms.parents.get(name),
                     '' if bbox is None else json.dumps(bbox['min']),
                     '' if bbox is None else json.dumps(bbox['max']),
                     '' if bbox is None else bbox['watertight'],
                     '' if bbox is None else bbox['faces'],
                     'REVIEW' if group=='UNCLASSIFIED_REVIEW' else 'EXISTING_UNCERTIFIED'])
    with (output/'node_register.csv').open('w',newline='',encoding='utf-8') as stream:
        w=csv.writer(stream);w.writerow(['node','place_id','parent','min_xyz_m','max_xyz_m','closed','faces','status']);w.writerows(rows)
    checks=[]
    for item in profile['constraints']:
        observed=measure(scene,item,index);target=item.get('si_value')
        if observed is None:
            status='NOT_VERIFIABLE_BY_MESH_BOUNDING_CHECK'
        else:
            tol=item.get('tolerance_m')
            tol=0.0 if tol is None else tol
            status='MODEL_NUMERIC_PASS_NOT_CERTIFIED' if abs(float(observed)-float(target))<=tol else 'MODEL_NUMERIC_FAIL'
        checks.append({'id':item['id'],'place_id':item['place_id'],'key':item['key'],
                       'measured_source_si':target,'model_measured_si':observed,
                       'status':status,'evidence_status':item['evidence_status'],
                       'source':item['source']})
    with (output/'dimension_checks.csv').open('w',newline='',encoding='utf-8') as stream:
        w=csv.DictWriter(stream,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)
    report={'schema':'fmp.scene-audit.v1','asset':str(model_path.name),
            'model_sha256':source_hash,'nodes':len(scene.graph.nodes),
            'geometry_assets':len(scene.geometry),'units':'metres','up_axis':'Y',
            'group_counts':groups,'checks':checks,'history_proposals':profile.get('rejected_as_built'),
            'unresolved':profile.get('unresolved'),
            'site_registered':False,'historically_certified':False,
            'warning':'Numerical pass validates the current model only, not historical correctness.'}
    (output/'audit.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    if drawings:draw_sheets(scene,output)
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--model',required=True)
    ap.add_argument('--constraints',required=True)
    ap.add_argument('--out',required=True)
    ap.add_argument('--no-drawings',action='store_true')
    args=ap.parse_args()
    result=audit(args.model,args.constraints,args.out,not args.no_drawings)
    print('Audited',result['nodes'],'existing nodes;',
          sum(x['status']=='MODEL_NUMERIC_PASS_NOT_CERTIFIED' for x in result['checks']),
          'direct model checks passed')
