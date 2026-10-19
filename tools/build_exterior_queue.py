"""Generate an evidence-gated exterior queue; never changes historical records.

Run: python tools/build_exterior_queue.py --output out/exterior_queue.csv
The output is a derived planning view, not proof of existence in any year.
"""
import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTERIOR = {'architecture', 'circulation', 'landscape', 'infrastructure'}
YEARS = {1939, 1940, 1964, 1965, 2026}
FIELDS = ('task_id', 'place_id', 'name', 'year', 'category', 'priority',
          'identity_status', 'geometry_status', 'site_registration',
          'year_verification', 'next_action', 'completion_gate', 'notes')


def expand_years(value):
    """Accept explicit comma/semicolon years or ranges; reject ambiguous scope."""
    result = set()
    for part in re.split(r'[,;]', value):
        match = re.fullmatch(r'\s*(\d{4})(?:\s*-\s*(\d{4}))?\s*', part)
        if not match:
            raise ValueError(f'Unrecognized year scope: {value!r}')
        start = int(match[1])
        end = int(match[2] or start)
        if end < start or end - start > 100:
            raise ValueError(f'Invalid year range: {value!r}')
        result.update(range(start, end + 1))
    if not result <= YEARS:
        raise ValueError(f'Unsupported historical years: {sorted(result - YEARS)}')
    return sorted(result)


def build_rows(places):
    rows, seen = [], set()
    for place in places:
        pid = place['place_id']
        if not pid or pid in seen:
            raise ValueError(f'Missing or duplicate place_id: {pid!r}')
        seen.add(pid)
        years = expand_years(place['year_scope'])
        if place['category'] not in EXTERIOR:
            continue
        # Registration alone never proves an exterior or a year-specific state.
        unregistered = place['site_registration'] == 'UNREGISTERED'
        action = ('Identify dated plan and control points; record CRS, vertical datum '
                  'and registration residuals before site placement.' if unregistered else
                  'Review registration evidence and dated footprint before exterior modeling.')
        if place['geometry_status'] == 'PLANS_LOCATED':
            action += ' Retrieve and review the plan lead; located does not mean verified.'
        elif place['geometry_status'] in {'PROVISIONAL_MODEL', 'INTERPRETIVE_MODEL'}:
            action += ' Reconcile existing geometry with the dated exterior evidence.'
        else:
            action += ' Gather footprint, height, roof and facade evidence; label unknown massing.'
        for year in years:
            rows.append(dict(task_id=f'{pid}-{year}-EXT', place_id=pid,
                name=place['name'], year=year, category=place['category'],
                priority='P1' if place['zone'] == 'Theme Center' else 'P2',
                identity_status=place['identity_status'],
                geometry_status=place['geometry_status'],
                site_registration=place['site_registration'],
                year_verification='REVIEW_REQUIRED', next_action=action,
                completion_gate='Dated identity and footprint evidence; registered location; '
                    'dimension sources; explicit uncertainty; exterior QA; walkable approach '
                    'and collision test. Interior and media remain separate work.',
                notes=place['notes']))
    return sorted(rows, key=lambda r: (r['priority'], r['place_id'], r['year']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=ROOT / 'catalog/places.csv')
    parser.add_argument('--output', type=Path, default=ROOT / 'out/exterior_queue.csv')
    args = parser.parse_args()
    if args.output.resolve() == args.catalog.resolve():
        parser.error('Output must not overwrite the source catalog')
    with args.catalog.open(encoding='utf-8-sig', newline='') as handle:
        rows = build_rows(csv.DictReader(handle))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f'{len(rows)} exterior/year tasks from the current catalog. '
          'Not an exhaustive inventory; no historical states certified.')


if __name__ == '__main__':
    main()
