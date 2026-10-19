# FMP Work Thread

## 2026-10-18: exterior-first production queue

Direction: start with exteriors; use explicitly uncertain massing where necessary;
advance each building toward a finished experience. Preserve authored decisions
and distinguish historical evidence from interpretation.

Implemented `tools/build_exterior_queue.py`, a dependency-free derived work queue.
Run from the repository root:

```bash
python tools/build_exterior_queue.py --output out/exterior_queue.csv
python -m unittest discover -s tests -v
```

The current 20-place source catalog yields 32 exterior/year tasks for 16 places.
Exhibits and show characters are excluded from the exterior queue, not deleted
from the project. Each year requires review; a catalog year range is not evidence
of an unchanged building. Existing geometry statuses are preserved. Plans located
does not mean plans reviewed, and site registration does not certify a model.
The generated CSV is disposable: do not record completion edits in it.

## Next work, in order

1. Reconcile the archived 239-candidate inventory with the 20-place Git catalog.
   Preserve original IDs and provenance; distinguish buildings, exhibits, tenants,
   characters, landscape and infrastructure. Do not infer missing-year existence.
2. Acquire and review baseline survey metadata and dated historical plan controls.
   Horizontal CRS, vertical datum, local origin and historical terrain remain unset.
3. Register the Theme Center footprint with documented residuals. Reconcile Trylon,
   Perisphere, Helicline and grounds as one exterior/circulation assembly, retaining
   separate 1939 and 1940 evidence and explicit uncertainty.
4. Track footprint, height, roof and facade evidence per building, then produce
   exterior geometry. Label unsupported volumes as provisional massing.
5. Verify walkable approaches and collision before interiors and media integration.

## Verification and limits

Six unit tests pass: year splitting, invalid/future year rejection, duplicate IDs,
category separation, and evidence gates. The script ran against the current Git
catalog and generated 32 rows. No new geometry, survey certification, terrain data,
or Unreal build is claimed by this increment. The 239-candidate archive has not
been reconciled or revalidated in this increment. No Drive backup was made here.

## 2026-10-18: archived inventory recovered and compared

Imported 239 candidates, 82 source records, 58 Operations Manual sheet leads and
239 production availability rows into separate archive tables in the standard
SQLite build. Comparison: 18 matching live records, 2 ID matches with differences,
219 archive-only candidates, no live-only records. Original IDs and raw years
are preserved. No automatic promotion to verified places. Eleven tests, catalog
validation, full imported-row comparison and SQLite checks pass.

See [reconciliation details](INVENTORY_RECONCILIATION.md). The archival recovery
and identity comparison portion of step 1 is complete; evidence review, candidate
classification and survey registration remain open. No new geometry in this pass.
