import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('queue_builder',
    Path(__file__).resolve().parents[1] / 'tools/build_exterior_queue.py')
queue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(queue)


class ExteriorQueueTests(unittest.TestCase):
    def place(self, **overrides):
        row = dict(place_id='WF1', name='Test', category='architecture',
                   zone='Theme Center', year_scope='1939-1940',
                   identity_status='HISTORICAL_NAME', geometry_status='PLANS_LOCATED',
                   site_registration='UNREGISTERED', notes='Unreviewed lead')
        return dict(row, **overrides)

    def test_years_are_separate_and_unverified(self):
        rows = queue.build_rows([self.place()])
        self.assertEqual([r['year'] for r in rows], [1939, 1940])
        self.assertEqual(len({r['task_id'] for r in rows}), 2)
        self.assertTrue(all(r['year_verification'] == 'REVIEW_REQUIRED' for r in rows))
        self.assertIn('located does not mean verified', rows[0]['next_action'])

    def test_exhibits_and_characters_are_not_pavilions(self):
        for category in ['exhibit', 'show_character']:
            self.assertEqual(queue.build_rows([self.place(category=category)]), [])

    def test_registration_does_not_certify_geometry(self):
        row = queue.build_rows([self.place(site_registration='REGISTERED')])[0]
        self.assertIn('Review registration evidence', row['next_action'])
        self.assertEqual(row['year_verification'], 'REVIEW_REQUIRED')

    def test_bad_and_future_years_rejected(self):
        for value in ['1939?', '1940-1939', '2039', '', '1939-1965']:
            with self.assertRaises(ValueError):
                queue.expand_years(value)

    def test_duplicate_identity_rejected(self):
        with self.assertRaises(ValueError):
            queue.build_rows([self.place(), self.place()])

    def test_explicit_disjoint_years(self):
        self.assertEqual(queue.expand_years('1964-1965;2026'), [1964, 1965, 2026])


if __name__ == '__main__':
    unittest.main()
