import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from reconcile_inventory import reconcile, candidate_years


class ReconciliationTests(unittest.TestCase):
    def candidate(self, **kw):
        return dict(dict(inventory_id='WF1', label='Test', category='architecture',
                         year_candidates='1939|1940'), **kw)

    def place(self, **kw):
        return dict(dict(place_id='WF1', name='Test', category='architecture'), **kw)

    def test_no_name_only_merge(self):
        rows = reconcile([self.candidate()], [self.place(place_id='OTHER')])
        self.assertEqual([r['match_status'] for r in rows],
                         ['ARCHIVE_ONLY_CANDIDATE', 'LIVE_ONLY_PLACE'])

    def test_category_conflict_retained(self):
        rows = reconcile([self.candidate(category='attraction')], [self.place()])
        self.assertEqual(rows[0]['differences'], 'category')
        self.assertEqual(rows[0]['match_status'], 'ID_MATCH_REVIEW_DIFFERENCES')

    def test_only_suffix_is_explicit(self):
        self.assertEqual(candidate_years('1940|only'), ('1940', 'NORMALIZED_ONLY_SUFFIX'))
        self.assertEqual(candidate_years('1940|unknown'), ('', 'INVALID_REVIEW_REQUIRED'))
        self.assertEqual(candidate_years('2039'), ('', 'INVALID_REVIEW_REQUIRED'))

    def test_duplicates_rejected(self):
        with self.assertRaises(ValueError):
            reconcile([self.candidate(), self.candidate()], [])

    def test_no_mutation(self):
        c, p = self.candidate(), self.place()
        before = (dict(c), dict(p))
        reconcile([c], [p])
        self.assertEqual((c, p), before)


if __name__ == '__main__':
    unittest.main()
