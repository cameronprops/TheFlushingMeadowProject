# Theme Center upper exit photo-consistent sidewall and stair conflict v012

**Status: implemented / 15 focused tests passed / provisional runtime overlay; historical master unchanged.**

## Direct model measurements

Actual scene `FMP_ThemeCenter_Assembled_Runtime_v005.glb`, SHA256 `de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439`. Uses right-handed model-local Y-up metres, not surveyed.

The older `PROVISIONAL_UPPER_EXIT_STAIR` has bbox x **−22.499 to −17.226 metres**; the separate 23-tread `PROVISIONAL_UpperReturnStair_01..23` system is x **−30.934 to −24.016 metres**. There is a **1.517m X-axis AABB gap**. The older stair's AABB overlaps the **lower Perisphere exit header and jamb AABBs** (broad phase, NOT a triangle collision). It does not overlap the upper portal-head X range. The 23-tread run connects in X to the newer upper landing. No claim that as-built fair had two staircases; do not delete either prior source without reconciliation.

## Actual photograph evidence

Original RIBApix `RIBA9908` secondary reproduction visually shows a **solid triangular wall flanking the upper exit stair**, which slopes to the open bridge, and a separate partially occluded opening at the lower deck. No photographed exact side, wall thickness, riser count, door dimension or absolute grade was measured. The lower opening is likely the public lower exit but the image alone does not certify its original architectural label. Source pixels intentionally NOT included due rights restrictions.

New original-photo candidate: [Harry Ransom Center Gottscho accession 980:0151:0007](https://research.hrc.utexas.edu/photoPublic/fullDisplay.cfm?CollID=16343), 1939, title *Perisphere bridge, trylon and ramp*. Record is catalog-only and image has not been reviewed. RIBA original photographic scan remains unacquired.

## Deliverables

The [v012 full source package](../../archive/packages/FMP_ThemeCenter_UpperExit_Cheek_v012.zip) contains source-locked parametric Python `build_cheek_v012.py`, 15-test regression harness, generated **4,424-byte GLB candidate overlay**, code-rendered actual-model side elevation PNG/SVG, original-read-only model audit, SHA256 member inventory, and README. Original v005 GLB is NOT copied into this ZIP. Its bounds and hash were validated before generating the overlay.

Provisional modeling parameters: 0.10m wall thickness, 1.045m lateral offset, 1.0m above tread guard and bottom bridge datum 15.8496m. These are EDITORIAL, not photographic/surveyed dimensions. GLB is watertight, winding consistent, 196 triangles. Load as a separate overlay; do not replace historical master or permanently suppress the legacy stair yet. No native Unreal tests, full-body capsule sweep, entire scene collisions, or print master approval completed.

Google Drive complete source package: https://drive.google.com/file/d/1Y-zCKYJHcn6KwR6d0APrBVrhtHm5rFwV/view . Image drawing separately https://drive.google.com/file/d/1yT-sZn11cRiQYDVmxf3abdZt6rsu6f7k/view . Source package local SHA-256 `37351d7c3d8df6f219fdde1964bf3edcfebed491f464ace64ba545415fa740f9`, size 137,150 bytes.

**Next:** independently confirm actual original RIBA stair and Harry Ransom Center/NYPL alternate views; reconcile the two source stairs with authenticated portal position and collision, then update a reversible CAD master.
