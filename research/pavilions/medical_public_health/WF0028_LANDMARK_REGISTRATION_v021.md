# WF0028 v021: independent landmark calibration tool

Date 2026-10-21. The source-first progression after curve sensitivity v020.

- Reproducible Python utility `tools/world_build/wf0028_landmark_fit_v021.py` fits a planar 2D scale/rotation/translation to 3+ independently sourced point pairs with >=1 withheld verification landmark, logs per-point residuals and RMS. Collinear controls rejected. It intentionally does **not** solve the perspective of oblique postcard photographs.
- No historical landmark coordinates have been provided or invented. Fitting period photos requires calibrated camera pose and/or original measured plans.
- Local tests for insufficient observations, synthetic similarity transform and collinear rejection: **3 passed** using NumPy, with synthetic samples only.
- Package `WF0028_Landmark_Registration_v021.zip` SHA256 `016f2b97cce638dba73a623338969c92e7f6d6d9b1c8e6cdba29cba5a946f1c7`, holds executable initial implementation and tests.
- Previous v020 ZIP uploaded to Drive as [WF0028 v020](https://drive.google.com/file/d/1NqeuBKsEnGtKK2N3hwe2RLN1tLPXdI-T/view); its PDF/PNG remain Git binary pending.

**Next**: obtain/read NYSL original full-plan scan or measured dimension string and independently identifiable control points. Create dated landmark records with source page pixels and independent holdout. Do not fit architectural curves to illustrative postcard art or mark numerical guesses derived measurements.
