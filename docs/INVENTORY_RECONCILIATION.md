# Archived inventory reconciliation

The research snapshot is now reproducible in the Git-built SQLite index. This is
an identity comparison and archival import, not historical verification.

## Results

| Measure | Count |
|---|---:|
| Archived candidate records | 239 |
| Matching live IDs and labels/categories | 18 |
| Matching IDs with name/category differences | 2 |
| Candidates absent from the live places table | 219 |
| Live places absent from the archive | 0 |
| Archived source records | 82 |
| Operations Manual sheet leads | 58 |
| Archived production availability records | 239 |

The archive consists of 59 older research targets and 180 1964/1965 subjects.
These are not 239 verified buildings. Categories include tenants, exhibits,
performers, grouped infrastructure and candidate venues. It does not supply a
2026 site inventory or verified historic footprints.

## Differences requiring review

- WF0042: archive `Aquacade / Marine Amphitheatre`, category `attraction`;
  live `Aquacade`, category `architecture`. Review venue/show boundaries, including
  archive WF0043, before combining records or modeling duplicate structures.
- WF0050: archive `IRT/BMT and LIRR Fair Stations`; live `World's Fair Rail and
  Subway Access`. Review whether the record needs separate station/route children.
- WF0022: raw candidate year `1940|only` is preserved in the archival CSV. The
  comparison report explicitly normalizes this to `1940`, without certifying presence.

## Reproduce

```bash
python tools/validate_catalog.py
python tools/build_db.py
python tools/reconcile_inventory.py
python -m unittest discover -s tests -v
```

The four `catalog/archive_*.csv` files populate separate `archive_*` tables.
`places`, current model statuses, verified claims and era presence are unchanged.
`out/inventory_reconciliation.csv` is disposable; do not edit it as a master record.
No fuzzy name matching or automatic place creation occurs. IDs with different
names or categories require review even when the IDs match.

The import manifest records the source Drive URL, archive/database SHA-256 hashes,
CSV hashes and row counts. Raw year strings and source IDs remain intact.
Empty strings and SQL NULL both become NULL when rebuilt, consistent with the
existing database loader. The archive's source IDs are its own namespace; in
particular `LEGACY_DB` is a provenance marker, not an invented source-table record.

## Validation

All 618 imported rows compared equal to the source database after documented
empty-string normalization. SQLite integrity and foreign-key checks pass.
All 11 unit tests pass. Catalog validation passes for all 14 imported CSV tables.
Original drawings and source pages have not been newly reviewed in this pass.

## Next production gate

Use the retained sheet leads to locate dated site plans and survey control for the
Theme Center. Register the footprint and record residuals before assigning park
coordinates to existing geometry. Classify the 219 archive-only candidates and
resolve the two identity differences incrementally using primary evidence.
