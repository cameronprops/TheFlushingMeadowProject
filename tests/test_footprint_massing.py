import copy
import sys
import unittest
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_footprint_massing import build


class MassingTests(unittest.TestCase):
    def data(self):
        return dict(units='m',coordinate_status='UNREGISTERED_LOCAL',objects=[dict(
            id='SYNTHETIC_TEST',year=1939,footprint=[[0,0],[4,0],[4,3],[0,3]],
            base_z=2,height=5,evidence_status='PROVISIONAL',source_refs=[])])

    def test_closed_oriented_mesh_and_volume(self):
        text,m=build(self.data());verts=[];faces=[]
        for line in text.splitlines():
            if line.startswith('v '):verts.append(list(map(float,line.split()[1:])))
            if line.startswith('f '):faces.append([int(v)-1 for v in line.split()[1:]])
        edges=Counter((f[i],f[(i+1)%3]) for f in faces for i in range(3))
        self.assertTrue(all(edges[(b,a)]==1 and count==1 for (a,b),count in edges.items()))
        volume=0
        for f in faces:
            a,b,c=[verts[i] for i in f]
            volume+=sum(a[i]*(b[(i+1)%3]*c[(i+2)%3]-b[(i+2)%3]*c[(i+1)%3]) for i in range(3))/6
        self.assertAlmostEqual(volume,60)
        self.assertEqual(m['objects'][0]['volume_m3'],60)

    def test_clockwise_and_closed_ring(self):
        d=self.data();d['objects'][0]['footprint'].reverse()
        d['objects'][0]['footprint'].append(d['objects'][0]['footprint'][0])
        self.assertEqual(build(d)[1]['objects'][0]['volume_m3'],60)

    def test_bad_geometry_and_evidence(self):
        for field,value in [('height',-1),('base_z',float('nan')),('evidence_status','SOURCE_BACKED'),
                            ('footprint',[[0,0],[4,0],[1,1],[0,4]])]:
            d=self.data();d['objects'][0][field]=value
            with self.assertRaises(ValueError):build(d)

    def test_duplicate_and_registration_guard(self):
        d=self.data();d['objects'].append(copy.deepcopy(d['objects'][0]))
        with self.assertRaises(ValueError):build(d)
        d=self.data();d['coordinate_status']='REGISTERED_LOCAL'
        with self.assertRaises(ValueError):build(d)


if __name__=='__main__':unittest.main()
