"""Synthetic, host-independent tests for the FMP preview import adapters."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from fmp_marker_core import make_placements, load_json
from fmp_export_worldwright import encode_dxf, export_worldwright
from fmp_import_rhino8 import apply_to_doc
from fmp_import_unreal_editor import apply_to_level

FIX = Path(__file__).resolve().parent.parent / 'fixtures'
SCENE = FIX / 'SYNTHETIC_Scene_v1.json'
MARKERS = FIX / 'SYNTHETIC_Marker_Catalog_v1.json'

class WorldwrightTests(unittest.TestCase):
    def setUp(self):
        self.points = make_placements(load_json(SCENE), load_json(MARKERS))

    def test_source_transform(self):
        self.assertEqual(len(self.points), 4)
        self.assertAlmostEqual(self.points[0]['local_m'][0], -50.0)
        self.assertAlmostEqual(self.points[0]['local_m'][1], -25.0)
        self.assertAlmostEqual(self.points[1]['local_m'][0], -15.0)
        self.assertAlmostEqual(self.points[2]['local_m'][1], 10.0)

    def test_dxf_unit_and_entities(self):
        dxf = encode_dxf(self.points)
        self.assertIn('$INSUNITS\n70\n6\n', dxf)
        self.assertIn('2\nFMP_SYNTHETIC_1939\n', dxf)
        self.assertEqual(dxf.count('0\nPOINT\n'), 4)
        self.assertEqual(dxf.count('0\nLINE\n'), 8)
        self.assertEqual(dxf.count('0\nTEXT\n'), 4)
        self.assertTrue(dxf.endswith('0\nEOF\n'))

    def test_export_sidecar_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path, side = export_worldwright(SCENE, MARKERS, Path(tmp)/'preview.dxf')
            data = json.loads(side.read_text())
            self.assertEqual(data['height_status'], 'UNRESOLVED_PREVIEW_Z0')
            self.assertEqual(data['horizontal_crs'], 'EPSG:32118')
            self.assertEqual(len(data['dxf_sha256']), 64)
            self.assertEqual(len(data['placements']), 4)
            self.assertIn(b'0\nPOINT\n', path.read_bytes())

    def test_height_rejected(self):
        bad = [dict(self.points[0], local_m=[-50., -25., 6.])]
        with self.assertRaises(ValueError):
            encode_dxf(bad)

    def test_fictional_class_rejected(self):
        bad = [dict(self.points[0], data_class='FICTIONAL_WORLD_ASSET')]
        with self.assertRaises(ValueError):
            encode_dxf(bad)

    def test_duplicates_rejected(self):
        with self.assertRaises(ValueError):
            encode_dxf([self.points[0], self.points[0]])

    def test_refuse_fake_dftba(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                export_worldwright(SCENE, MARKERS, Path(tmp)/'fake.dftba')

    def test_bad_numeric_fit_rejected(self):
        scene = load_json(SCENE)
        scene['maps']['SYNTHETIC_1939']['qa']['status'] = 'NUMERIC_FAIL'
        with self.assertRaises(ValueError):
            make_placements(scene, load_json(MARKERS))

class FakeRhinoLayer:
    def __init__(self):
        self.Name = ''
        self.Index = -1

class FakeAttr:
    def __init__(self):
        self._u = {}
        self.Name = ''
        self.LayerIndex = 0
    def SetUserString(self, k, v): self._u[k] = v
    def GetUserString(self, k): return self._u.get(k)

class FakeObject:
    def __init__(self, attributes): self.Attributes = attributes

class FakeLayers:
    def __init__(self): self.items = {}
    def FindName(self, name): return self.items.get(name)
    def Add(self, layer):
        layer.Index = len(self.items)
        self.items[layer.Name] = layer
        return layer.Index

class FakeRhinoDoc:
    ModelUnitSystem = 'Meters'
    def __init__(self):
        self.Layers = FakeLayers()
        self.Objects = self
        self.objects = []
        self.Views = SimpleNamespace(Redraw=lambda: None)
    def __iter__(self): return iter(self.objects)
    def AddPoint(self, point, attr):
        self.objects.append(FakeObject(attr))
        return '00000000-0000-0000-0000-000000000001'

class HostMockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.points = make_placements(load_json(SCENE), load_json(MARKERS))

    def test_rhino_idempotence(self):
        doc = FakeRhinoDoc()
        types = SimpleNamespace(Layer=FakeRhinoLayer, ObjectAttributes=FakeAttr)
        rhino = SimpleNamespace(
            UnitSystem=SimpleNamespace(Meters='Meters', CustomUnits='CustomUnits'),
            RhinoMath=SimpleNamespace(UnitScale=lambda a,b: 1.0),
            DocObjects=types, Geometry=SimpleNamespace(Point3d=lambda x,y,z: (x,y,z)))
        first = apply_to_doc(doc, rhino, self.points)
        second = apply_to_doc(doc, rhino, self.points)
        self.assertEqual(first['added'], 4)
        self.assertEqual(second['skipped_existing'], 4)
        self.assertEqual(len(doc.objects), 4)

    def test_unreal_idempotence(self):
        class Actor:
            def __init__(self): self.tags = []
            def get_editor_property(self,k): return getattr(self,k)
            def set_editor_property(self,k,v): setattr(self,k,v)
            def set_actor_label(self,x): self.label=x
            def set_folder_path(self,x): self.folder=x
        class Subsystem:
            def __init__(self): self.actors = []
            def get_all_level_actors(self): return self.actors
            def spawn_actor_from_class(self,klass,position):
                actor=Actor(); actor.position=position
                self.actors.append(actor)
                return actor
        subsystem=Subsystem()
        unreal=SimpleNamespace(EditorActorSubsystem=object(),
                               get_editor_subsystem=lambda k: subsystem,
                               Name=lambda v:v, Vector=lambda x,y,z: (x,y,z), TargetPoint=Actor)
        self.assertEqual(apply_to_level(unreal,self.points)['added'],4)
        self.assertEqual(apply_to_level(unreal,self.points)['skipped_existing'],4)
        self.assertEqual(subsystem.actors[0].position,(-5000.,-2500.,0.))

if __name__=='__main__':
    unittest.main()
