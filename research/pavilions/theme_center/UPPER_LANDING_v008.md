# Upper Perisphere landing v008

Fixed the incomplete connection between the rectangular upper landing and diagonal stair. Six of fifteen probes 100 mm before the stair previously lacked level support. The replacement slab follows the existing stair/rail footprint and has a full-width nosing notch. Fifteen of fifteen approach probes and fifteen of fifteen first-tread probes now reach their intended elevations. Four focused tests pass; a fresh doorway screen records no surface contacts at 204 poses. Wolfram independently checked the outer corner's 0.676524 m projection beyond the old landing edge. Original geometry remains preserved in the file; only the landing node binds to the new mesh.

[Complete v008 scene, code, tests, reports and actual-mesh drawing](https://drive.google.com/file/d/14X-Jp_tt8PfbNNy0F3TpBFkuKbJM5eGO/view). [Editable source and SVG](../../../tools/portal_approach_v008/README.md). [Per-file hashes and sizes](../../../tools/portal_approach_v008/ARCHIVE_INVENTORY.json). Source/SVG commit sequence ends at 0d4a6db42de08b3a5347c34d18e2a41207ea3792. Drive folder membership and size were verified after upload.

This is a provisional runtime repair, not historical/structural certification. Native Unreal traversal is untested. Game Development Studio CLI unavailable; local Trimesh/Manifold/Matplotlib performed production and checks. PNG/GLB/ZIP Git copies remain GIT_BINARY_PENDING due to missing direct Git push credentials and no binary release connector. Earlier thread backfill and verbatim transcript remain pending. Next: native engine import and traversal of the corrected landing and full stair route.

## 2026-10-21: Full stair support screen

Read-only v008 inspection found support at all 375 sampled positions: 15 per tread across 23 treads, plus 30 beyond the bottom junction onto the return bridge. No mesh change was required. Wolfram confirms nominal 159.026 mm rise, 296.622 mm going and 28.197-degree slope. [Code and detailed limits](https://github.com/cameronprops/TheFlushingMeadowProject/tree/main/tools/stair_run_review_v008). This establishes discrete floor support only; body/head clearance and Unreal movement remain open.

Actual source/report copies are in project Drive: script `1rJQHNtlY6Agmo069nlVFdeHM8MzwLPEH`, report `1NzEBbZLzY3I93S1m1cK3hEqhCqIyGpqa`, Wolfram receipt `1ncWUFbW8Cfl28zkakxIxNrwv-EMAbu5a`, README `1ewmbnN-IiAglNDLgWg4jtBWyJpWB9EE3`. Git commits through d6f302622bdfd9b872581f39d97bc908099d2813. Drive size/folder readback passed; independent downloaded-byte dual verification is still pending. Prior large binary and transcript backfill remain open.


## v008 stair body screen, 2026-10-22 UTC

103 discrete poses / 1,339 sphere centres: zero nonwalking surface contacts; 69 walking contacts at the bottom sphere remain unresolved pending Unreal step handling. No geometry changed. See [scope and reproduction](https://github.com/cameronprops/TheFlushingMeadowProject/blob/main/tools/stair_run_review_v008/BODY_SCREEN.md) (repository path: tools/stair_run_review_v008/BODY_SCREEN.md). Native Unreal traversal untested; game-dev executable unavailable. Wolfram independently confirmed cover radius 0.304138126514911 m. Full transcript unavailable and prior GIT_BINARY_PENDING entries remain open.

| File in tools/stair_run_review_v008 | Git commit | Drive file | SHA-256 |
|---|---|---|---|
| check_body.py | b9fa776b73c6d000ab055db8ecbaa3bca1249769 | [copy](https://drive.google.com/file/d/1pveOyTfO-ijTeUfZ_7V3H9L9JvHZNbNo/view) | dc6e1f39ff4ebf8f5ec8f956d4dd63329644a8f3aa17915359a4eebd4d1edd2c |
| body_screen.json | 6749a0e1881b410d326e1ee3603545df72428322 | [copy](https://drive.google.com/file/d/11o9Ylg0eDVh-QarflDueHR3DG-yNsY1Y/view) | dcb6d7a876c91f2185133d6b942587de844275621d2eb5f4c142404f9f0f628f |
| BODY_SCREEN.md | 71e3343acbb11f3a3f26b1c0ba510a5599d319dd | [copy](https://drive.google.com/file/d/1qiYaQKInEPTK7xdDYFBi5nxxChMyOLl3/view) | 00f8dfb4c5d6a1aa3985baecaf8542dcac5ce95ab5c77331842f721efe387d96 |

Git contents read back identically. Drive file IDs, sizes and archive folder membership verified; independent Drive byte-hash readback pending. Actual files uploaded, not pointers.
