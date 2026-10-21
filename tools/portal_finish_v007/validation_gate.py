"""Bind the discrete portal screen to exact asset bytes and reject failed reports."""
import hashlib


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_clear(report, asset_path, portal_ids):
    if report.get('asset_sha256') != sha256(asset_path):
        raise ValueError('Clearance report is stale or lacks the current asset hash')
    expected = set(portal_ids)
    screens = report.get('screens', [])
    ids = [screen.get('portal') for screen in screens]
    if len(ids) != len(expected) or set(ids) != expected:
        raise ValueError('Clearance report has missing or duplicate portals')
    for key in ('preservation', 'added_solids', 'brace_jamb_connections'):
        if report.get(key) != 'PASS':
            raise ValueError('Failed geometry check: ' + key)
    for screen in screens:
        if screen.get('poses') != 51 or screen.get('sphere_samples') != 663:
            raise ValueError('Incomplete doorway screen')
        if screen.get('surface_contacts') != []:
            raise ValueError('Doorway surface contact: ' + screen['portal'])
