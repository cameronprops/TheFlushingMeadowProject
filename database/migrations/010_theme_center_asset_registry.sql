-- FMP 010 - Preserve existing Theme Center reconstruction as the central asset family.
-- Applied after catalogs and other prioritization migrations.
CREATE TABLE IF NOT EXISTS building_linked_places(
 link_id TEXT PRIMARY KEY,
 building_id TEXT NOT NULL REFERENCES building_dossiers(building_id),
 place_id TEXT NOT NULL REFERENCES places(place_id),
 link_type TEXT NOT NULL CHECK(link_type IN ('SHARED_THEME_ASSEMBLY','NESTED_EXHIBIT','GUEST_CIRCULATION','SHARED_SITE_ENVIRONMENT')),
 source_model_url TEXT,
 source_model_sha256 TEXT,
 status TEXT NOT NULL,
 notes TEXT
);
INSERT INTO building_linked_places(link_id,building_id,place_id,link_type,source_model_url,source_model_sha256,status,notes) VALUES
('FMP-TC-TR-EXTERIOR','WF0001','WF0001','SHARED_THEME_ASSEMBLY','https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view','a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5','LEGACY_MODEL_PRESERVED','Trylon existing in 510-node staging GLB; verified Y-up height 610ft; base is provisional'),
('FMP-TC-PS-EXTERIOR','WF0002','WF0002','SHARED_THEME_ASSEMBLY','https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view','a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5','LEGACY_MODEL_PRESERVED','Perisphere upper/lower shells, 8 supports, 32 meridians, 15 latitude trusses'),
('FMP-TC-PS-DEMO','WF0002','WF0003','NESTED_EXHIBIT','https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view','a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5','PROVISIONAL_DEMOCRACITY_MODEL','Partly interpretive interior diorama with ~293 descendant graph nodes; separate full-scale future world is different authored scene'),
('FMP-TC-PS-HELIX','WF0002','WF0004','GUEST_CIRCULATION','https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view','a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5','PROVISIONAL_PLAN_SOLVED_LENGTH','Helicline separately modeled; 950ft centerline target in legacy builder, plan angle and supports provisional'),
('FMP-TC-PS-GROUND','WF0002','WF0005','SHARED_SITE_ENVIRONMENT','https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view','a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5','INTERPRETIVE_LANDSCAPE','Fountains and plazas are impressions pending period site plan registration');
UPDATE building_dossiers
 SET production_priority='P1',baseline_model_status='EXISTING_TRUTH_GATED_RECONSTRUCTION',notes='610-foot built Trylon; preserve source 510-node shared Theme Center GLB and original StructureGraph/BIM workbook. Site registration and final portal sections outstanding.'
 WHERE building_id='WF0001';
UPDATE building_dossiers
 SET production_priority='P1',baseline_model_status='EXISTING_TRUTH_GATED_RECONSTRUCTION',notes='180-foot built Perisphere; existing 510-node shared model includes Democracity, Helicline, shell, frame. 200ft original proposal not built. Walkable guest path not engine-tested.'
 WHERE building_id='WF0002';
