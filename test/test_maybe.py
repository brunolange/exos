import unittest

from exos.monads.maybe import Maybe, Just, Nothing

class TestMaybe(unittest.TestCase):
    def test_nothing(self):
        n = Nothing
        self.assertTrue(isinstance(n, Maybe))

    def test_just(self):
        n = Just(42)
        self.assertTrue(isinstance(n, Maybe))
        self.assertEqual(n.value, 42)

    def test_bind(self):
        self.assertEqual(Just(6).bind(lambda x: x*7), Just(42))
        self.assertEqual(Nothing.bind(lambda x: x*7), Nothing)
