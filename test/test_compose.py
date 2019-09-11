import unittest
from functools import reduce
from exos import compose

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
