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
    ... def p(a, b, c):
    ...     return a*b*c
    ...
    >>> p(1,2,3) == p(1)(2)(3) == p(1,2)(3) == p(1)(2,3) == 6
    """
    spec = getfullargspec(fn)
    arity = len(spec.args) - len(spec.defaults or ())

    @wraps(fn)
    def curried(*args, **kwargs):
        return (
            fn(*args, **kwargs) if arity - len(args) == 0 else
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


def fattr(key, value):
    """Decorator for function attributes

    >>> @fattr('key', 42)
    ... def f():
    ...     pass
    >>> f.key
    42
    """
    def wrapper(fn):
        setattr(fn, key, value)
        return fn
    return wrapper
