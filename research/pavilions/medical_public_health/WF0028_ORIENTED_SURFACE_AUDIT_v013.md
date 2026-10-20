# WF0028 v013 oriented floor-support audit

2026-10-20. Tested v012 unchanged GLB with actual transformed and rotated mesh-footprint convex hulls rather than axis-aligned deck bounds. Sampled 0.45m-radius walking footprint at <=0.2m intervals across 14 proposed links. Support polygons are unioned by elevations in 0.03m bands; abrupt elevation changes >0.03m flagged.

**Result: 5/14 candidate routes clear in this preliminary oriented-footprint screen; 9/14 require further repair.** This supersedes optimistic 14/14 *centerline* support from v010 and 8/14 AABB-body screen from v011. Examples: western courtyard link 20 samples unsupported; east courtyard to Science north face 10 unsupported. Several threshold areas have uncovered margins and steps.

Three local regression tests passed. v012 geometry unmodified. No full triangle-level support or swept-body collision (convex hull can overstate support), no Unreal test and no historically verified openings, floorplan or elevation datum. All geometry INTERPRETIVE / SIMULATED.

Downloadable release: `WF0028_1939_Oriented_Surface_Audit_v013.zip`, SHA256 `7712ef9e76ca03b31ac4a629bcdc8099e8bca3675d501eecb966fb50235732ce`. Contains v012 GLB, route JSON, runnable audit, tests, report and README.

Next task: solve unsupported margins and elevations via independent level-matched continuous walkway polygons or historically sourced thresholds, then test exact oriented triangles and obstacle clearances. Preserve original 1939 source masters.
