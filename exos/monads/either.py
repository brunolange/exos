"""Simple implementation of an Either monad
"""

__author__ = "Bruno Lange"
__email__ = "blangeram@gmail.com"
__license__ = "MIT"

import operator
from abc import abstractmethod

from . import Monad

EITHER_XOR = "Either requires either a left or a right value"


class Either(Monad):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "{} {}".format(type(self).__name__, self.value)


class Left(Either):
    def bind(self, _):
        return Left(self.value)


class Right(Either):
    def bind(self, fn):
        return Right(fn(self.value))
