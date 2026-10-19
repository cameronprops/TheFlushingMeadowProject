-- FMP 008: historical building priorities and unresolved rotating object.
-- Run only AFTER the building subject and evidence catalogs are populated.
UPDATE building_dossiers SET production_priority='P2'
 WHERE building_id IN ('WF0012','FMP64SUBJ0064');
UPDATE building_dossiers
 SET classification='CONFIRMED_BUILDING',architecture_status='BUILDING_IDENTITY_DOCUMENTED',
 notes='GM Futurama II in 1964-65; distinct from 1939 Highways and Horizons. Period postcard describes 680-ft building, 110-ft canopy, 40-ft revolving indicator; no site registration yet.'
 WHERE building_id='FMP64SUBJ0064';
INSERT INTO unidentified_visual_leads
 (lead_id,working_description,status,candidate_building_id,reference_url,feature_motion,notes)
 VALUES ('FMP-VIS-ROTATING-PYRAMID-01',
 'Giant floating pyramid-like object that rotates at the fair',
 'UNIDENTIFIED',NULL,NULL,'ROTATING',
 'Owner-requested identity research. The 1964 GM roof indicator rotated but the description does not establish an actual pyramid; IBM theater also appeared suspended but was an ovoid. Neither is certified as the intended structure. Hold for image or confirmation.');
