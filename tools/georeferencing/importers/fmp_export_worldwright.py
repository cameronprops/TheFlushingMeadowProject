"""Export FMP markers to Worldwright DXF and a provenance sidecar.

Open DXF in existing Worldwright/CADCraft importer, then Save As .dftba.
DXF stores site-local metres, not real historical Z elevations.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
from fmp_marker_core import read_placements

DXF_VERSION = 'AC1015'
METRE_INSUNITS = 6

def _tags(*items):
    if len(items) % 2:
        raise ValueError('Each DXF group code needs a value')
    return ''.join('{}\n{}\n'.format(items[i], items[i+1]) for i in range(0, len(items), 2))

def _safe_id(value):
    if not isinstance(value, str) or not value or len(value) > 200:
        raise ValueError('Invalid identifier')
    if any(c in value for c in '\n\r\0'):
        raise ValueError('Invalid identifier characters')
    return value

def _layer(source):
    raw = 'FMP_' + _safe_id(source)
    name = ''.join(ch if ch.isascii() and (ch.isalnum() or ch in '_-.') else '_' for ch in raw)
    if len(name) > 200:
        raise ValueError('Source map ID too long for DXF layer')
    return name

def _finite(value):
    try:
        n = float(value)
    except (ValueError, TypeError) as exc:
        raise ValueError('Invalid coordinate') from exc
    if not math.isfinite(n):
        raise ValueError('Invalid coordinate')
    return n

def encode_dxf(placements):
    """Build AC1015 ASCII DXF with POINT, annotation crosshairs and TEXT labels."""
    if not placements:
        raise ValueError('No placements')
    layers = sorted({_layer(p['source_map_id']) for p in placements})
    output = [_tags(0, 'SECTION', 2, 'HEADER', 9, '$ACADVER', 1, DXF_VERSION,
                    9, '$INSUNITS', 70, METRE_INSUNITS,
                    9, '$MEASUREMENT', 70, 1, 0, 'ENDSEC',
                    0, 'SECTION', 2, 'TABLES', 0, 'TABLE',
                    2, 'LAYER', 70, len(layers))]
    for layer in layers:
        output.append(_tags(0, 'LAYER', 2, layer, 70, 0, 62, 7, 6, 'CONTINUOUS'))
    output.append(_tags(0, 'ENDTAB', 0, 'ENDSEC', 0, 'SECTION', 2, 'ENTITIES'))
    observed = set()
    for p in placements:
        ident = _safe_id(p['id'])
        if ident in observed:
            raise ValueError('Duplicate marker ID')
        observed.add(ident)
        if p['height_status'] != 'UNRESOLVED_PREVIEW_Z0':
            raise ValueError('Expected unresolved vertical preview')
        if p['data_class'] not in ('SYNTHETIC_TEST_ONLY', 'HISTORICAL_OBSERVATION'):
            raise ValueError('Invalid data class')
        layer = _layer(p['source_map_id'])
        xyz = p['local_m']
        if not isinstance(xyz, list) or len(xyz) != 3:
            raise ValueError('Three local coordinates required')
        x, y, z = [_finite(v) for v in xyz]
        if z != 0:
            raise ValueError('Refuse fabricated height values')
        output.append(_tags(0, 'POINT', 8, layer, 10, x, 20, y, 30, 0.0))
        # Crosshair annotation only, 1 m by 1 m.
        for ax, ay, bx, by in ((x-0.5,y,x+0.5,y), (x,y-0.5,x,y+0.5)):
            output.append(_tags(0, 'LINE', 8, layer, 10, ax, 20, ay, 30, 0.0,
                                11, bx, 21, by, 31, 0.0))
        label = ''.join(ch if ord(ch) < 127 and ch not in '\r\n' else '_' for ch in ident)
        output.append(_tags(0, 'TEXT', 8, layer, 10, x+0.7, 20, y+0.7,
                            30, 0.0, 40, 0.6, 1, label))
    output.append(_tags(0, 'ENDSEC', 0, 'EOF'))
    return ''.join(output)

def export_worldwright(scene_path, catalog_path, out_path):
    placements = read_placements(scene_path, catalog_path)
    dxf = encode_dxf(placements)
    path = Path(out_path)
    if path.suffix.lower() != '.dxf':
        raise ValueError('Output must be .dxf; .dftba belongs to native Worldwright IO')
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = dxf.encode('ascii')
    path.write_bytes(raw)
    sidecar = {
        'schema': 'fmp.worldwright.dxf-preview.v1',
        'data_class': 'PREVIEW_ONLY_NOT_SURVEY_CERTIFIED',
        'horizontal_crs': 'EPSG:32118',
        'position_units': 'metres',
        'height_status': 'UNRESOLVED_PREVIEW_Z0',
        'dxf_sha256': hashlib.sha256(raw).hexdigest(),
        'dxf_filename': path.name,
        'placements': placements,
        'warning': 'DXF markers are annotations, not reconstructed terrain or verified historical geometry.'
    }
    sidecar_path = path.with_suffix('.fmp.json')
    sidecar_path.write_text(json.dumps(sidecar, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    return path, sidecar_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scene')
    parser.add_argument('catalog')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    path, sidecar = export_worldwright(args.scene, args.catalog, args.output)
    print('Worldwright preview DXF:', path)
    print('Audit sidecar:', sidecar)
