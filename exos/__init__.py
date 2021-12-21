""" exos.py
EXpressions Over Statements: extended functional tools in Python.
"""

import threading
from functools import partial, reduce
from inspect import getfullargspec
from operator import iconcat

from .decorators import curry, fattr, memoize
from .exceptions import NonExhaustivePattern
from .io import each, peach, print_each, ueach
from .utils import pairs

__author__ = "Bruno Lange"
__email__ = "blangeram@gmail.com"
__license__ = "MIT"


def when(*args):
    """
    A declarative approach to a switch statement.
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
    """
    Takes a function that takes two or more positional parameters
    and returns another one where the first two positional parameters
    are flipped.

    >>> def statement(a, b):
    ...     print("I'm {} if and only if I'm {}.".format(a, b))
    ...
    >>> statement('alive', 'breathing')
    I'm alive if and only if I'm breathing.
    >>> flip(statement)('alive', 'breathing')
    I'm breathing if and only if I'm alive.
    """
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
    return partial(reduce, getattr, attr.split("."))


class XAttrNoDefault:
    pass


def xattr(obj, attr, default=XAttrNoDefault):
    """
    Similar to getattr except it allows for deep extraction
    of attributes by splitting them with a dot. Unless a
    default value is provided, an AttributeError exception
    is thrown when the attribute does not exist.

    >>> xattr(matrix, 'rank') # same as getattr(matrix, 'rank') or matrix.rank
    4
    >>> xattr(wave, 'amplitude.imag')
    1.618
    """
    return reduce(
        getattr if default is XAttrNoDefault else
        lambda acc, curr: getattr(acc, curr, default),
        attr.split('.'),
        obj
    )


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

    >>> mmethod('start')
    is equivalent to
    >>> lambda thread: thread.start()

    >>> mmethod('book_set.filter', number_of_pages__gte=100)
    is equivalent to
    >>> lambda author: author.book_set.filter(number_of_pages__gte=100)
    """
    return lambda x: mattr(path)(x)(*args, **kwargs)


def map_method(path, iterable):
    """
    Returns a map object in which each item corresponds to the method
    given by `path` called on the objects in the iterable collection.
    >>> map('magnitude', [v1, v2, v3])
    is equivalent to
    >>> map(lambda v: v.magnitude(), [v1, v2, v3])
    """
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

    return zip(
        iterable, *(tuple(xattr(item, attr) for item in iterable) for attr in attrs)
    )


def unpack(iterable, *attrs):
    """Unpacks the iterable in parity with the attributes passed.
    ```
    >>> @dataclass
    ... class Point:
    ...     u: float
    ...     v: float
    ...
    >>> points: List[Point] = get_points()
    >>> for u, v in unpack(points, "u", "v"):
    ...     print(u, v)
    ```
    """
    for x in iterable:
        yield tuple(getattr(x, a) for a in attrs)


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
    Acts as a placeholder for the initial value of the reduction functions
    """

    pass


_compose = lambda f, g: (
    f if g is Identity else lambda *args, **kwargs: f(g(*args, **kwargs))
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


def setattr_(obj, name, value):
    """Similar to setattr except it returns back the modified object.
    """
    setattr(obj, name, value)
    return obj


def setattrs(obj, *args, **kwargs):
    """Allows for multiple attributes to be set from dictionaries
    passed as positional arguments or named parameters.
    >>> setattrs(car, {'make': 'Jeep', 'model': 'Patriot'}, year=2011)
    <__main__.Car object at 0x103331320>
    >>> car.make, car.model, car.year
    ('Jeep', 'Patriot', 2011)
    """
    attrs = extend(*args, kwargs)
    return reduce(
        lambda acc, curr: setattr_(acc, *curr),  # curr <- (k, v)
        attrs.items(),
        obj
    )


def take(n, collection):
    """Returns at most n items from the collection in a list
    >>> take(4, range(100000, 1000000, 4))
    [100000, 100004, 100008, 100012]
    >>> take(10, ['hello', 'world'])
    ['hello', 'world']
    """
    return [item for item, _ in zip(collection, range(n))]


def take_while(predicate, collection):
    """Returns a list corresponding to the longest prefix
    of the original list for which all the values when
    tested against the given predicate return True
    >>> take_while(lambda x: x<=10, range(10000))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    payload = []
    for item in collection:
        if not predicate(item):
            break
        payload.append(item)
    return payload


def tmap(fn, collection):
    """Concurrent map. Map each item in the collection with
    the provided function in a separate thread.
    `tmap` can drastically improve performance when compared to
    `map` but should only be used for IO-bound functions that have
    no side effects.
    >>> tmap(download, urls)
    [<url1_data>, <url2_data>, <url3_data>]
    >>> datasets = tmap(read_csv, files)
    """
    n = len(collection)
    payload = [None] * n

    def process(i):
        payload[i] = fn(collection[i])

    threads = [threading.Thread(target=process, args=(i,)) for i in range(n)]

    each("start", threads)
    each("join", threads)

    return payload


def teach(fn, collection):
    """Concurrently digest each item in the collection with
    the provided function.
    >>> tmap(save_to_disk, documents)
    """
    threads = [threading.Thread(target=fn, args=(item,)) for item in collection]

    each("start", threads)
    each("join", threads)
