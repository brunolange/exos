import unittest
from functools import reduce
from exos import reduce_right

class TestReduceRight(unittest.TestCase):
    def test_commutative(self):
        sum1to100 = reduce(lambda acc, curr: acc+curr, range(1, 101), 0)
        sum100to1 = reduce_right(lambda curr, acc: acc+curr, range(1, 101), 0)
        self.assertTrue(sum1to100 == sum100to1 == 5050)
