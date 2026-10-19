"""Platform-independent preview markers for FMP georeferenced drawings.

Historical plan pixels may supply horizontal coordinates only. Z=0 is a
preview annotation plane, NOT a ground elevation. No survey is certified.
"""
import json
import math
from pathlib import Path

SCENE_SCHEMA = 'fmp.georef.scene.v1'
CATALOG_SCHEMA = 'fmp.markers.v1'
KINDS = {'SYNTHETIC_TEST_ONLY', 'HISTORICAL_OBSERVATION'}

def finite(value, key):
    if isinstance(value, bool):
        raise ValueError('%s: boolean is not a coordinate' % key)
    try:
        n = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError('%s: coordinate must be numeric' % key) from exc
    if not math.isfinite(n):
        raise ValueError('%s: coordinate must be finite' % key)
    return n

def _axis(values, name):
    if not isinstance(values, list) or len(values) != 3:
        raise ValueError('%s: affine must be 3 coefficients' % name)
    return tuple(finite(v, name) for v in values)

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def make_placements(scene, catalog, *, allow_failed_fit=False):
    """Return normalized placements; reject untraceable and failed QA input."""
    if not isinstance(scene, dict) or scene.get('schema') != SCENE_SCHEMA:
        raise ValueError('Incorrect scene manifest schema')
    h, vertical, maps, engine = (scene.get(k) for k in
                                ('horizontal', 'vertical', 'maps', 'engine'))
    if not isinstance(h, dict) or h.get('crs') != 'EPSG:32118' or h.get('units') != 'metres':
        raise ValueError('Canonical EPSG:32118 metres required')
    if not h.get('origin_source') or not isinstance(maps, dict):
        raise ValueError('Missing site-origin provenance or maps')
    if not isinstance(vertical, dict) or vertical.get('status') != 'UNRESOLVED':
        raise ValueError('This importer does not apply elevations')
    if not isinstance(engine, dict) or engine.get('centimetres_per_metre') != 100:
        raise ValueError('Unreal centimeter convention mismatch')
    if engine.get('unreal_x_positive') != 'east' or engine.get('unreal_y_positive') != 'north':
        raise ValueError('Unreal XY axes do not match FMP convention')
    if not isinstance(catalog, dict) or catalog.get('schema') != CATALOG_SCHEMA:
        raise ValueError('Incorrect marker catalog schema')
    kind = catalog.get('data_class')
    if kind not in KINDS:
        raise ValueError('Only synthetic tests or historical observations are allowed here')
    if not isinstance(catalog.get('markers'), list) or not catalog['markers']:
        raise ValueError('No markers supplied')
    identifiers, placements = set(), []
    for marker in catalog['markers']:
        if not isinstance(marker, dict):
            raise ValueError('Marker must be an object')
        ident, map_id = marker.get('id'), marker.get('source_map_id')
        if not isinstance(ident, str) or not ident.strip() or any(c in ident for c in '\\/:'):
            raise ValueError('Invalid marker ID')
        if ident in identifiers:
            raise ValueError('Duplicate marker ID: ' + ident)
        identifiers.add(ident)
        if not isinstance(map_id, str) or map_id not in maps:
            raise ValueError('%s: unknown source map' % ident)
        entry = maps[map_id]
        qa = entry.get('qa')
        if not isinstance(qa, dict) or qa.get('historically_certified') is not False:
            raise ValueError('%s: missing/invalid QA state' % map_id)
        if qa.get('status') == 'NUMERIC_FAIL' and not allow_failed_fit:
            raise ValueError('%s: map failed numeric QA' % map_id)
        pixel = marker.get('pixel')
        if not isinstance(pixel, list) or len(pixel) != 2:
            raise ValueError('%s: pixel must be [u,v]' % ident)
        u, v = [finite(x, ident + '.pixel') for x in pixel]
        t = entry.get('pixel_to_local_site_m')
        if not isinstance(t, dict):
            raise ValueError('%s: missing map transform' % map_id)
        ax, ay = _axis(t.get('east_x'), map_id + '.east_x'), _axis(t.get('north_y'), map_id + '.north_y')
        x, y = ax[0]*u + ax[1]*v + ax[2], ay[0]*u + ay[1]*v + ay[2]
        if not math.isfinite(x) or not math.isfinite(y):
            raise ValueError('%s: overflow position' % ident)
        title, period = marker.get('title', ident), marker.get('period', 'unassigned')
        if not isinstance(title, str) or not title.strip():
            raise ValueError('%s: invalid title' % ident)
        if not isinstance(period, str) or not period.strip() or any(c in period for c in '/\\:'):
            raise ValueError('%s: invalid period' % ident)
        placements.append({
            'id': ident, 'title': title, 'period': period,
            'source_map_id': map_id, 'data_class': kind, 'pixel': [u, v],
            'local_m': [x, y, 0.0], 'unreal_cm': [100*x, 100*y, 0.0],
            'height_status': 'UNRESOLVED_PREVIEW_Z0', 'qa_status': qa['status']
        })
    return placements

def read_placements(scene_path, catalog_path, *, allow_failed_fit=False):
    return make_placements(load_json(scene_path), load_json(catalog_path),
                           allow_failed_fit=allow_failed_fit)

def export_preview(scene_path, catalog_path, output_path):
    placements = read_placements(scene_path, catalog_path)
    data = {'schema': 'fmp.marker-preview.v1', 'certified': False,
            'vertical': 'UNRESOLVED_PREVIEW_Z0', 'placements': placements}
    Path(output_path).write_text(json.dumps(data, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    return data

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('scene'); ap.add_argument('catalog'); ap.add_argument('--output', required=True)
    args = ap.parse_args()
    data = export_preview(args.scene, args.catalog, args.output)
    print('Validated and exported %d preview markers' % len(data['placements']))
