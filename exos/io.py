"""
stateful functions
"""

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

    unpack = kwargs.get('_unpack', False)
    _ = (
        [accept(item) for item in iterable] if not unpack else
        [accept(*item) for item in iterable]
    )


def ueach(accept, iterable, *args, **kwargs):
    """
    Unpacks elements in the collection before applying the accept function.
    """
    kwargs['_unpack'] = True
    each(accept, iterable, *args, **kwargs)


def print_each(xs, prefix=''):
    """
    Prints each element in the collection given by xs.
    """
    return ueach(
        lambda i, x: print('{}{}'.format(prefix.format(i=i), x)),
        enumerate(xs)
    )


def peach(xs, prefix=''):
    """
    A shortcut to print_each
    """
    return print_each(xs, prefix=prefix)
