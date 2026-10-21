import copy
import tempfile
import unittest
from pathlib import Path
from validation_gate import require_clear, sha256

class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.asset = Path(self.tmp.name) / 'scene.glb'
        self.asset.write_bytes(b'fixture')
        self.report = dict(asset_sha256=sha256(self.asset), preservation='PASS',
                           added_solids='PASS', brace_jamb_connections='PASS',
                           screens=[dict(portal='A', poses=51, sphere_samples=663, surface_contacts=[])])
    def test_current_clear_report_passes(self):
        require_clear(self.report, self.asset, ['A'])
    def test_changed_asset_rejected(self):
        self.asset.write_bytes(b'changed')
        with self.assertRaises(ValueError): require_clear(self.report, self.asset, ['A'])
    def test_collision_rejected(self):
        self.report['screens'][0]['surface_contacts'] = [{'node':'wall'}]
        with self.assertRaises(ValueError): require_clear(self.report, self.asset, ['A'])
    def test_missing_duplicate_and_incomplete_screens_rejected(self):
        for screens in ([], self.report['screens'] * 2, [dict(portal='A', poses=1, sphere_samples=13, surface_contacts=[])]):
            report = copy.deepcopy(self.report); report['screens'] = screens
            with self.assertRaises(ValueError): require_clear(report, self.asset, ['A'])
    def test_missing_hash_or_contact_result_rejected(self):
        for key in ('asset_sha256','surface_contacts'):
            report=copy.deepcopy(self.report)
            if key=='asset_sha256': del report[key]
            else: del report['screens'][0][key]
            with self.assertRaises(ValueError): require_clear(report,self.asset,['A'])
    def test_failed_geometry_rejected(self):
        self.report['added_solids']='FAIL'
        with self.assertRaises(ValueError): require_clear(self.report,self.asset,['A'])

if __name__ == '__main__': unittest.main()
