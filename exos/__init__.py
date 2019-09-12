""" exos.py
EXpressions Over Statements: extended functional tools in Python.
"""

from functools import partial, reduce, wraps
from operator import iconcat
from inspect import getfullargspec
from collections import defaultdict
from .io import each, ueach, print_each
from .decorators import curry, memoize
from .exceptions import NonExhaustivePattern
from .utils import pairs

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'
__all__ = [
    'each',
    'ueach',
    'print_each',
    'curry',
    'memoize',
    'when',
    'flip',
    'map_attr',
    'map_method',
    'flatten',
    'zip_with_map',
    'extend',
    'reduce_right',
    'compose'
]

def when(*args):
    """
    The declarative version of a switch statement.
    >>> a = 42
    >>> c = when(
        a < 4,   'less than 4',
        a < 10,  'less than 10',
        a == 42, 'the answer!',
    )
    >>> print(c)
    The answer!

    If you'd like to defer evaluation of either the predicate
    or the actual value, use a lambda or a partial constructor
    to emulate laziness.
    """
    for predicate, value in pairs(*args):
        predicate = predicate() if callable(predicate) else predicate
        if predicate:
            return value() if callable(value) else value
    raise NonExhaustivePattern()

def flip(fn):
    spec = getfullargspec(fn)
    arity = len(spec.args) - len(spec.defaults or ())
    if arity < 2:
        return fn
    def flipped(*args, **kwargs):
        swapped = (args[1], args[0]) + args[2:]
        return (
            fn(*swapped, **kwargs) if len(args) == arity else
            partial(fn, *swapped, **kwargs)
        )
    return flipped

def map_attr(attr):
    """
    Returns a mapper function for attribute extraction

    map_attr('auth_user') <=> lambda account_user: account_user.auth_user
    map_attr('auth_user.email') <=> lambda account_user: account_user.auth_user.email
    """
    # there's no need to flip because of the order of arguments in the reduce function
    return partial(reduce, getattr, attr.split('.'))

def map_method(path, *args, **kwargs):
    """
    Returns a mapper function that runs the path method for each instance of
    the iterable collection.

    `map_method('accountuser_set.filter', is_deleted=False)` is equivalent to
    `lambda account: account.accountuser_set.filter(is_deleted=False)`
    """
    return lambda x: map_attr(path)(x)(*args, **kwargs)

def flatten(xs):
    """
    Flattens list of lists.

    >>> flatten([[1], [2], [3])
    >>> [1,2,3]
    >>> flatten([[10], [], [55])
    >>> [10, 55]
    """
    return reduce(iconcat, xs, [])

def zip_with_map(mapper, iterable):
    """
    Returns a collection of pairs where the first
    element correspond to the item in the iterable
    and the second is its mapped version, that is,
    the item when applied to the mapper function.

    >>> zip_with_map(lambda x: x**2, [1,2,3])
    >>> [(1,1), (2,4), (3,9)]
    """
    return zip(iterable, map(mapper, iterable))

def extend(*dicts):
    """
    Returns a dictionary that combines all dictionaries passed as arguments
    without mutating any of them.
    """
    def fold(acc, curr):
        acc.update(curr)
        return acc
    return reduce(fold, dicts, {})

def reduce_right(fold, xs, x0):
    """
    Right-associative fold of a structure.
    """
    return reduce(flip(fold), reversed(xs), x0)

identity = lambda x: x

class Identity:
    pass

def compose(*fns):
    """
    Simple function composition.
    """
    def fold(curr, acc):
        if acc is Identity:
            return curr

        return lambda *args, **kwargs: curr(acc(*args, **kwargs))
    return reduce_right(fold, fns, Identity)
