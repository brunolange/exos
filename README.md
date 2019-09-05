## fun
### Extending your arsenal of functional tools in Python.
---
# `when`
`when` emulates pattern matching.

```python
from fun import when
a = 42
c = when(
    a < 4,   'less than 4',
    a < 10,  'less than 10',
    a == 42, 'the answer!',
)
print(c)
# the answer!
```

## Lazy evaluation

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

Either alternatively will prevent predicates and values from being evaluated
if a previously predicate is True.

## Error handling

If none of the conditions specified by the predicates are triggered, an
`NonExhaustivePattern` exception is thrown.

```python
>>> from fun import when
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
