"""
Data structures
"""

from collections import defaultdict


__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'


def multimap(depth, callable):
    """A multilevel map.

    >>> m = multimap(3, set)
    >>> m['a']['b']['c'].add(42)
    >>> m['a']['b']['c']
    42
    >>> m['a']['b']['d']
    set()
    """
    nxt = lambda f: defaultdict(lambda: f)
    output = defaultdict(callable)
    for _ in range(depth - 1):
        output = nxt(output)
    return output
