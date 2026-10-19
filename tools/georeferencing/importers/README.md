# FMP preview import: Rhino 8, Unreal Editor, Worldwright

Three adapters use the common fmp.georef.scene.v1 coordinate manifest and fmp.markers.v1 catalog. All results are horizontally aligned *preview markers*, not certified historic surveying or completed 3D reconstructions. Z=0 remains an annotation plane.

Canonical frame: EPSG:32118, metres, local X east, local Y north.
Rhino uses native unit scaling; Unreal uses centimetres; Worldwright DXF is explicitly in metres (INSUNITS=6).

## Local verification

From the FMP repository root:

    python3 tools/georeferencing/importers/fmp_marker_core.py tools/georeferencing/fixtures/SYNTHETIC_Scene_v1.json tools/georeferencing/fixtures/SYNTHETIC_Marker_Catalog_v1.json --output /tmp/fmp-preview.json
    python3 tools/georeferencing/importers/fmp_export_worldwright.py tools/georeferencing/fixtures/SYNTHETIC_Scene_v1.json tools/georeferencing/fixtures/SYNTHETIC_Marker_Catalog_v1.json --output /tmp/fmp-preview.dxf
    cd tools/georeferencing/importers && python3 -m unittest -v test_importers

Worldwright output consists of fmp-preview.dxf plus audit sidecar fmp-preview.fmp.json. The DXF includes POINT entities, LINE crosshairs and TEXT IDs on FMP source-map layers. The sidecar records source classifications and a SHA-256 of the DXF.

From the separate Worldwright/BuilderCraft checkout (with Rust installed):

    cargo run -p cadcraft-cli -- info /tmp/fmp-preview.dxf
    cargo run -p cadcraft-cli -- convert /tmp/fmp-preview.dxf /tmp/fmp-preview.dftba

The latter relies on existing DXF read and .dftba save in the native app. Open DXF in a fresh drawing to avoid duplicate markers. The external sidecar is not embedded in .dftba. Native host import/round-trip is not yet verified.

Rhino 8: run fmp_import_rhino8.py in Python 3 editor with the importer directory on sys.path; invoke import_markers(scene_path,catalog_path) or its interactive file pickers. It adds tagged point objects on per-map FMP_PREVIEW layers, skipping existing marker IDs.

Unreal Editor 5.x: enable Python Editor Script Plugin, add the importers directory to sys.path, and call fmp_import_unreal_editor.import_markers(scene_path,catalog_path). It adds tagged TargetPoint actors in per-map folders, skipping existing IDs. It does not change landscape, origin rebasing or terrain elevation.

Synthetic checks: 10 mocked/host-independent tests passed, and a generated DXF parsed with ezdxf 1.4.4 (16 entities, 4 points, 8 lines, 4 labels, zero audit errors). Rhino, Unreal, Worldwright native host tests are still outstanding.

Fictional future branches must not be labeled HISTORICAL_OBSERVATION. This importer accepts only SYNTHETIC_TEST_ONLY and HISTORICAL_OBSERVATION. Source rights, survey alignment and vertical datum remain separate gates.
