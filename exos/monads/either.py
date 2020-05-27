"""Simple implementation of an Either monad
"""

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'

import operator

EITHER_XOR = 'Either requires either a left or a right value'

class Either:
    def __init__(self, left=None, right=None):
        if left is None:
            assert right is not None, EITHER_XOR
            self.value = right
            self.is_left = False
        if right is None:
            assert left is not None, EITHER_XOR
            self.value = left
            self.is_left = True
        assert self.value is not None, EITHER_XOR
        print('value', self.value)


    def bind(self, fn):
        return (
            Left(self.value) if self.is_left else
            Right(fn(self.value))
        )


"""Type constructors
"""
Left = lambda value: Either(left=value)
Right = lambda value: Either(right=value)
