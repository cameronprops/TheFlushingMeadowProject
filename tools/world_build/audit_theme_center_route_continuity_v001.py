"""Conservative OFFLINE swept-sphere surface-contact exclusion for 1939 FMP return route.

Proves sampled-path *surface separation* only under explicit finite-radius,
finite-height, no-rotation capsule assumptions. Does NOT prove solid exclusion,
movement feasibility, Unreal collision, physics, accessibility or historical geometry.
Never writes or edits input GLBs.

Usage:
    python -m tools.world_build.audit_theme_center_route_continuity_v001 \
        --glb EXACT_V005.glb --manifest ASSEMBLED_RUNTIME_v005.json \
        --route RETURN_ROUTE_CLEARANCE_v004.json --out result.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import trimesh

EXPECTED_GLB_SHA = 'de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439'
EXPECTED_SOURCE_SHA = 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5'
EXPECTED_OVERLAY_SHA = 'b1467273bf674c7fbf081bb7ec64800ae61ecf88942e42678ed8948c452c5e01'
EXPECTED_HIDDEN = {'Perisphere_Lower_Removable_Shell', 'Helicline_Bridge_Transition_Hypothesis', 'Trylon_Face_3_Frame', 'Trylon_Hollow_Exterior', 'Helicline_Rail_-1'}
EXPECTED_ROUTE_REPORT_SHA = '0c81c8a35a6448027c73254c7e7ed8d083ccc04ea6b188e89b591965509cea9c'
DEFAULT_SUBDIVISIONS = 16


class RouteAuditError(ValueError):
    pass


def ensure(condition, reason):
    if not condition:
        raise RouteAuditError(reason)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def validate_lineage(route: dict, manifest: dict, glb: Path) -> None:
    ensure(sha256_file(glb) == EXPECTED_GLB_SHA, 'Unexpected GLB SHA-256')
    ensure(manifest['sha256'] == EXPECTED_GLB_SHA, 'Unexpected manifest asset identity')
    ensure(manifest['source_sha256'] == route['source_sha256'] == EXPECTED_SOURCE_SHA, 'Source mismatch')
    ensure(manifest['overlay_sha256'] == route['overlay_sha256'] == EXPECTED_OVERLAY_SHA, 'Overlay mismatch')
    ensure({x['name'] for x in manifest['disabled_source_meshes']} == EXPECTED_HIDDEN, 'Disabled source mesh set mismatch')
    ensure(set(route['hidden_source_nodes']) == EXPECTED_HIDDEN, 'Route screen hidden source mismatch')
    ensure(route['route'] == 'return' and route['pose_count'] == len(route['poses']) == 435, 'Unexpected return route grid')
    ensure(route['status'] == 'NO_SAMPLED_SURFACE_CONTACTS' and not route['findings'], 'Original screen contains obstacles')
    ensure(route['acceptance'] == 'OPEN_NATIVE_COLLISION_AND_CONTINUOUS_SWEEP', 'Unexpected original acceptance')
    body = route['body_assumption']
    ensure(abs(body['radius_m'] - 0.3) < 1e-10 and abs(body['height_m'] - 1.8) < 1e-10, 'Changed test body')
    ensure(abs(body['axis_cover_radius_m'] - math.hypot(0.3, 0.05)) < 1e-8, 'Changed axis cover sphere')
    ensure(route['checked_nodes'] and all(math.isfinite(x['minimum_surface_clearance_m']) for x in route['checked_nodes']), 'Missing surface-clearance measurements')
    ensure(not any(x['minimum_surface_clearance_m'] <= 0 for x in route['checked_nodes']), 'Original screen failed')


def track_groups(route: dict) -> dict:
    groups = defaultdict(list)
    for p in route['poses']:
        ensure(p.get('segment') in (1, 2, 3, 4) and p.get('lateral_m') in (-0.6, 0, 0.6), 'Unexpected pose group')
        xyz = np.asarray(p['foot_xyz_m'], dtype=np.float64)
        ensure(xyz.shape == (3,) and np.all(np.isfinite(xyz)), 'Invalid foot location')
        groups[(p['segment'], p['lateral_m'])].append(xyz)
    ensure(len(groups) == 12 and all(len(v) >= 2 for v in groups.values()), 'Missing route tracks')
    return groups


def straight_segment_bound(route: dict, groups: dict) -> dict:
    """One-Lipschitz distance bound, only for obstacles actually screened by v004.

    Each axis-cover sphere center moves the same 3D translation as the foot point.
    Along straight interpolation, the nearest endpoint is at most half the step
    distance away, hence surface separation >= sampled_separation - step/2.
    Geometry excluded by v004's global expanded-AABB narrow phase cannot touch
    these straight interpolants as they lie within that entire bounding box.
    """
    margin = min(x['minimum_surface_clearance_m'] for x in route['checked_nodes'])
    rows = []
    all_steps = []
    for (seg, lat), points in sorted(groups.items()):
        steps = [float(np.linalg.norm(b-a)) for a, b in zip(points, points[1:])]
        max_step = max(steps)
        lower_bound = margin - max_step / 2
        rows.append({'segment': seg, 'lateral_m': lat, 'edges': len(steps), 'max_translation_m': max_step,
                     'screened_obstacle_clearance_lower_bound_m': lower_bound,
                     'screened_surface_contact_excluded': lower_bound > 0})
        all_steps.extend(steps)
    return {'sampled_min_clearance_to_screened_obstacles_m': margin,
            'edges_checked': len(all_steps), 'max_step_m': max(all_steps),
            'minimum_screened_obstacle_lower_bound_m': min(r['screened_obstacle_clearance_lower_bound_m'] for r in rows),
            'all_straight_interpolants_surface_contact_excluded': all(r['screened_surface_contact_excluded'] for r in rows),
            'tracks': rows}


def corner_surface_certificate(scene: trimesh.Scene, a, b, body: dict, *, subdivisions=8) -> dict:
    """Screen scene triangles and mathematically bound interpolation between poses.

    Sampled axis spheres conservatively cover the vertical capsule; a candidate
    triangle that can contact any interpolated sphere must overlap the AABB of
    sphere centers enlarged by cover radius. Pad additionally by half a step
    for the one-Lipschitz test at sample locations. For each candidate surface,
    minimum sampled distance minus (cover sphere radius + half step) must be >0.
    This proves absence of *surface contacts*, NOT being outside closed solids.
    """
    ensure(isinstance(subdivisions, int) and subdivisions >= 1, 'Invalid subdivisions')
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    radius = body['radius_m']; height = body['height_m']; cover = body['axis_cover_radius_m']
    ensure(height >= 2 * radius, 'Invalid body height')
    foots = a[None, :] + np.linspace(0, 1, subdivisions + 1)[:, None] * (b-a)[None, :]
    # Thirteen axis centers at 0.1m intervals from capsule's bottom sphere center
    # to top sphere center, exactly reproducing the existing v004 body screen.
    ys = np.linspace(radius, height - radius, 13)
    ensure(np.max(np.diff(ys)) <= 0.100000001 and cover >= math.hypot(radius, np.max(np.diff(ys)) / 2), 'Axis-cover spheres do not enclose continuous capsule axis')
    centers = np.vstack([foots + [0, y, 0] for y in ys])
    halfstep = float(np.linalg.norm(b-a)) / (2 * subdivisions)
    search_radius = cover + halfstep + 1e-9
    lo = centers.min(axis=0) - search_radius
    hi = centers.max(axis=0) + search_radius
    touched_meshes = 0; checked_triangles = 0; min_clearance = float('inf'); closest_node = None
    for node in sorted(scene.graph.nodes_geometry):
        tf, key = scene.graph[node]
        mesh = scene.geometry[key]
        # Affine transform of all bounding-box corners gives a conservative
        # candidate bound even when a node has nontrivial orientation/scale.
        bb = trimesh.transform_points(trimesh.bounds.corners(mesh.bounds), tf)
        if np.any(bb.max(axis=0) < lo) or np.any(bb.min(axis=0) > hi):
            continue
        world = mesh.copy()
        world.apply_transform(tf)
        tris = world.triangles
        crop = np.all(tris.max(axis=1) >= lo, axis=1) & np.all(tris.min(axis=1) <= hi, axis=1)
        if not np.any(crop):
            continue
        # Every excluded triangle lies outside the entire axis-sphere corridor;
        # it cannot touch any point on these interpolated motions.
        submesh = trimesh.Trimesh(vertices=world.vertices, faces=world.faces[crop], process=False)
        distances = trimesh.proximity.closest_point_naive(submesh, centers)[1]
        sampled = float(np.min(distances) - cover)
        if sampled < min_clearance:
            min_clearance = sampled
            closest_node = node
        touched_meshes += 1
        checked_triangles += int(np.count_nonzero(crop))
    lower_bound = None if not math.isfinite(min_clearance) else float(min_clearance - halfstep)
    return {'jump_length_m': float(np.linalg.norm(b-a)), 'subdivisions': subdivisions,
            'sampled_capsule_poses': subdivisions + 1,
            'candidate_mesh_nodes': touched_meshes, 'candidate_triangles': checked_triangles,
            'nearest_candidate_node': closest_node,
            'candidate_min_sampled_clearance_m': None if lower_bound is None else min_clearance,
            'candidate_min_lipschitz_lower_bound_m': lower_bound,
            'surface_contact_excluded': lower_bound is None or lower_bound > 0}


def audit(glb: Path, manifest: dict, route: dict, subdivisions=DEFAULT_SUBDIVISIONS) -> dict:
    validate_lineage(route, manifest, glb)
    groups = track_groups(route)
    straight = straight_segment_bound(route, groups)
    scene = trimesh.load(glb, force='scene', process=False)
    ensure(len(scene.graph.nodes_geometry) == manifest['visible_mesh_nodes'] == 558, 'GLB active node count mismatch')
    rows=[]
    for seg in range(1, 4):
        for lat in (-0.6, 0, 0.6):
            a=groups[(seg,lat)][-1]; b=groups[(seg+1,lat)][0]
            x=corner_surface_certificate(scene,a,b,route['body_assumption'],subdivisions=subdivisions)
            x.update({'from_segment':seg,'to_segment':seg+1,'lateral_m':lat})
            rows.append(x)
    corner_pass=all(r['surface_contact_excluded'] for r in rows)
    return {
        'schema': 'fmp.theme-center.surface-route-continuity.v001',
        'glb_sha256': EXPECTED_GLB_SHA,
        'source_sha256': EXPECTED_SOURCE_SHA, 'overlay_sha256': EXPECTED_OVERLAY_SHA,
        'source_v004_pose_count': route['pose_count'],
        'body_assumption': route['body_assumption'],
        'method': 'straight-track one-Lipschitz bound from archived v004 screened obstacles; full-active-scene triangle distance screen with subdivided straight corner joins and one-Lipschitz bounds',
        'straight_sections': straight,
        'corner_links_checked':len(rows), 'corners':rows,
        'overall_surface_contact_excluded_for_declared_track_paths': bool(straight['all_straight_interpolants_surface_contact_excluded'] and corner_pass),
        'acceptance': 'OFFLINE_SURFACE_CONTACT_EXCLUSION_ONLY' if straight['all_straight_interpolants_surface_contact_excluded'] and corner_pass else 'SURFACE_CONTACT_NOT_EXCLUDED',
        'native_unreal_collision_and_playtest': 'NOT_RUN',
        'limitations': [
            'Tested only the 12 archived lateral tracks and nine new straight-link corner paths, not arbitrary visitor steering or all other public routes',
            'Only triangle-surface separation is bounded; a player entirely contained in a closed solid is not detected by surface distances',
            'Collision presets, stairs, movement modes, navmesh, actual character shape and walkability have not been tested in Unreal',
            'The v004 original uses a bounded static triangle screen and excludes designated superseded source meshes',
            'Conservative cover spheres can overreport obstructions; clear positive bounds exclude surface contact only',
            'Source geometry remains historical/provisional and site-unregistered; no printed geometry or structural safety is certified'
        ]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--glb',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--route',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--corner-subdivisions',type=int,default=DEFAULT_SUBDIVISIONS)
    a=p.parse_args()
    ensure(sha256_file(a.route) == EXPECTED_ROUTE_REPORT_SHA, 'Unexpected archived v004 route report SHA-256')
    report=audit(a.glb,json.loads(a.manifest.read_text()),json.loads(a.route.read_text()),a.corner_subdivisions)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':report['acceptance'],'straight_edges':report['straight_sections']['edges_checked'], 'corners':report['corner_links_checked'],'minimum_screened_straight_bound_m':report['straight_sections']['minimum_screened_obstacle_lower_bound_m']},indent=2))
    if not report['overall_surface_contact_excluded_for_declared_track_paths']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
