"""monads.py
"""

__author__ = "Bruno Lange"
__email__ = "blangeram@gmail.com"
__license__ = "MIT"

from abc import abstractmethod


class Monad:
    @abstractmethod
    def bind(self, fn):
        pass
