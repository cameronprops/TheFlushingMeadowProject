import tempfile, unittest
from pathlib import Path
import numpy as np
from tools.world_build.inspect_theme_center_bridge_entry_v001 import SHA,NODES,xy_hull,run
class BridgeEntryEvidenceTests(unittest.TestCase):
 def test_hash_locked(self):self.assertEqual(len(SHA),64)
 def test_nodes_named(self):
  self.assertEqual(NODES['bridge'],'Return_Bridge_Deck')
  self.assertEqual(NODES['lobby'],'Trylon_Lobby_Floor_Envelope')
 def test_other_source_refused(self):
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'fake.glb';f.write_bytes(b'not an archived GLB')
   with self.assertRaisesRegex(ValueError,'Unknown runtime GLB SHA256'):run(f,Path(d)/'out')
 def test_actual_vertex_hull(self):
  a=np.array([[0,0,1],[2,0,1],[2,3,1],[0,3,1],[1,2,1]])
  self.assertEqual(set(map(tuple,xy_hull(a))),{(0.,0.),(2.,0.),(2.,3.),(0.,3.)})
if __name__=='__main__':unittest.main()
