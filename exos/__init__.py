""" exos.py
EXpressions Over Statements: extended functional tools in Python.
"""

from functools import partial, reduce
from operator import iconcat
from inspect import getfullargspec
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
    'mattr',
    'map_attr',
    'mmethod',
    'map_method',
    'flatten',
    'zip_with_map',
    'zip_with_attr',
    'extend',
    'reduce_right',
    'compose',
    'pipe'
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
    _pairs = pairs(*args)
    last = _pairs[-1]
    if len(last) < 2:
        last.insert(0, True)

    for predicate, value in _pairs:
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


def mattr(attr):
    """
    Returns a mapper function for attribute extraction

    mattr('user') <=> lambda account: account.user
    mattr('user.email') <=> lambda account: account.user.email
    """
    return partial(reduce, getattr, attr.split('.'))

def map_attr(attr, iterable):
    """
    Returns a map object where each item corresponds to the extracted
    attribute given by `attr` from the original object in the iterable
    collection.
    """
    return map(mattr(attr), iterable)


def mmethod(path, *args, **kwargs):
    """
    Returns a mapper function that runs the path method for each instance of
    the iterable collection.

    mmethod('start')
    <=>
    lambda thread: thread.start()

    mmethod('book_set.filter', number_of_pages__gte=100)
    <=>
    lambda author: author.book_set.filter(number_of_pages__gte=100)
    """
    return lambda x: mattr(path)(x)(*args, **kwargs)


def map_method(path, iterable):
    return map(mmethod(path), iterable)


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


def zip_with_attr(iterable, *attrs):
    """
    Zips collection of objects with instance attribute

    zip(cars, (car.price for car in cars))
    <=>
    zip_with_attr(cars, 'price')
    """

    return zip(iterable, *(
        tuple(reduce(getattr, attr.split('.'), item) for item in iterable)
        for attr in attrs
    ))


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


class Identity:
    """Utility class for the composition function.
    Acts as a placeholder for the initial value for the reduction functions
    """
    pass


_compose = lambda f, g: (
    f if g is Identity else
    lambda *args, **kwargs: f(g(*args, **kwargs))
)


def compose(*fns):
    """
    Simple function composition.
    """
    return reduce_right(_compose, fns, Identity)


def pipe(*fns):
    """
    Left-to-right composition, Unix style.
    """
    return reduce(flip(_compose), fns, Identity)
