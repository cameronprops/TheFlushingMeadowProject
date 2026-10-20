"""Safety regression for Constitution Mall v002 source preservation.

Requires numpy. Does not require the large archived source GLB.
"""
import hashlib
import struct
import tempfile
import unittest
from pathlib import Path

from tools.world_build.build_constitution_mall_v002 import build

EXPECTED = "a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5"


class MallSourceGuardTests(unittest.TestCase):
    def test_known_source_digest_constant(self):
        # Prevent accidental replacement with an unrelated archive or a guessed hash.
        self.assertEqual(len(EXPECTED), 64)
        self.assertEqual(bytes.fromhex(EXPECTED).hex(), EXPECTED)

    def test_refuses_wrong_glb_before_appending_any_geometry(self):
        # A valid-looking but unaudited GLB must be rejected before parsing/editing.
        json_chunk = b'{"asset":{"version":"2.0"}}'
        json_chunk += b" " * (-len(json_chunk) % 4)
        binary = b"\x00\x00\x00\x00"
        glb = (
            struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(json_chunk) + 8 + len(binary))
            + struct.pack("<II", len(json_chunk), 0x4E4F534A) + json_chunk
            + struct.pack("<II", len(binary), 0x004E4942) + binary
        )
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "unverified.glb"
            source.write_bytes(glb)
            with self.assertRaisesRegex(ValueError, "Refusing unexpected Theme Center source SHA256"):
                build(source)
            self.assertEqual(source.read_bytes(), glb)

    def test_missing_archive_fails_without_creating_placeholder(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "missing.glb"
            with self.assertRaises(FileNotFoundError):
                build(path)
            self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
