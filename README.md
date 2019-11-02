# `exos` | expressions over statements

exos is a Python module containing varied functional tools.

## Installation

`exos` is compatible with Python 3. Install it with `pip`:

```bash
$ pip install exos
```

## Documentation

### `memoize`

In functional programming lingo, *referential transparency* is a term that refers
to expressions that can be replaced with their value without altering the program's
behavior. For that to be the case, referentially transparent functions need to be
*pure*, that is, they must always produce the same output when given then same
inputs and they cannot have any effects on the outside world. In other words,
they have no *side effects*.

Functions that fit this bill can benefit from a performance optimization technique
known as *memoization*. Since pure functions always return the same output given
the same inputs and have no effect on the outside world, by storing calculated values
in a lookup table, whenever a function gets called on reoccurring inputs we can simply
look up the previously calculated value instead of performing a potentially costly
calculation again.

`exos` provides a function decorator aptly called `memoize` which sets up this
automatic caching.

```python
>>> from exos import memoize
>>> import timeit
>>> def fibo(n):
...     return 1 if n <= 2 else fibo(n-1) + fibo(n-2)
...
>>> timeit.repeat("fibo(30)", "from __main__ import fibo", number=3)
[8.696023122000042, 8.712087763, 8.689468796000256]
>>> # well, that took a while, let's redefine it with memoize
...
>>> @memoize
... def fibo(n):
...     return 1 if n <= 2 else fibo(n-1) + fibo(n-2)
...
>>> timeit.repeat("fibo(30)", "from __main__ import fibo", number=3)
[4.720499964605551e-05, 8.240000170189887e-06, 7.680000180698698e-06]
>>> # blazing fast!
```

### `curry`

The bread and butter of functional programming, *currying* allows you to provide
a function with an incomplete set of arguments, getting in return a partially
applied function.

```python
>>> def volume(height, width, depth):
...     return height * width * depth
...
>>> volume(1, 4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: volume() missing 1 required positional argument: 'depth'
>>>
>>> from exos import curry
>>> @curry
... def volume(height, width, depth):
...     return height * width * depth
...
>>> volume(2, 3)
>>> <function curry.<locals>.curried at 0x102920e18>
>>> volume(1,2,3) == volume(1)(2)(3) == volume(1,2)(3) == volume(1)(2,3) == 6
True
>>> list(map(volume(0.5, 2.25), range(1, 10)))
[1.125, 2.25, 3.375, 4.5, 5.625, 6.75, 7.875, 9.0, 10.125]
```

### `compose`

Simple function composition.

```python
>>> from exos import compose
>>> f = lambda x: x**2
>>> g = lambda x: -x
>>> w = compose(f, g) # w(x) = f . g = f(g(x))
>>> h = compose(g, f) # h(x) = g . f = g(f(x))
>>> w(3)
9
>>> h(3)
-9
```

### `pipe`

Function composition, Unix-style.

```python
>>> from exos import pipe
>>> pipe(lambda s: s.upper(), print)('hello world!')
HELLO WORLD!
```

### `each`

`each(accept, iterable, *args, **kwargs)`

`each` applies the accept function to each of the elements in the iterable
collection.

```python
>>> from exos import each
>>> each(print, range(5))
0
1
2
3
4
```

### `ueach`

`ueach(accept, iterable, *args, **kwargs)`

`ueach` is similar to `each` except it unpacks the elements in the collection
before applying the accept function.

```python
>>> from exos import ueach
>>> ueach(
...     lambda k, v: print('{} >=> {}'.format(k, v)),
...     {'a': 42, 'b': 100}.items()
... )
a >=> 42
b >=> 100
>>> ueach(print, enumerate(['a', 'b', 'c']))
0 a
1 b
2 c
```

### `flatten`
Flattens a nested collection.

```python
>>> from exos import flatten
>>> flatten([[1,2,3], [4,5,6]])
>>> [1, 2, 3, 4, 5, 6]
```

### `when`
`when` is the declarative version of a switch statement.

```python
from exos import when
a = 42
c = when(
    a < 4,   'less than 4',
    a < 10,  'less than 10',
    a == 42, 'the answer!',
)
print(c)
# the answer!
```
is imperatively equivalent to
```python
a = 42
if a < 42:
    c = 'less than 4'
elif a < 10:
    c = 'less than 10'
elif a == 42:
    c = 'the answer!'
```

Notice how, in this example, if `a > 42` then `c` is undefined and could cause
problems down the road when `c` is actually used. To prevent such scenarios,
include an argument to `when` that does not pair up with a predicate to
indicate the default value:
```python
c = when(
    a < 4,   'less than 4',
    a < 10,  'less than 10',
    a == 42, 'the answer!',
    'greater than 42'
)
```

#### Lazy evaluation

If you want to defer evaluation of either predicates or values, use a lambda or `functools.partial`.

```python
value = when(
    condition_1(arg1, arg2), 'a string',
    condition_2(arg1, arg2), value_2(),
    condition_3(),           value_3(arg1),
    otherwise()
)
```
can be lazily evaluated like so:
```python
value = when(
    lambda: condition_1(arg1, arg2), 'a string',
    lambda: condition_2(arg1, arg2), lambda: value_2(),
    lambda: condition_3(),           lambda: value_3(arg1),
    lambda: otherwise()
)
```
or, alternatively,
```python
from functools import partial as p
value = when(
    p(condition_1, arg1, arg2), 'a string',
    p(condition_2, arg1, arg2), p(value_2),
    p(condition_3,              p(value_3, arg1),
    p(otherwise)
)
```

Either alternative will prevent predicates and values from being evaluated
if a previously evaluated predicate is True.

#### Error handling

If none of the conditions specified by the predicates are triggered, a
`NonExhaustivePattern` exception is thrown.

```python
>>> from exos import when
>>> a = 42
>>> when(
...     a < 0, 'a is negative',
...     a < 10, 'a is less than 10',
... )
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/blangera/dev/exos/exos.py", line 75, in when

exos.NonExhaustivePattern
>>>
```

### `flip`

`flip(fn)`

`flip` takes a function and returns a new function for which the first two
arguments are flipped.

```python
>>> from exos import flip
>>> subtract = lambda a, b: a - b
>>> subtract(10, 3)
7
>>> f = flip(subtract)
>>> f(10, 3)
-7
>>> coord = lambda x, y, z: (x, y, z)
>>> flip(coord)(1,2,0)
(2,1,0)
```

```python
>>> from functools import partial
>>> from exos import flip, each
>>> is_string = partial(flip(isinstance), str)
>>> each(print, filter(is_string, ['forty two', 42, True, '', 'done']))
forty two

done
```
