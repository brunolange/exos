import unittest
from exos import when

class TestWhen(unittest.TestCase):
    def test_eager(self):
        a = 42
        c = when(
            a < 10, 'less than 10',
            a == 42, 'the answer!',
            'something else'
        )
        self.assertEqual(c, 'the answer!')

    def test_lazy(self):
        class Stateful:
            def __init__(self, value):
                self.value = value
            def inc(self):
                self.value += 1
                return self.value

        state = Stateful(40)
        result = when(
            lambda: state.inc() == 42, 'first try!',
            lambda: state.inc() == 42, 'second try!',
            lambda: state.inc() == 42, 'third try!',
            lambda: state.inc(), 'needed more tries'
        )

        self.assertEqual(result, 'second try!')
        self.assertEqual(state.value, 42)
