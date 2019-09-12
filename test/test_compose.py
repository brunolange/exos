import unittest
from functools import reduce, partial
import math
from exos import compose, pipe

class TestCompose(unittest.TestCase):
    def test_compose(self):
        f = lambda x: x*2
        h = lambda x: -x
        g = compose(f, h)
        self.assertEqual(g(4), f(h(4)))

        w = compose(h, f)
        self.assertEqual(w(4), h(f(4)))

        p = lambda x: x**2

        self.assertTrue(compose(p, g)(3) == p(f(h(3))) == 36)
        self.assertTrue(compose(h, p)(12) == h(p(12)) == -144)

    def test_general_composition(self):
        f = lambda x, y, bias=0: 2*x - math.sqrt(y) + bias
        g = lambda x: -x

        h = compose(g, f)
        self.assertEqual(h(5, 144), 2)

        hb = compose(g, partial(f, bias=100))
        self.assertEqual(hb(5, 144), -98)

        s = compose(str, h)
        self.assertEqual(s(12, 625), '1.0')

        digits = compose(lambda number: [int(digit) for digit in number.split('.')], s)
        self.assertEqual(digits(12, 625), [1, 0])

    def test_pipe(self):
        def f(x, y, bias=0):
            return 2*x - math.sqrt(y) + bias
        def g(x):
            return -x

        h = compose(g, f)
        p = pipe(f, g)
        self.assertTrue(h(5, 144) == p(5, 144))
