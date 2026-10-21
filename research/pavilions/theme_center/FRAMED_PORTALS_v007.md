# Framed portals v007

Built on 2026-10-20 as a separate provisional runtime derivative. [Download complete GLB, actual mesh renders, code and validation](https://drive.google.com/file/d/1nR8_305Dx3t6yEbcRdMPhm1Owi-vqS6Y/view). [Reproduction and detailed limitations](../../../tools/portal_finish_v007/README.md).

Four open doorway assemblies now have walls, deep jambs, headers, trim and thresholds: two Trylon passages and two Perisphere passages. Trylon infill closes the oversized facade opening and jambs meet cut brace caps; Helicline rail ends return into the exit jambs. Perisphere curved wall patches close inherited gaps around precise apertures. Its upper landing, 23-tread stair and returned rails replace obstructing provisional geometry. No hinged door leaves were added.

Six regression tests passed. All four openings cleared a discrete 51-position body surface screen (204 positions total; 0.6 m diameter, 1.8 m height). Source data, identities and transforms are preserved with documented mesh binding replacements. New/replacement solids were checked for closure and consistent winding. Renders are direct GLB renders, not AI images.

This implements the unfinished runtime elements; it does not reconstruct or certify the historical ground-level entrance, canopy, lettering, bridge underside, door dimensions or structural load paths. Native Unreal import, collision and complete traversal remain untested. Original source and print masters remain unchanged. Historical entrance/bridge reconstruction remains a distinct evidence-led task.

## Validation hardening, 2026-10-20

The checker now returns failure on surface contacts and binds the report to exact GLB bytes. Tests reject stale reports, missing/duplicate/incomplete portal screens, missing contact results and failed geometry checks. Fresh local validation of unchanged v007 cleared all 204 sampled poses; all 12 regressions passed. The original Drive ZIP stays immutable; current code and updated checksums are in `tools/portal_finish_v007/`. Game Development Studio CLI was unavailable; Python checks were executed. No geometry change or new Wolfram calculation. Next engine gate remains native Unreal import and full traversal; historical entrance/bridge work continues separately.
