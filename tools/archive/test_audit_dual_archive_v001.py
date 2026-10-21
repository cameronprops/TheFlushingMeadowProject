"""Hermetic regression tests for FMP's retroactive two-copy acceptance gate."""
import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.archive.audit_dual_archive_v001 import audit, inspect_artifact, safe_relpath


def sha(data):
    return hashlib.sha256(data).hexdigest()


class DualArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.drive = self.root / 'drive'; self.drive.mkdir()
        self.git = self.root / 'git'; self.git.mkdir()
        self.data = b'reproducible FMP data\n'
        self.a = {'id': 'example', 'filename': 'example.bin', 'drive_relpath': 'example.bin',
                  'git_binary_path': 'archive/example.bin', 'drive_file_id': 'real-drive-id',
                  'sha256': sha(self.data), 'size_bytes': len(self.data), 'public_git_rights': 'allowed'}

    def test_no_endpoint_is_unrecovered(self):
        self.assertEqual(inspect_artifact(self.a,self.drive,self.git)['status'],'UNRECOVERED')

    def test_drive_only_is_not_double_archived(self):
        (self.drive/'example.bin').write_bytes(self.data)
        self.assertEqual(inspect_artifact(self.a,self.drive,self.git)['status'],'GIT_BINARY_PENDING')

    def test_actual_matching_copies_pass(self):
        (self.drive/'example.bin').write_bytes(self.data)
        (self.git/'archive').mkdir()
        (self.git/'archive/example.bin').write_bytes(self.data)
        self.assertEqual(inspect_artifact(self.a,self.drive,self.git)['status'],'BOTH_LOCAL_COPIES_MATCH')

    def test_changed_git_bytes_cannot_pass(self):
        (self.drive/'example.bin').write_bytes(self.data)
        (self.git/'archive').mkdir()
        (self.git/'archive/example.bin').write_bytes(b'wrong')
        self.assertEqual(inspect_artifact(self.a,self.drive,self.git)['status'],'INTEGRITY_FAILURE')

    def test_changed_drive_bytes_cannot_pass(self):
        (self.drive/'example.bin').write_bytes(b'wrong')
        self.assertEqual(inspect_artifact(self.a,self.drive,self.git)['status'],'INTEGRITY_FAILURE')

    def test_blocked_rights_never_pass_public_git(self):
        self.a['public_git_rights'] = 'blocked'
        (self.drive/'example.bin').write_bytes(self.data)
        self.assertEqual(inspect_artifact(self.a,self.drive,self.git)['status'],'BLOCKED_RIGHTS')

    def test_unsafe_parent_escape_refused(self):
        self.a['drive_relpath'] = '../elsewhere.bin'
        with self.assertRaises(ValueError): inspect_artifact(self.a,self.drive,self.git)

    def test_windows_path_refused(self):
        with self.assertRaises(ValueError): safe_relpath(r'..\outside')

    def test_zip_exact_members_and_hashes(self):
        path = self.drive/'example.bin'
        with zipfile.ZipFile(path,'w') as z:
            z.writestr('tools/script.py', b'print(1)\n')
        package = path.read_bytes()
        self.a['sha256']=sha(package); self.a['size_bytes']=len(package)
        self.a['members']=[{'path':'tools/script.py','sha256':sha(b'print(1)\n'),'size_bytes':9}]
        self.assertEqual(inspect_artifact(self.a,self.drive,self.git)['status'],'GIT_BINARY_PENDING')

    def test_zip_member_checksum_failure_detected(self):
        path = self.drive/'example.bin'
        with zipfile.ZipFile(path,'w') as z:
            z.writestr('tools/script.py', b'print(1)\n')
        package = path.read_bytes()
        self.a['sha256']=sha(package); self.a['size_bytes']=len(package)
        self.a['members']=[{'path':'tools/script.py','sha256':sha(b'bad'),'size_bytes':9}]
        self.assertEqual(inspect_artifact(self.a,self.drive,self.git)['status'],'INTEGRITY_FAILURE')

    def test_schema_reject(self):
        with self.assertRaisesRegex(ValueError,'schema'):
            audit({'schema':'wrong','artifacts':[]},self.drive,self.git)


if __name__ == '__main__':
    unittest.main()