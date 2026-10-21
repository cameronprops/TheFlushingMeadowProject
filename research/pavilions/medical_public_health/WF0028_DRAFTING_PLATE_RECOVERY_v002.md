# WF0028 drafting plate recovery v002 (2026-10-20)

## Reported failure and repair
User reported the four-view plate package did not work. The v001 ZIP passed CRC checks but `wf0028_drafting/render_plate.py` contained machine-specific absolute `/mnt/data/wf0028_drafting` paths and was not portable.

Rebuilt the release from its original v004 GLB: changed loader and PNG output to paths relative to the script directory; executed `python wf0028_drafting/render_plate.py` from an extracted directory successfully; generated 3570 x 2730 PNG plus single-sheet PDF from the regenerated PNG. Verified `ZipFile.testzip()==None`. PDF and GLB/PNG do not establish as-built accuracy; the v017 curved facade study is not included in this v004 mesh.

## Files and archive
- `WF0028_four_view_drafting_plate_FIXED_v002.zip`: full bundle (original source v004 GLB, repaired renderer Python, PNG, PDF, README); ZIP SHA256 `7265b062c849f636024e271758de85bf3699bdba38c402368e08b3a19e2df15d`; size **630058 bytes**.
- [Verified Google Drive archive](https://drive.google.com/file/d/1EVcuQwn5j26Mqu04uN9Kr0hDgQaezIRd/view?usp=drivesdk), ID `1EVcuQwn5j26Mqu04uN9Kr0hDgQaezIRd`, project archive folder `11aRetkT2qaA69j8jnRyqxCJu2sR7DAPk`.
- Original v001 documented at `WF0028_FOUR_VIEW_DRAFTING_PLATE_v001.md`, now superseded for portability but retained unchanged.
- **Dual archive status: GIT_BINARY_PENDING.** The actual repaired Python, PNG/PDF and source GLB are preserved in Drive ZIP, but they are not all separate tracked objects or Git release binaries. This Git document is a verified pointer, not an independent second byte copy. Do not mark DUAL_VERIFIED.

## Historical status
Curved courtyard-facing architectural features are documented in photographic reference. The v016 and v017 arcs are independent provisional witness geometry; v016 was misplaced and v017 remains visually interpretive. Never draw them as if they were present in source v004.

## Agent follow-up
An archival agent can reconcile the binary Git release/LFS policy, a CAD/render QA agent can inspect a 4-view screenshot/render inside the deployed viewer, and a research agent can calibrate the v017 arc against dated source photos. All three must report artifacts and test outcomes individually, not accept one agent's statement as proof.
