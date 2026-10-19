-- FMP 009 (2026-10-19). Correct the user-identified rotating "pyramid" lead.
-- The Ford Cycle of Production was an exhibit WITHIN the 1939-40 Ford Exposition,
-- not an independent tower or another pavilion.
-- Run AFTER import of archive_inventory_candidates and building_evidence.
UPDATE unidentified_visual_leads
 SET status='MATCH_CONFIRMED',
     candidate_building_id='WF0014',
     reference_url='https://www.thehenryford.org/collections/explore/artifact/47282',
     feature_motion='TIERED_PLATFORM_ROTATES_FLOATING_ON_PONTOONS_IN_WATER_MOAT',
     notes='Identified by owner as Ford Exposition. Independent archival museum evidence: Ford Cycle of Production 1939-1940; rotating tiered platform floats on pontoons in moat; 87 working models; 142 figures; 27 raw materials. Exhibit nested inside Ford pavilion, not separate tower. Feature ID FORD39_CYCLE_OF_PRODUCTION.'
 WHERE lead_id='FMP-VIS-ROTATING-PYRAMID-01';
UPDATE building_dossiers
 SET production_priority='P1',
 notes='1939 Ford Exposition with Road of Tomorrow and source-documented nested Cycle of Production rotating waterborne industrial diorama exhibit. Pavilion footprint, hall location, tier size and rotation rate remain unregistered.'
 WHERE building_id='WF0014';
