"""Runtime topology test of shared apertures. Not historical/structural approval."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
import trimesh
from tools.world_build.audit_helicline_join import world_mesh,SOURCE_SHA
from tools.world_build.audit_transition_clearance import OVERLAY_SHA

REPLACED=('Trylon_Face_3_Frame','Trylon_Hollow_Exterior','Helicline_Rail_-1')

def build(source,previous,out):
    source,previous,out=Path(source),Path(previous),Path(out)
    if hashlib.sha256(source.read_bytes()).hexdigest()!=SOURCE_SHA:raise ValueError('Unknown source')
    if hashlib.sha256(previous.read_bytes()).hexdigest()!=OVERLAY_SHA:raise ValueError('Unknown v003 overlay')
    out.mkdir(parents=True,exist_ok=True)
    original=trimesh.load(source,force='scene');runtime=trimesh.load(previous,force='scene')
    floor=float(world_mesh(original,'Return_Bridge_Deck').bounds[1,1])
    deck_z=float(world_mesh(original,'Return_Bridge_Deck').bounds[:,2].mean())
    apertures=[];cutters=[]
    for name,z in [('TRYLON_RETURN_ENTRY',deck_z),('TRYLON_RETURN_EXIT',-3.15)]:
        center=[-36.7,floor+1.2,z];size=[3.4,2.4,2.4]
        cut=trimesh.creation.box(extents=size);cut.apply_translation(center);cutters.append(cut)
        apertures.append({'id':name,'center_xyz_m':center,'size_xyz_m':size,
          'status':'PREVIEW_ONLY_TOPOLOGY_TEST_NOT_HISTORICAL_DIMENSIONS'})
    changes=[]
    for name in REPLACED:
        m=world_mesh(original,name);parts=m.split(only_watertight=False);output=[];count=0
        for part in parts:
            active=[c for c in cutters if np.all(part.bounds[1]>=c.bounds[0]) and np.all(part.bounds[0]<=c.bounds[1])]
            if not active:output.append(part);continue
            if not part.is_watertight:raise ValueError('Nonclosed source component: '+name)
            result=part
            for cutter in active:
                result=trimesh.boolean.difference([result,cutter],engine='manifold',check_volume=True)
                if result.is_empty:break
            if not result.is_empty:
                if not result.is_watertight:raise ValueError('Nonclosed cut result: '+name)
                output.append(result)
            count+=1
        replacement=trimesh.util.concatenate(output)
        replacement.visual.face_colors=[175,180,185,255]
        node=name+'__RUNTIME_SHARED_APERTURES_v004'
        runtime.add_geometry(replacement,node_name=node,geom_name=node)
        changes.append({'source_node':name,'replacement_node':node,'source_parts':len(parts),
                        'candidate_cut_parts':count,'source_volume_m3':float(m.volume),
                        'replacement_volume_m3':float(replacement.volume),
                        'watertight':bool(replacement.is_watertight)})
    file=out/'ThemeCenter_1939_GuestFlow_Trim_v004.glb';file.write_bytes(runtime.export(file_type='glb'))
    r={'schema':'fmp.shared-portals.v004','source_sha256':SOURCE_SHA,'overlay_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),
       'output':file.name,'apertures':apertures,'replacements':changes,
       'hide_source_nodes':['Perisphere_Lower_Removable_Shell','Helicline_Bridge_Transition_Hypothesis']+list(REPLACED),
       'coordinate_frame':'MODEL_LOCAL_Y_UP_METRES','source_unchanged':hashlib.sha256(source.read_bytes()).hexdigest()==SOURCE_SHA,
       'authority':'Workbook K031/K032 shared aperture rule; not evidence for these dimensions or member transfers',
       'status':'RUNTIME_TOPOLOGY_TEST_ONLY','structural_acceptance':'NOT_ENGINEERED; cut brace ends need archival reframing design',
       'guard_acceptance':'PROVISIONAL_GAP; rail return/edge protection not resolved',
       'historical_acceptance':'UNVERIFIED','unreal_acceptance':'NOT_TESTED',
       'integration':'Replace v003 overlay with v004 and hide only listed source nodes in visitor view. Never overwrite original source/print parts.'}
    (out/'Shared_Portals_v004.json').write_text(json.dumps(r,indent=2)+'\n');return r
if __name__=='__main__':
    if len(sys.argv)!=4:raise SystemExit('usage: python -m tools.world_build.build_shared_portals_v004 SOURCE V003 OUT')
    print(json.dumps(build(*sys.argv[1:]),indent=2))
