import unittest
from exos import extend

class TestExtend(unittest.TestCase):
    def test_shallow(self):
        self.assertEqual(
            extend({'a': 'A', 'b': 'B'}, {'c': 'C'}),
            {'a': 'A', 'b': 'B', 'c': 'C'}
        )

    def test_deep(self):
        d1 = {
            'package': 'exos',
            'motto': 'expressions over statements',
            'versions': {
                'beta': 'nightly'
            }
        }
        d2 = {
            'versions': {
                'beta': 'NIGHTLY'
            }
        }

        d = extend(d1, d2)
        self.assertTrue('package' in d)
        self.assertTrue(d['versions']['beta'] == 'NIGHTLY')

    def test_immutability(self):
        d = {'a': 42}
        _ = extend(d, d, d, d, d, {'b': 100})
        self.assertEqual(d, {'a': 42})
