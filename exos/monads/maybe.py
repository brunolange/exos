"""Simple implementation of a Maybe monad
"""

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'


class Maybe:
    pass


class Just(Maybe):
    def __init__(self, value):
        self.value = value


    def bind(self, fn):
        return Just(fn(self.value))


    def __eq__(self, other):
        return isinstance(other, Just) and other.value == self.value


    def __str__(self):
        return 'Just {}'.format(self.value)


class _Nothing(Maybe):
    def bind(self, _):
        return self


    def __str__(self):
        return 'Nothing'

Nothing = _Nothing()
