# `exos` | **ex**pressions **o**ver **s**tatements

exos is a Python module containing varied functional tools.

## `when`
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

### Lazy evaluation

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

### Error handling

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
  File "/Users/blangera/dev/fun/fun.py", line 75, in when

fun.NonExhaustivePattern
>>>
```

## `each`

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

## `ueach`

`ueach(accept, iterable, *args, **kwargs)`

`ueach` is similar to `each` except it unpacks the elements in the collection
before applying the accept function.

```python
>>> from exos import ueach
>>> ueach(
...     lambda k, v: print('{} -> {}'.format(k, v)),
...     {'a': 42, 'b': 100}.items()
... )
a -> 42
b -> 100
>>> ueach(print, enumerate(['a', 'b', 'c']))
0 a
1 b
2 c
```

## `flip`

`flip(fn)`

`flip` takes a function and returns a new function
in which the two first arguments are flipped.

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
