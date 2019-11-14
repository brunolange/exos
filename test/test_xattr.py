import unittest
from exos import xattr

class TestXAttr(unittest.TestCase):
    def test_xattr(self):
        class A:
            def __init__(self, a):
                self.a = a
        class B:
            def __init__(self, a, b):
                self.a = a
                self.b = b

        self.assertEqual(xattr(A(42), 'a'), 42)
        self.assertEqual(xattr(B(100, 31), 'a'), 100)
        self.assertEqual(xattr(B(100, 31), 'b'), 31)
        self.assertTrue(isinstance(xattr(B(A('hello'), None), 'a'), A))
        self.assertEqual(xattr(B(A('hello'), 31), 'a.a'), 'hello')
        self.assertEqual(xattr(B(A('hello'), 31), 'b'), 31)

        with self.assertRaises(AttributeError):
            _ = xattr(None, 'b')

        with self.assertRaises(AttributeError):
            _ = xattr(A(None), 'b')

        self.assertEqual(xattr(None, 'a', 42), 42)
