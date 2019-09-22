"""
decorators module
"""

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'

from functools import partial, wraps
from inspect import getfullargspec
from collections import defaultdict
from .utils import hashabledict


def curry(fn):
    """
    Decorator for currying functions.
    >>> @curry
    ... def volume(a, b, c):
    ...     return a*b*c
    ...
    >>> volume(1,2,3) == volume(1)(2)(3) == volume(1,2)(3) == volume(1)(2,3) == 6
    """
    _args = getfullargspec(fn).args

    @wraps(fn)
    def curried(*args, **kwargs):
        return (
            fn(*args, **kwargs) if len(_args) - len(args) == 0 else
            curry(partial(fn, *args, **kwargs))
        )
    return curried


def memoize(fn):
    """
    Decorator that provides automatic caching for referentially transparent
    functions.
    """

    class NotInCache:
        """Placeholder class that implies the function hasn't
        been called yet for those particular arguments
        """
        pass

    cache = fn.cache = defaultdict(lambda: defaultdict(NotInCache))
    @wraps(fn)
    def memoized(*args, **kwargs):
        key0, key1 = str(args), hashabledict(kwargs) if kwargs else ''
        value = cache[key0][key1]
        if isinstance(value, NotInCache):
            value = cache[key0][key1] = fn(*args, **kwargs)
        return value
    return memoized
