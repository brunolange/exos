import unittest

from exos import curry


class TestDecorators(unittest.TestCase):
    def test_curry(self):
        @curry
        def add(x, y):
            return x + y

        # pylint: disable=no-value-for-parameter
        add3 = add(3)
        self.assertEqual(add3(5), 8)

        @curry
        def concat(s1, s2, prefix=''):
            return ''.join([prefix, s1, s2])

        cfoo = concat('foo')
        # pylint: disable=not-callable
        self.assertEqual(cfoo('bar'), 'foobar')


