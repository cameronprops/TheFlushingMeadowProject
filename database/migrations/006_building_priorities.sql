-- FMP 006: author-controlled first-accessible-building production priorities.
-- Priority is a BUILD ORDER only; it never implies historic accuracy or readiness.
UPDATE building_dossiers SET production_priority='P1',public_access_status='INTERIOR_ALPHA_TARGET'
 WHERE building_id IN ('WF0002','WF0020','WF0009','WF0008');
UPDATE building_dossiers SET production_priority='P2'
 WHERE building_id IN ('WF0001','WF0012','WF0014','WF0024','WF0028','WF0030','WF0031','WF0056','WF0055');
UPDATE building_dossiers SET baseline_model_status='PROVISIONAL_MODEL_REUSE'
 WHERE building_id IN ('WF0001','WF0002');
UPDATE building_dossiers SET baseline_model_status='EXTERIOR_PROVISIONAL_GLTF',
 site_position_status='UNREGISTERED' WHERE building_id='WF0020';
UPDATE building_dossiers SET footprint_status='DRAWING_LEAD_UNTRACED'
 WHERE building_id IN ('WF0009','WF0028','WF0030','WF0031','WF0056');
INSERT INTO building_worklog
 (log_id,building_id,period_year,build_stage,status,asset_uri,notes,changed_utc)
 VALUES
 ('FMP-WLOG-WH-01','WF0020',1939,'EXTERIOR','PREVIEW_UNREGISTERED',
  'https://drive.google.com/file/d/1SC756j7deuJnPYIkjn_U9bcOV-GNSDd2/view',
  'Westinghouse 329-component schematic draft; archive ZIP and research dossier. No site placement or walkable interior validated.',
  '2026-10-18T23:00:00Z'),
 ('FMP-WLOG-PI-01','WF0002',1939,'EXTERIOR_AND_EXHIBIT','PREVIEW_UNREGISTERED',
  'https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view',
  '510-node existing Theme Center model includes Perisphere and Democracity; entrance, collision and navigability NOT engine-tested.',
  '2026-10-18T23:00:00Z');
