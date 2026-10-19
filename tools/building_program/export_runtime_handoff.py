#!/usr/bin/env python3
"""Read-only FMP master SQLite -> Unreal / print / future projection manifest.

No scene geometry is mutated; no viewer position or registration is guessed.
Run: python tools/building_program/export_runtime_handoff.py --db out/flushing_meadows.sqlite --out out/handoff
     python tools/building_program/export_runtime_handoff.py --db ... --out ... --building WF0002 --scale 250
Python >=3.10, stdlib only.
"""
import argparse, hashlib, json, math, sqlite3
from pathlib import Path

SCHEMA = 'fmp.runtime-handoff.v1'

def present(conn, name):
    return conn.execute("SELECT 1 FROM sqlite_master WHERE name=? AND type IN ('table','view')", (name,)).fetchone() is not None

def query(conn, sql, args=()):
    return [dict(x) for x in conn.execute(sql, args)]

def finite_or_none(n):
    if n is None: return None
    v=float(n)
    if not math.isfinite(v): raise ValueError('Nonfinite model coordinate')
    return v

def bounds_from_parts(parts):
    if not parts: return None
    mins = [min(finite_or_none(p[f'min_{a}_m']) for p in parts) for a in 'xyz']
    maxs = [max(finite_or_none(p[f'max_{a}_m']) for p in parts) for a in 'xyz']
    if any(hi<lo for lo,hi in zip(mins,maxs)): raise ValueError('Inverted bounds')
    return dict(min_xyz_m=mins,max_xyz_m=maxs,size_xyz_m=[round(b-a,6) for a,b in zip(mins,maxs)])

def unreal_transform(up):
    # Row-major affine matrices: RH source metres -> left-handed Unreal Z-up cm.
    # GLB normally Y-up; some FMP historical previews store source vertices Z-up.
    if up=='Y': return [[100,0,0,0],[0,0,100,0],[0,100,0,0],[0,0,0,1]]
    if up=='Z': return [[100,0,0,0],[0,-100,0,0],[0,0,100,0],[0,0,0,1]]
    raise ValueError(f'No approved X-up axis transform: {up}')

def print_dimensions_mm(bounds, denominator):
    return [round(1000.0*x/denominator,3) for x in bounds['size_xyz_m']]

def bundle(conn, building_id, year, denominator):
    if denominator<=0: raise ValueError('Print scale denominator must be positive')
    conn.row_factory=sqlite3.Row
    if present(conn, 'building_dossiers'):
        building=query(conn,"SELECT building_id,classification,site_position_status,footprint_status,public_access_status FROM building_dossiers WHERE building_id=?",(building_id,))
        if not building: raise ValueError(f'Unknown building {building_id}')
        building=building[0]
    else: building=dict(building_id=building_id,classification='NOT_AVAILABLE_IN_FIXTURE',site_position_status='UNREGISTERED',footprint_status='NOT_TRACED',public_access_status='NOT_TESTED')
    rows=query(conn,'SELECT * FROM master_active_model_releases WHERE building_id=? AND period_year=? ORDER BY logical_role',(building_id,year))
    models=[]; materials={}; warnings=[]
    for row in rows:
        parts=query(conn,'SELECT * FROM master_model_components WHERE building_id=? AND period_year=? AND model_asset_id=? ORDER BY source_node',(building_id,year,row['active_media_id']))
        if not parts:
            warnings.append(f"Active asset {row['active_media_id']} has no matching mesh observations")
            continue
        source_hashes={p['source_sha256'] for p in parts}
        if source_hashes!={row['source_sha256']}:
            raise ValueError(f"Hash mismatch for active model {row['active_media_id']}")
        up=row['up_axis']
        bounds=bounds_from_parts(parts)
        model=dict(release_key=row['release_key'],asset_id=row['active_media_id'],
            source_path=row['source_path'],source_sha256=row['source_sha256'],
            logical_role=row['logical_role'],source_up_axis=up,
            source_frame='RIGHT_HANDED_ASSUMED_REQUIRES_HOST_CONFIRMATION',
            transform_source_m_to_unreal_cm=unreal_transform(up),
            matrix_convention='ROW_MAJOR_COLUMN_VECTOR',
            bounds_source_m=bounds,
            preview_print_size_mm=print_dimensions_mm(bounds,denominator),
            observed_mesh_count=len(parts),
            watertight_mesh_count=sum(bool(p['watertight']) for p in parts),
            mesh_parts=[dict(component_id=p['component_id'],source_node=p['source_node'],
                geometry_key=p['mesh_key'],role=p['role'],material_name=p['material_name'],
                vertices=p['vertices'],faces=p['faces'],watertight=bool(p['watertight'])) for p in parts],
            limitations=['Source coordinates are not historical fairground coordinates',
                         'Watertight component is not certified print-ready',
                         'Unreal import, normals/winding and collision require native verification'])
        models.append(model)
        for p in parts:
            key=(row['active_media_id'],p['material_name'] or 'UNASSIGNED')
            materials[key]=dict(asset_id=key[0],source_material_name=key[1],
                source_roughness=p['roughness'],source_metallic=p['metallic'],
                unreal_material_instance=None,projection_surface_override=None,
                evidence_status='MODEL_OBSERVED_MATERIAL_NOT_HISTORICAL_FINISH')
    if present(conn,'master_interactive_points'):
        ints=query(conn,'SELECT * FROM master_interactive_points WHERE building_id=? AND period_year=? ORDER BY point_id',(building_id,year))
    else: ints=[]
    hotspots=[]
    for r in ints:
        xyz=[finite_or_none(r[k]) for k in ('x_m','y_m','z_m')]
        if any(v is None for v in xyz) and any(v is not None for v in xyz):
            raise ValueError('Partial hotspot coordinates are invalid: '+r['point_id'])
        if r['position_status']=='UNLOCATED' and any(v is not None for v in xyz):
            raise ValueError('Unlocated hotspot has coordinates: '+r['point_id'])
        hotspots.append(dict(point_id=r['point_id'],label=r['label'],type=r['interaction_type'],
            action_key=r['trigger_or_scene_key'],requested_behavior=r['requested_behavior'],
            position_xyz_m=xyz if xyz[0] is not None else None,
            coordinate_frame=r['coordinate_frame'],status=r['position_status'],
            operational=False,engine_tested=bool(r['native_unreal_tested'])))
    if present(conn,'building_spaces'):
        spaces=query(conn,'SELECT space_id,space_name,access_intent,collision_status,navigation_status FROM building_spaces WHERE building_id=? AND year=? ORDER BY space_id',(building_id,year))
    else: spaces=[]
    if present(conn,'master_all_media'):
        media=query(conn,'SELECT media_ref,record_type,title,media_kind,uri,project_uri,rights_status,acquisition_status FROM master_all_media WHERE building_id=? AND (period_year IS NULL OR period_year=?) ORDER BY media_ref',(building_id,year))
    else: media=[]
    if present(conn,'master_building_envelopes'):
        envelopes=query(conn,'SELECT envelope_id,source_asset_id,coordinate_frame,evidence_status,site_registered FROM master_building_envelopes WHERE building_id=? AND period_year=? ORDER BY envelope_id',(building_id,year))
    else: envelopes=[]
    obj=dict(schema=SCHEMA,building_id=building_id,period_year=year,history_classification=building['classification'],
        physical_scale=dict(model_units='m',preview_print_scale=f'1:{denominator}',
             target_units='mm',print_scale_denominator=denominator,
             manufacturing_scale_not_validated=True),
        geometry_registration=dict(site_registered=False,
            source_envelopes=envelopes,world_to_physical_matrix=None,
            projector_intrinsics=None,projector_extrinsics=None,
            projector_warp=None,projection_calibrated=False),
        models=models,material_slots=[materials[k] for k in sorted(materials)],
        interactive_points=hotspots,public_spaces=spaces,media_manifest=media,
        render_targets=dict(unreal_status='HANDOFF_ONLY_NOT_IMPORTED',
             print_status='SCALE_PREVIEW_ONLY_NOT_SLICED',
             projection_status='FUTURE_INTEGRATION_NO_CALIBRATION',
             worldwright_show_control='FUTURE_OPTION_NOT_CONNECTED'),warnings=warnings)
    return obj

def export(conn,out,buildings=None,denominator=250):
    conn.row_factory=sqlite3.Row
    if not present(conn,'master_active_model_releases'): raise ValueError('Missing master_active_model_releases table')
    if not present(conn,'master_model_components'): raise ValueError('Missing master_model_components table')
    rows=query(conn,'SELECT DISTINCT building_id,period_year FROM master_active_model_releases ORDER BY building_id,period_year')
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    entries=[]
    for row in rows:
        bid,year=row['building_id'],row['period_year']
        if buildings and bid not in buildings:continue
        obj=bundle(conn,bid,year,denominator)
        name=f'{bid}_{year}_handoff.json'
        data=(json.dumps(obj,sort_keys=True,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
        (out/name).write_bytes(data)
        entries.append(dict(building_id=bid,year=year,file=name,sha256=hashlib.sha256(data).hexdigest(),
            model_count=len(obj['models']),mesh_count=sum(m['observed_mesh_count'] for m in obj['models']),
            materials=len(obj['material_slots']),unlocated_hotspots=sum(p['position_xyz_m'] is None for p in obj['interactive_points'])))
    index=dict(schema='fmp.runtime-handoff-index.v1',units='source metres / Unreal cm / physical preview mm',
        print_scale_denominator=denominator,buildings=entries,engine_accepted=False,projection_calibrated=False)
    (out/'handoff_index.json').write_text(json.dumps(index,sort_keys=True,indent=2)+'\n')
    return index

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--db',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--building',action='append')
    ap.add_argument('--scale',type=int,default=250)
    args=ap.parse_args()
    with sqlite3.connect(args.db) as con:
        con.row_factory=sqlite3.Row
        idx=export(con,args.out,args.building,args.scale)
    print(json.dumps({'buildings':len(idx['buildings']),'mesh_parts':sum(x['mesh_count'] for x in idx['buildings'])},indent=2))
if __name__=='__main__':main()
