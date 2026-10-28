# WF0028 v032: cross-frame entrance depth suitability check

2026-10-27. Increment after v031 frame selector.

Implemented ORB feature matching + RANSAC planar homography diagnostic for pairs of selected stills. Outputs pairwise feature counts, planar inlier ratios and pixel residual, with explicit flags for planar / rotational ambiguity and insufficient matches. A non-planar candidate is **not proof of stereo baseline**, and planar correspondence does not exclude actual 3D geometry.

Local test: two synthetic/blank frame cases PASSED. **No actual Meière film frames processed** because original film access remains unavailable. Historical entrance dimensions, curvature, stairs and elevations remain unsolved and unchanged.

Git scripts:
- `tools/world_build/wf0028_assess_frame_pairs_v032.py`
- `tools/world_build/test_wf0028_assess_frame_pairs_v032.py`
Drive binary ZIP `WF0028_Entrance_View_Pair_Diagnostics_v032.zip`: https://drive.google.com/file/d/1NOLGu8obC-2sAuRywu7I_N9N7r3rXWvF/view ; SHA256 `af5f107d46934324a0d7a22a9e5dfc61ab642e126e6e105e58bcc3f2cfaa0092`; size 3250 bytes.

**Archive status:** scripts and tests physically committed to GitHub and in the complete ZIP on Drive; ZIP file itself Git binary pending. No historic imagery included or redistributed. No verbatim conversation transcript export.

Next: acquire authorized film digital file, run v031 selector and v032 diagnostics, manually confirm view baselines, fit camera poses with off-plane physical tie points and a metric plan, then assess 2–3 inch tolerance against independent error budget before reconstructing stairs.
