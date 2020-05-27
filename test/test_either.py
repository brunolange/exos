import unittest

from exos.monads.either import Left, Right

class TestEither(unittest.TestCase):
    def test_left_right(self):
        for value in [
            10,
            '10',
            0,
            Right('hello')
        ]:
            self.assertEqual(Right(value).value, value)
            self.assertEqual(Left(value).value, value)

    def test_bind(self):
        self.assertEqual(Right(6).bind(lambda x: x*7).value, 42)
        self.assertEqual(Left(6).bind(lambda x: x*7).value, 6)
