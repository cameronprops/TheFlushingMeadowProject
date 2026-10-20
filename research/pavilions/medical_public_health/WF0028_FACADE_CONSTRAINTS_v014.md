# WF0028 v014: facade proportions and artwork controls
2026-10-20. Source-based constraint analysis, **not** a rebuilt GLB.

The previous 9 m high interpretive wall cannot accommodate the documented 36 ft high *Modern Medicine* mural at full scale. Its artwork height is 10.9728 m, requiring at least that much **local facade height if wholly placed on a wall**. The mural is 34 ft (10.3632 m) wide. This DOES NOT establish overall roof height or imply every wing must be enlarged. Source: https://www.hildrethmeiere.org/commissions/new-york-1939-worlds-fair-medicine-and-public-health-science-and-education-building-complex-south-facade

Other artwork constraints: *Primitive Man and Civilized Man* 30 × 15 ft, *Hippocrates* relief approximately 21 × 14 ft, *The Picnic* 110 × 14 ft. The 110-ft mural length measures artwork extent, NOT a full facade or footprint. Source references WF28-A031, A030 and A033.

The courtyard mural *Man between the Past and the Future* occupies a curved treatment in historical imagery, which cannot be represented faithfully by an unsupported rectangular wing alone. Source: https://www.hildrethmeiere.org/commissions/new-york-1939-worlds-fair-medicine-and-public-health-science-and-education-building-complex-facade-facing-courtyard

Use `tools/world_build/facade_constraints_v014.py` for reproducible per-facade dimensional bounds and `test_facade_constraints_v014.py` for regression checks. Six local equivalent tests passed before committing. The **v013 geometry is preserved unchanged**. No new GLB, inferred global coordinates, source image calibration, or measured elevations. Next step: test an independent taller SOUTH facade option and curved COURTYARD facade against photo silhouettes and independent artwork controls, retaining both as hypotheses.
