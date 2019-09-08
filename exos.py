""" exos.py
EXpressions Over Statements: extended functional tools in Python.
"""

from functools import partial, reduce, wraps
from operator import iconcat
from inspect import getfullargspec
from collections import defaultdict

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'

class NonExhaustivePattern(Exception):
    """
    Thrown when pattern matching fails to find a matching predicate.
    """
    pass

def _pairs(*args):
    def fold(acc, curr):
        if len(acc[-1]) < 2:
            acc[-1].append(curr)
        else:
            acc.append([curr])
        return acc
    payload = reduce(fold, args, [[]])
    last = payload[-1]
    if len(last) < 2:
        last.insert(0, True)
    return payload

def when(*args):
    """
    Pattern matching FTW
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
    >>> when(
        condition_1(arg1, arg2), value_1(arg1, arg2),
        condition_2(arg1, arg2), value_2(),
        condition_3(),           value_3(arg1),
        otherwise()
    )
    's lazy alternative:
    >>> import exos
    >>> exos.when(
        lambda: condition_1(arg1, arg2), 'a string',
        lambda: condition_2(arg1, arg2), lambda: value_2(),
        lambda: condition_3(),           lambda: value_3(arg1),
        lambda: otherwise()
    )
    or, alternatively:
    >>> from functools import partial as p
    >>> exos.when(
        p(condition_1,arg1, arg2),  'a string',
        p(condition_2,arg1, arg2),  p(value_2),
        p(condition_3,              p(value_3, arg1),
        p(otherwise)
    )
    """
    for predicate, value in _pairs(*args):
        predicate = predicate() if callable(predicate) else predicate
        if predicate:
            return value() if callable(value) else value
    raise NonExhaustivePattern()

def each(accept, iterable, *args, **kwargs):
    """
    Applies the accept function to each of the elements in the iterable
    collection.
    """
    if isinstance(accept, str):
        methods = [getattr(item, accept) for item in iterable]
        _ = [method(*args, **kwargs) for method in methods]
        return

    _ = (
        [accept(item) for item in iterable] if not kwargs.get('_unpack', False) else
        [accept(*item) for item in iterable]
    )

def ueach(accept, iterable, *args, **kwargs):
    """
    Unpacks elements in the collection before applying the accept function.
    """
    kwargs['_unpack'] = True
    each(accept, iterable, *args, **kwargs)

# ueach = partial(each, _unpack=True)

def print_each(xs, prefix=''):
    """
    Prints each element in the collection given by xs.
    """
    return ueach(
        lambda i, x: print('{}{}'.format(prefix, x).format(i=i)),
        enumerate(xs)
    )

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
        return tuple((k,self[k]) for k in sorted(self))
    def __hash__(self):
        return hash(self.__key())
    def __eq__(self, other):
        return self.__key() == other.__key()

def memoize(fn):
    """
    Decorator that provides automatic caching for referentially transparent
    functions.
    """
    class NotInCache(object):
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
