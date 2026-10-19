#!/usr/bin/env python3
"""Convert independently fitted FMP 2D source-map transforms to local site/Unreal coordinates.

Georeferencing is horizontal only. An archive/survey specialist must verify
sources, control points, datum and tolerances before production certification.
"""
import argparse
import json
import math
from pathlib import Path

CANONICAL_CRS = 'EPSG:32118'
SCHEMA = 'fmp.georef.scene.v1'


def _finite_number(value, label):
    if isinstance(value, bool):
        raise ValueError(f'{label} must be a finite number')
    try:
        num = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f'{label} must be a finite number') from exc
    if not math.isfinite(num):
        raise ValueError(f'{label} must be a finite number')
    return num


def _affine_params(value, label):
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f'{label} must be a list of 3 numbers')
    return [_finite_number(v, label) for v in value]


def _invert_affine(x, y):
    a, b, tx = x
    c, d, ty = y
    det = a*d - b*c
    scale = max(abs(a), abs(b), abs(c), abs(d))
    if scale == 0 or abs(det) <= 1e-12 * scale * scale:
        raise ValueError('Noninvertible/degenerate source-map transform')
    return [(d / det), (-b / det), (b*ty - d*tx)/det], [(-c / det), (a / det), (c*tx - a*ty)/det]


def _evaluate_quality(fit, max_check_rmse_m):
    control = _finite_number(fit.get('control_rmse_m'), 'control_rmse_m')
    check = _finite_number(fit.get('check_rmse_m'), 'check_rmse_m')
    if control < 0 or check < 0:
        raise ValueError('RMSE values cannot be negative')
    status = 'UNASSESSED' if max_check_rmse_m is None else ('NUMERIC_PASS_NOT_CERTIFIED' if check <= max_check_rmse_m else 'NUMERIC_FAIL')
    return {'control_rmse_m': control, 'check_rmse_m': check,
            'numeric_check_limit_m': max_check_rmse_m, 'status': status,
            'historically_certified': False}


def make_scene(fits, origin_easting_m, origin_northing_m, origin_source, max_check_rmse_m=None):
    if not isinstance(origin_source, str) or not origin_source.strip():
        raise ValueError('A reference describing the measured origin is required')
    e0 = _finite_number(origin_easting_m, 'origin_easting_m')
    n0 = _finite_number(origin_northing_m, 'origin_northing_m')
    if max_check_rmse_m is not None:
        max_check_rmse_m = _finite_number(max_check_rmse_m, 'max_check_rmse_m')
        if max_check_rmse_m <= 0:
            raise ValueError('max_check_rmse_m must be positive')
    if not fits:
        raise ValueError('At least one fitted map required')
    maps = {}
    for map_id, fit in fits.items():
        if not isinstance(map_id, str) or not map_id.strip() or '/' in map_id or '\\' in map_id:
            raise ValueError('Each map ID must be nonempty without path separators')
        if not isinstance(fit, dict):
            raise ValueError(f'{map_id}: fit must be a JSON object')
        if fit.get('crs') != CANONICAL_CRS:
            raise ValueError(f'{map_id}: expected {CANONICAL_CRS}; run a real reprojection for other CRSs')
        if fit.get('certified') is True:
            raise ValueError(f'{map_id}: refusing a claim of certification from an automatic fit')
        ax = _affine_params(fit.get('affine_x'), f'{map_id}.affine_x')
        ay = _affine_params(fit.get('affine_y'), f'{map_id}.affine_y')
        ix, iy = _invert_affine(ax, ay)
        local_x = [ax[0], ax[1], ax[2] - e0]
        local_y = [ay[0], ay[1], ay[2] - n0]
        li_x, li_y = _invert_affine(local_x, local_y)
        maps[map_id] = {
            'pixel_to_projected_m': {'easting': ax, 'northing': ay},
            'projected_m_to_pixel': {'u': ix, 'v': iy},
            'pixel_to_local_site_m': {'east_x': local_x, 'north_y': local_y},
            'local_site_m_to_pixel': {'u': li_x, 'v': li_y},
            'pixel_to_unreal_cm': {'x': [100*v for v in local_x], 'y': [100*v for v in local_y]},
            'qa': _evaluate_quality(fit, max_check_rmse_m),
        }
    return {
        'schema': SCHEMA,
        'horizontal': {'crs': CANONICAL_CRS, 'units': 'metres',
                       'site_x_positive': 'east', 'site_y_positive': 'north',
                       'origin_easting_m': e0, 'origin_northing_m': n0,
                       'origin_source': origin_source.strip()},
        'engine': {'unreal_units': 'centimetres', 'centimetres_per_metre': 100,
                   'unreal_x_positive': 'east', 'unreal_y_positive': 'north'},
        'vertical': {'status': 'UNRESOLVED', 'datum': None,
                     'note': 'No Z offset, elevation or vertical datum inferred.'},
        'use_status': 'PREVIEW_ONLY_UNTIL_INDEPENDENT_SURVEY_VALIDATION',
        'maps': maps,
    }


def _parse_fit_argument(arg):
    if '=' not in arg:
        raise ValueError('Use --fit MAP_ID=path/to/fit.json')
    name, path = arg.split('=', 1)
    if not name.strip() or not path.strip():
        raise ValueError('Map ID and fit JSON path must be nonempty')
    return name, Path(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fit', action='append', required=True, metavar='ID=FIT_JSON')
    parser.add_argument('--origin-easting-m', type=float, required=True)
    parser.add_argument('--origin-northing-m', type=float, required=True)
    parser.add_argument('--origin-source', required=True, help='Provenance for site-origin coordinates')
    parser.add_argument('--max-check-rmse-m', type=float, default=None)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    fits = {}
    for item in args.fit:
        name, path = _parse_fit_argument(item)
        if name in fits:
            parser.error(f'Duplicate map ID: {name}')
        with path.open('r', encoding='utf-8') as fh:
            fits[name] = json.load(fh)
    scene = make_scene(fits, args.origin_easting_m, args.origin_northing_m,
                       args.origin_source, args.max_check_rmse_m)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(scene, indent=2, allow_nan=False)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
