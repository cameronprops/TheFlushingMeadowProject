"""Compare archived candidate identities with current places without merging them."""
import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ('inventory_id', 'archive_label', 'place_id', 'current_name',
          'match_status', 'differences', 'raw_year_candidates', 'candidate_years',
          'year_parse_status', 'next_action')
YEARS = {'1939', '1940', '1964', '1965', '2026'}


def candidate_years(raw):
    tokens = raw.split('|')
    if len(tokens) == 2 and tokens[0] in YEARS and tokens[1] == 'only':
        return tokens[0], 'NORMALIZED_ONLY_SUFFIX'
    if tokens and all(t in YEARS for t in tokens) and len(tokens) == len(set(tokens)):
        return '|'.join(sorted(tokens)), 'PARSED_NOT_VERIFIED'
    return '', 'INVALID_REVIEW_REQUIRED'


def index_unique(rows, key):
    result = {}
    for row in rows:
        value = row[key]
        if not value or value in result:
            raise ValueError(f'Duplicate or empty {key}: {value!r}')
        result[value] = row
    return result


def reconcile(candidates, places):
    candidates = index_unique(candidates, 'inventory_id')
    places = index_unique(places, 'place_id')
    rows = []
    for key, item in sorted(candidates.items()):
        place = places.get(key)
        years, parse_status = candidate_years(item['year_candidates'])
        differences = []
        if place:
            for old, new in [('label', 'name'), ('category', 'category')]:
                if item[old] != place[new]:
                    differences.append(new)
        status = ('ID_MATCH_REVIEW_DIFFERENCES' if differences else 'ID_AND_LABEL_MATCH') if place else 'ARCHIVE_ONLY_CANDIDATE'
        rows.append(dict(inventory_id=key, archive_label=item['label'],
            place_id=key if place else '', current_name=place['name'] if place else '',
            match_status=status, differences='|'.join(differences),
            raw_year_candidates=item['year_candidates'], candidate_years=years,
            year_parse_status=parse_status,
            next_action='Review dated identity, category and footprint evidence; no automatic promotion to verified place.'))
    for key in sorted(places.keys() - candidates.keys()):
        rows.append(dict(inventory_id='', archive_label='', place_id=key,
            current_name=places[key]['name'], match_status='LIVE_ONLY_PLACE',
            differences='', raw_year_candidates='', candidate_years='',
            year_parse_status='NOT_APPLICABLE', next_action='Retain current record; investigate archive coverage.'))
    return rows


def read(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'out/inventory_reconciliation.csv')
    args = parser.parse_args()
    inputs = [ROOT / 'catalog/archive_inventory_candidates.csv', ROOT / 'catalog/places.csv']
    if args.output.resolve() in [p.resolve() for p in inputs]:
        parser.error('Output must not overwrite input')
    rows = reconcile(read(inputs[0]), read(inputs[1]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    from collections import Counter
    print(dict(Counter(r['match_status'] for r in rows)))
    print(dict(Counter(r['year_parse_status'] for r in rows)))


if __name__ == '__main__':
    main()
