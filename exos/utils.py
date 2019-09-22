"""
utility functions and classes
"""

from functools import reduce

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'


def pairs(*args):
    def fold(acc, curr):
        if len(acc[-1]) < 2:
            acc[-1].append(curr)
        else:
            acc.append([curr])
        return acc
    return reduce(fold, args, [[]])


class hashabledict(dict):
    """
    A hashable dicitionary that comes with the cost of immutability.
    Any attempts to modify it after its inception yields a RunTimeError
    """
    def __readonly__(self, *args, **kwargs):
        raise RuntimeError('Cannot modify hashabledict')

    __setitem__ = __readonly__
    __delitem__ = __readonly__
    pop = __readonly__
    popitem = __readonly__
    clear = __readonly__
    update = __readonly__
    setdefault = __readonly__
    del __readonly__

    def __key(self):
        return tuple((k, self[k]) for k in sorted(self))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()
