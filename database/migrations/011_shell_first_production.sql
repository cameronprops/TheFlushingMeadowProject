-- FMP 011: Shell-first production. Structural detailing is optional, never an
-- acceptance prerequisite for cinematic or 3D-printed pavilion shells.
-- Previous as-built evidence and full complex CAD model are retained unchanged.
CREATE TABLE IF NOT EXISTS building_reconstruction_policy (
  building_id TEXT PRIMARY KEY REFERENCES building_dossiers(building_id),
  exterior_shell_priority TEXT NOT NULL DEFAULT 'REQUIRED_FIRST',
  interior_shell_priority TEXT NOT NULL DEFAULT 'PUBLIC_SPACES_WHEN_SCOPED',
  printed_shell_priority TEXT NOT NULL DEFAULT 'OPTIONAL_DELIVERABLE',
  structural_frame_priority TEXT NOT NULL DEFAULT 'OPTIONAL_DOCUMENT_IF_SOURCED',
  steel_construction_animation TEXT NOT NULL DEFAULT 'FUTURE_OPTION',
  shell_source_strategy TEXT NOT NULL DEFAULT 'PRESERVE_EXACT_SOURCE_MESH_IF_AVAILABLE',
  shell_collision_qa TEXT NOT NULL DEFAULT 'NATIVE_UNREAL_TEST_PENDING',
  print_minimum_wall_qa TEXT NOT NULL DEFAULT 'SLICER_AND_PHYSICAL_CHECK_PENDING',
  note TEXT
);
INSERT INTO building_reconstruction_policy(building_id)
 SELECT building_id FROM building_dossiers
 WHERE building_id NOT IN (SELECT building_id FROM building_reconstruction_policy);
CREATE TRIGGER IF NOT EXISTS trg_shell_policy_on_new_dossier
AFTER INSERT ON building_dossiers
BEGIN
  INSERT INTO building_reconstruction_policy(building_id) VALUES (NEW.building_id);
END;
CREATE TABLE IF NOT EXISTS building_shell_parts (
  part_id TEXT PRIMARY KEY,
  building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
  period_year INTEGER NOT NULL CHECK(period_year IN (1939,1940,1964,1965,2026)),
  role TEXT NOT NULL CHECK(role IN (
   'EXTERIOR_SHELL','INTERIOR_SHELL_AND_VIEWING','GUEST_CIRCULATION_PREVIEW',
   'OPTIONAL_STEEL_STRUCTURE','PRINT_SHELL_SAMPLE')),
  source_model_uri TEXT,
  source_sha256 TEXT,
  exact_source_node TEXT NOT NULL,
  construction_status TEXT NOT NULL,
  import_status TEXT NOT NULL DEFAULT 'NOT_NATIVE_HOST_TESTED',
  print_scale_denominator INTEGER,
  wall_thickness_verified INTEGER NOT NULL DEFAULT 0 CHECK(wall_thickness_verified IN (0,1)),
  historical_certified INTEGER NOT NULL DEFAULT 0 CHECK(historical_certified IN (0,1)),
  notes TEXT
);
CREATE INDEX IF NOT EXISTS ix_fmp_shell_parts ON building_shell_parts(building_id,role,period_year);
-- Exact original GLB node names. Exports do not alter the original asset.
INSERT INTO building_shell_parts
(part_id,building_id,period_year,role,source_model_uri,source_sha256,exact_source_node,construction_status,notes)
VALUES
('FMP-TC-TR-EXTERIOR-v1','WF0001',1939,'EXTERIOR_SHELL',
 'https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view',
 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5',
 'Trylon_Hollow_Exterior','EXTRACTED_WATERTIGHT', '610ft full-height shell; footprint still interpretive'),
('FMP-TC-PS-UPPER-v1','WF0002',1939,'EXTERIOR_SHELL',
 'https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view',
 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5',
 'Perisphere_Upper_Removable_Shell','EXTRACTED_WATERTIGHT', 'Top hemisphere; period external diameter 180ft'),
('FMP-TC-PS-LOWER-v1','WF0002',1939,'EXTERIOR_SHELL',
 'https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view',
 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5',
 'Perisphere_Lower_Removable_Shell','EXTRACTED_WATERTIGHT', 'Lower hemisphere; separate shell/lid assembly'),
('FMP-TC-PS-LINER-v1','WF0002',1939,'INTERIOR_SHELL_AND_VIEWING',
 'https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view',
 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5',
 'Interior_Projection_Liner','EXTRACTED_PREVIEW', 'Immersive interior projection surface; no Unreal materials yet'),
('FMP-TC-PS-PLATFORM1-v1','WF0002',1939,'INTERIOR_SHELL_AND_VIEWING',
 'https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view',
 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5',
 'Moving_Platform_1','EXTRACTED_PREVIEW', 'Provisional viewing platform; guest circulation NOT tested'),
('FMP-TC-PS-PLATFORM2-v1','WF0002',1939,'INTERIOR_SHELL_AND_VIEWING',
 'https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view',
 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5',
 'Moving_Platform_2','EXTRACTED_PREVIEW', 'Provisional moving guest platform; animation not validated'),
('FMP-TC-PS-HELICLINE-v1','WF0002',1939,'GUEST_CIRCULATION_PREVIEW',
 'https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view',
 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5',
 'Helicline_Deck_and_Curved_Soffit','EXTRACTED_PREVIEW', '950ft historic length, site layout provisional'),
('FMP-TC-PS-BRIDGE-v1','WF0002',1939,'GUEST_CIRCULATION_PREVIEW',
 'https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view',
 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5',
 'Return_Bridge_Deck','EXTRACTED_PREVIEW', 'Landing and bridge widths provisional'),
('FMP-TC-TR-STEEL-F1-v1','WF0001',1939,'OPTIONAL_STEEL_STRUCTURE',
 'https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view',
 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5',
 'Trylon_Face_1_Frame','OPTIONAL_SOURCE_PREVIEW', 'For future exposed-structure and construction animation'),
('FMP-TC-PS-STRUCTURE-RING-v1','WF0002',1939,'OPTIONAL_STEEL_STRUCTURE',
 'https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view',
 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5',
 'Perisphere_Support_Ring','OPTIONAL_SOURCE_PREVIEW', 'Preserved 72ft original ring girder family; exact section unverified');
UPDATE building_dossiers
SET baseline_model_status='EXISTING_SHELL_FIRST_ASSET_EXPORTS',
    notes='Existing 510-node source preserved. Exterior/interior shells exported independently; optional steel for historical engineering/construction animation; 3D print sample not slicer or Unreal validated.'
WHERE building_id IN ('WF0001','WF0002');
