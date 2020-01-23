import unittest

from exos import curry, memoize, fattr


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

    # pylint: disable=no-member
    def test_memoize(self):
        @memoize
        @fattr('counter', 0)
        def fibo(n):
            fibo.counter += 1
            return 1 if n <= 2 else fibo(n-1) + fibo(n-2)

        self.assertEqual(fibo(100), 354224848179261915075)
        self.assertEqual(fibo.counter, 100)
