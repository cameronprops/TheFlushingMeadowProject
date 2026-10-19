"""Unreal Editor Python preview TargetPoint importer, target UE 5.x.

Requires Python Editor Script Plugin. Unverified in native Unreal host.
"""
from fmp_marker_core import read_placements

def apply_to_level(unreal, placements):
    subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    if subsystem is None:
        raise RuntimeError('EditorActorSubsystem is unavailable')
    existing = set()
    for actor in subsystem.get_all_level_actors():
        for tag in actor.get_editor_property('tags'):
            value = str(tag)
            if value.startswith('FMP_MARKER_ID='):
                existing.add(value[len('FMP_MARKER_ID='):])
    added = skipped = 0
    for p in placements:
        if p['id'] in existing:
            skipped += 1
            continue
        x, y, z = p['unreal_cm']
        actor = subsystem.spawn_actor_from_class(unreal.TargetPoint, unreal.Vector(x, y, z))
        if actor is None:
            raise RuntimeError('Unable to spawn Unreal TargetPoint ' + p['id'])
        actor.set_actor_label('FMP_PREVIEW_' + p['id'])
        actor.set_folder_path(unreal.Name('FMP_PREVIEW/' + p['source_map_id']))
        actor.set_editor_property('tags', [
            unreal.Name('FMP_PREVIEW'), unreal.Name('FMP_MARKER_ID=' + p['id']),
            unreal.Name('FMP_MAP_ID=' + p['source_map_id']),
            unreal.Name('FMP_HEIGHT_UNRESOLVED'), unreal.Name(p['data_class'])
        ])
        existing.add(p['id'])
        added += 1
    return {'added': added, 'skipped_existing': skipped}

def import_markers(scene_path, catalog_path):
    import unreal
    result = apply_to_level(unreal, read_placements(scene_path, catalog_path))
    unreal.log('FMP preview markers: %d added, %d existing' %
               (result['added'], result['skipped_existing']))
    return result

# In Unreal Python console:
# import sys; sys.path.append('/repo/tools/georeferencing/importers')
# import fmp_import_unreal_editor as fmp
# fmp.import_markers('/full/path/scene.json', '/full/path/markers.json')
