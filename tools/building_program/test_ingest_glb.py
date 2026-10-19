"""Portable tests: cd tools/building_program; python -m unittest -v test_ingest_glb.
Requires trimesh and numpy. Uses synthetic GLB geometry, not a private model.
"""
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import trimesh
from ingest_glb import inspect, stage_csv, read_csv, FIELDS, ENV_FIELDS, MEDIA_FIELDS, LINK_FIELDS

class TestPortableGLBInspector(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        scene = trimesh.Scene()
        scene.add_geometry(trimesh.creation.box(extents=(4,8,6)),node_name='SHELL',
                           geom_name='shell_geom',
                           transform=trimesh.transformations.translation_matrix([10,5,0]))
        scene.add_geometry(trimesh.creation.box(extents=(1,1,1)),node_name='STEEL_OPTIONAL',
                           geom_name='steel_geom',
                           transform=trimesh.transformations.translation_matrix([60,0,0]))
        self.path=self.root/'test.glb'
        self.path.write_bytes(scene.export(file_type='glb'))
        self.sha=hashlib.sha256(self.path.read_bytes()).hexdigest()

    def tearDown(self): self.tmp.cleanup()

    def test_select_shell_ignores_remote_optional_steel(self):
        result=inspect(self.path,'WF0001',1939,'Y','RELEASE',select=['SHELL'],expected_sha=self.sha)
        self.assertEqual(result['selected_components'],1)
        self.assertAlmostEqual(float(result['bounds_m'][0]),8.0,places=4)
        self.assertAlmostEqual(float(result['bounds_m'][3]),12.0,places=4)
        self.assertEqual(result['envelope']['site_registered'],0)
        self.assertEqual(result['watertight_components'],1)

    def test_all_meshes_include_both_parts(self):
        result=inspect(self.path,'WF0001',1939,'Y','RELEASE')
        self.assertEqual(result['selected_components'],2)
        self.assertAlmostEqual(float(result['bounds_m'][3]),60.5,places=4)
        self.assertEqual(result['selected_faces'],24)

    def test_stable_ids_and_hash_for_identical_input(self):
        a=inspect(self.path,'WF0002',1939,'Y','ASSET',select=['SHELL'])
        b=inspect(self.path,'WF0002',1939,'Y','ASSET',select=['SHELL'])
        self.assertEqual(a['components'][0]['component_id'],b['components'][0]['component_id'])
        self.assertEqual(a['source_sha256'],self.sha)
        self.assertEqual(hashlib.sha256(self.path.read_bytes()).hexdigest(),self.sha)

    def test_stale_sha_rejected(self):
        with self.assertRaisesRegex(ValueError,'Source hash mismatch'):
            inspect(self.path,'WF0002',1939,'Y','ASSET',expected_sha='0'*64)

    def test_unregistered_node_rejected(self):
        with self.assertRaisesRegex(ValueError,'Requested nodes missing'):
            inspect(self.path,'WF0002',1939,'Y','ASSET',select=['NOT_HERE'])

    def test_stage_csv_idempotent(self):
        result=inspect(self.path,'WF0001',1939,'Y','RELEASE',select=['SHELL'])
        dest=self.root/'master_model_components.csv'
        stage_csv(dest,FIELDS,result['components'],'component_id')
        old=dest.read_bytes()
        stage_csv(dest,FIELDS,result['components'],'component_id')
        self.assertEqual(old,dest.read_bytes())
        self.assertEqual(len(read_csv(dest,FIELDS)),1)

    def test_cli_produces_all_four_catalogs(self):
        out=self.root/'generated'
        cmd=[sys.executable,str(Path(__file__).with_name('ingest_glb.py')),
             '--glb',str(self.path),'--building','WF0001','--year','1939',
             '--up','Y','--asset-id','RELEASE','--node','SHELL','--out',str(out)]
        subprocess.run(cmd,check=True,capture_output=True)
        for name,columns in (('master_model_components.csv',FIELDS),
                             ('master_building_envelopes.csv',ENV_FIELDS),
                             ('master_media_assets.csv',MEDIA_FIELDS),
                             ('master_building_media.csv',LINK_FIELDS)):
            self.assertEqual(len(read_csv(out/name,columns)),1)

if __name__=='__main__':unittest.main()
