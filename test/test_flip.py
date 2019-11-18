import unittest
from exos import flip

class TestFLip(unittest.TestCase):
    def test_flip(self):
        subtract = lambda a, b: a - b
        self.assertTrue(subtract(100, 1), 99)
        self.assertTrue(flip(subtract)(100, 1), -99)
