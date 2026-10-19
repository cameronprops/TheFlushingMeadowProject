"""Read-only, model-local surface audit. No capsule or historical certification."""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import trimesh

SOURCE_SHA = 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5'

def vertical_surface(mesh, xz, reference_y, window=1.0):
    """Nearest upward-facing surface within a vertical window, or None.

    Barycentric XZ projection avoids nearest-vertex bias. Sidewalls and
    downward soffits cannot qualify. This samples points, not swept bodies.
    """
    tri = mesh.triangles
    a = tri[:, 0][:, [0, 2]]
    u = tri[:, 1][:, [0, 2]] - a
    v = tri[:, 2][:, [0, 2]] - a
    w = np.asarray(xz) - a
    det = u[:, 0]*v[:, 1] - u[:, 1]*v[:, 0]
    valid = (np.abs(det) > 1e-12) & (mesh.face_normals[:, 1] > 0.5)
    indices = np.flatnonzero(valid)
    if not len(indices):
        return None
    b = (w[valid, 0]*v[valid, 1]-w[valid, 1]*v[valid, 0])/det[valid]
    c = (u[valid, 0]*w[valid, 1]-u[valid, 1]*w[valid, 0])/det[valid]
    inside = (b >= -1e-8) & (c >= -1e-8) & (b+c <= 1+1e-8)
    ys = tri[valid, 0, 1]+b*(tri[valid, 1, 1]-tri[valid, 0, 1])+c*(tri[valid, 2, 1]-tri[valid, 0, 1])
    inside &= np.abs(ys-reference_y) <= window
    if not inside.any():
        return None
    picks = np.flatnonzero(inside)
    pick = picks[np.argmin(np.abs(ys[picks]-reference_y))]
    return {'surface_y_m': float(ys[pick]), 'drop_from_route_m': float(reference_y-ys[pick]),
            'triangle_index': int(indices[pick])}

def world_mesh(scene, name):
    transform, key = scene.graph[name]
    mesh = scene.geometry[key].copy()
    mesh.apply_transform(transform)
    return mesh

def audit(source):
    source = Path(source)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != SOURCE_SHA:
        raise ValueError('Unknown source revision')
    scene = trimesh.load(source, force='scene')
    helix = world_mesh(scene, 'Helicline_Deck_and_Curved_Soffit')
    floor = float(world_mesh(scene, 'Return_Bridge_Deck').bounds[1, 1])
    target = np.array([-32.5, floor, -9.5])
    approach = np.array([3.1, 0, -6.35]); approach /= np.linalg.norm(approach)
    across = np.array([-approach[2], 0, approach[0]])
    closest, distance, faces = trimesh.proximity.closest_point_naive(helix, [target])
    samples = []
    for along in (-.5, -.25, 0, .25, .5):
        for lateral in (-1.05, -.525, 0, .525, 1.05):
            point = target + along*approach + lateral*across
            samples.append({'along_m': along, 'lateral_m': lateral,
                            'sample_xyz_m': point.tolist(),
                            'surface': vertical_surface(helix, point[[0, 2]], floor)})
    return {'schema': 'fmp.helicline-surface-audit.v1', 'source_sha256': digest,
            'coordinate_frame': 'MODEL_LOCAL_Y_UP_METRES',
            'route_width_m': 2.1, 'sampling_window_m': 1.0,
            'reference': 'r2 provisional route endpoint; not historical survey',
            'nearest_vertex_distance_m': float(np.linalg.norm(helix.vertices-target, axis=1).min()),
            'nearest_triangle_distance_m': float(distance[0]),
            'nearest_triangle_point_m': closest[0].tolist(),
            'nearest_triangle_index': int(faces[0]),
            'samples': samples,
            'missing_surface_samples': sum(s['surface'] is None for s in samples),
            'acceptance': 'OPEN_SURFACE_TRANSITION_AND_BODY_CLEARANCE',
            'limits': ['25 discrete points do not certify continuous support',
                       'Only Helicline deck queried; no whole-scene obstruction check',
                       'No Unreal capsule, collision or navigation test',
                       'No geometry changed']}

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: audit_helicline_join.py SOURCE.glb REPORT.json')
    report = audit(sys.argv[1])
    Path(sys.argv[2]).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'samples'}, indent=2))
