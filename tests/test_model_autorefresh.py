"""Test versioned automatic GLB intake without altering historical evidence.
Run: python3 -m unittest -v tests.test_model_autorefresh
Requires numpy and trimesh. Uses synthetic meshes, no Internet.
"""
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import trimesh
from tools.building_program.refresh_model_catalog import (
    refresh_registered_models, TABLE_FILES, read_csv,
)

class TestGLBRevisionWatcher(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.catalog=self.root/'catalog'
        self.models=self.root/'models/incoming'
        self.catalog.mkdir()
        self.models.mkdir(parents=True)
        for filename,fields,key in TABLE_FILES:
            (self.catalog/filename).write_text(','.join(fields)+'\n')
        self.glb=self.models/'pavilion.glb'
        self.manifest=self.models/'pavilion.fmp-model.json'
        self.save_mesh(2)
        self.manifest.write_text(json.dumps(dict(building_id='WF0001',year=1939,
            up='Y',role='EXTERIOR_SHELL',glb='pavilion.glb',nodes=['SHELL'])))
    def tearDown(self):
        self.tmp.cleanup()
    def save_mesh(self,width):
        scene=trimesh.Scene()
        scene.add_geometry(trimesh.creation.box(extents=(width,3,4)),
                           node_name='SHELL')
        scene.add_geometry(trimesh.creation.box(extents=(1,1,1)),
                           node_name='OPTIONAL_STEEL')
        self.glb.write_bytes(scene.export(file_type='glb'))
    def rows(self,name):
        cols=next(fields for filename,fields,key in TABLE_FILES if name==filename)
        return read_csv(self.catalog/name,cols)
    def refresh(self):
        return refresh_registered_models(self.models,self.catalog,repo_root=self.root,
                                         observed_utc='2026-10-19T12:00:00Z')
    def test_observes_only_selected_shell(self):
        result=self.refresh()
        self.assertEqual(result['changed'],1)
        self.assertEqual(result['components_added'],1)
        self.assertEqual(len(self.rows('master_model_components.csv')),1)
        self.assertEqual(float(self.rows('master_building_envelopes.csv')[0]['max_x_m']),1.0)
    def test_idempotent(self):
        self.refresh()
        before={p.name:p.read_bytes() for p in self.catalog.iterdir()}
        self.assertEqual(self.refresh()['changed'],0)
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.catalog.iterdir()})
    def test_replaces_current_pointer_but_retains_history(self):
        self.refresh()
        old=self.rows('master_active_model_releases.csv')[0]['active_media_id']
        self.save_mesh(5)
        self.assertEqual(self.refresh()['changed'],1)
        rows=self.rows('master_model_components.csv')
        self.assertEqual(len(rows),2)
        self.assertEqual(len(self.rows('master_media_assets.csv')),2)
        new=self.rows('master_active_model_releases.csv')[0]['active_media_id']
        self.assertNotEqual(old,new)
        self.assertIn(old,[m['media_id'] for m in self.rows('master_media_assets.csv')])
    def test_selection_edit_creates_new_version(self):
        self.refresh()
        manifest=json.loads(self.manifest.read_text())
        manifest['nodes']=['OPTIONAL_STEEL']
        self.manifest.write_text(json.dumps(manifest))
        self.assertEqual(self.refresh()['changed'],1)
        self.assertEqual(len(self.rows('master_media_assets.csv')),2)
    def test_missing_node_rejected_with_no_catalog_edits(self):
        self.refresh()
        before={p.name:p.read_bytes() for p in self.catalog.iterdir()}
        manifest=json.loads(self.manifest.read_text())
        manifest['nodes']=['MISSING']
        self.manifest.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError,'Requested nodes missing'):
            self.refresh()
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.catalog.iterdir()})
    def test_duplicate_active_release_rejected_without_mutation(self):
        self.refresh()
        before={p.name:p.read_bytes() for p in self.catalog.iterdir()}
        (self.models/'second.fmp-model.json').write_bytes(self.manifest.read_bytes())
        with self.assertRaisesRegex(ValueError,'Duplicate active source role'):
            self.refresh()
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.catalog.iterdir()})
    def test_unregistered_glb_is_not_scanned(self):
        self.refresh()
        (self.models/'random.glb').write_bytes(self.glb.read_bytes())
        self.assertEqual(self.refresh()['changed'],0)
    def test_absent_directory_noop(self):
        result=refresh_registered_models(self.root/'none',self.catalog)
        self.assertEqual(result['status'],'NO_REGISTERED_MODELS')
if __name__=='__main__':
    unittest.main()
