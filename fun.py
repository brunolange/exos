""" fun.py
Extended functional tools
"""

from functools import partial, reduce
from operator import iconcat

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'

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
        map(accept, iterable) if not kwargs.get('_unpack', False) else
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

flip = lambda f: lambda x, y: f(y, x)

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
    return lambda x: partial(reduce, getattr, path.split('.'))(x)(*args, **kwargs)

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
