import unittest
from exos import zip_with_attr

class TestZip(unittest.TestCase):
    def test_zip_with_attr(self):
        class A:
            def __init__(self, a, b, c):
                self.a = a
                self.b = b
                self.c = c

        objects = [A(1, 2, 3), A('4', 5.0, 'six')]
        output = [
            (o.a, b, c)
            for o, b, c in zip_with_attr(objects, 'b', 'c')
        ]
        self.assertEqual(output, [(1, 2, 3), ('4', 5.0, 'six')])
