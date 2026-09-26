import copy
import json
import unittest
from pathlib import Path
from audit import compare

DATA = json.loads(Path(__file__).with_name('examples.json').read_text())

class ReleaseTests(unittest.TestCase):
    def test_bad_change_flags_dependencies_and_behavior(self):
        result = compare(DATA['before'], DATA['after'])
        self.assertFalse(result['ready_for_release'])
        self.assertEqual({'removal_review','behavior_regression_review','missing_dependency'},
                         {f['code'] for f in result['findings']})
        self.assertEqual(0, result['deployment_actions'])

    def test_no_change_passes(self):
        result = compare(DATA['before'], copy.deepcopy(DATA['before']))
        self.assertTrue(result['ready_for_release'])
        self.assertEqual([], result['changes'])

    def test_unknown_dependency(self):
        after = copy.deepcopy(DATA['before'])
        after[1]['depends_on'].append('field:Deal.Unknown')
        self.assertIn('missing_dependency', [f['code'] for f in compare(DATA['before'], after)['findings']])

    def test_duplicate_component_rejected(self):
        with self.assertRaises(ValueError):
            compare(DATA['before'], DATA['before'] + [DATA['before'][0]])

    def test_fingerprint_deterministic(self):
        a = compare(DATA['before'], DATA['after'])
        b = compare(copy.deepcopy(DATA['before']), copy.deepcopy(DATA['after']))
        self.assertEqual(a, b)

    def test_added_workflow_requires_review(self):
        after = copy.deepcopy(DATA['before']) + [{'kind':'workflow','name':'Deal.Notify','depends_on':[]}]
        self.assertIn('behavior_regression_review', [f['code'] for f in compare(DATA['before'], after)['findings']])

if __name__ == '__main__':
    unittest.main()
