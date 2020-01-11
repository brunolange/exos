import unittest
from exos import each, ueach, peach
from functools import partial
import sys

class TestIO(unittest.TestCase):
    def test_each(self):
        list_of_lists = [
            [0],
            [0, 1],
            [0, 1, 2]
        ]
        each(lambda l: l.append('the end'), list_of_lists)
        self.assertEqual(list_of_lists, [
            [0, 'the end'],
            [0, 1, 'the end'],
            [0, 1, 2, 'the end']
        ])

    def test_ueach(self):
        class C:
            pass
        ueach(partial(setattr, C), {'a': 42, 'b': 100}.items())
        self.assertEqual(getattr(C, 'a'), 42)
        self.assertEqual(getattr(C, 'b'), 100)

    def test_peach(self):
        class Buffer:
            def __init__(self):
                self.content = ''
            def write(self, string):
                self.content += string
            def flush(self):
                self.content = ''

        buffer = Buffer()
        sys.stdout = buffer

        def assertPeach(iterable, string, **kwargs):
            buffer.flush()
            peach(iterable, **kwargs)
            self.assertEqual(buffer.content, string)

        assertPeach(range(3), '0\n1\n2\n')
        assertPeach('abcd', 'a\nb\nc\nd\n')
        assertPeach('abcd', '\n'.join([
            line.strip()
            for line in filter(
                None,
                """
                0: a
                1: b
                2: c
                3: d
                """.split('\n')
            )
        ]), prefix='{i}: ')
