"""Rhino 8 Python 3 / RhinoCommon FMP preview point importer.

Run via Rhino 8 Python 3 editor. Does not change model units or place Z heights.
"""
from fmp_marker_core import read_placements

def apply_to_doc(doc, rhino, placements):
    if doc is None:
        raise RuntimeError('Open a Rhino document first')
    units = doc.ModelUnitSystem
    if units == rhino.UnitSystem.CustomUnits or units == getattr(rhino.UnitSystem, "None", None):
        raise ValueError('Set standard model units before importing')
    factor = rhino.RhinoMath.UnitScale(rhino.UnitSystem.Meters, units)
    if factor <= 0:
        raise ValueError('Invalid Rhino unit scale')
    existing = set()
    for obj in doc.Objects:
        value = obj.Attributes.GetUserString('FMP_MARKER_ID')
        if value:
            existing.add(value)
    added = skipped = 0
    layers = {}
    for p in placements:
        if p['id'] in existing:
            skipped += 1
            continue
        name = 'FMP_PREVIEW_' + p['source_map_id']
        if name not in layers:
            layer = doc.Layers.FindName(name)
            if layer is None:
                layer = rhino.DocObjects.Layer()
                layer.Name = name
                index = doc.Layers.Add(layer)
                if index < 0:
                    raise RuntimeError('Cannot create layer: ' + name)
            else:
                index = layer.Index
            layers[name] = index
        attr = rhino.DocObjects.ObjectAttributes()
        attr.Name = 'FMP_PREVIEW_' + p['id']
        attr.LayerIndex = layers[name]
        attr.SetUserString('FMP_MARKER_ID', p['id'])
        attr.SetUserString('FMP_MAP_ID', p['source_map_id'])
        attr.SetUserString('FMP_PERIOD', p['period'])
        attr.SetUserString('FMP_STATUS', p['data_class'] + '/' + p['height_status'])
        x, y, z = p['local_m']
        point = rhino.Geometry.Point3d(x*factor, y*factor, z*factor)
        obj_id = doc.Objects.AddPoint(point, attr)
        if not obj_id or str(obj_id) == '00000000-0000-0000-0000-000000000000':
            raise RuntimeError('Could not create Rhino point: ' + p['id'])
        existing.add(p['id'])
        added += 1
    doc.Views.Redraw()
    return {'added': added, 'skipped_existing': skipped}

def import_markers(scene_path, catalog_path):
    import Rhino
    import scriptcontext as sc
    return apply_to_doc(sc.doc, Rhino, read_placements(scene_path, catalog_path))

def run_interactive():
    import rhinoscriptsyntax as rs
    scene = rs.OpenFileName('Select FMP scene manifest', 'JSON Files (*.json)|*.json||')
    if not scene:
        return
    catalog = rs.OpenFileName('Select FMP marker catalog', 'JSON Files (*.json)|*.json||')
    if not catalog:
        return
    result = import_markers(scene, catalog)
    print('FMP Rhino preview: %d added, %d existing' % (result['added'], result['skipped_existing']))

if __name__ == '__main__':
    run_interactive()
