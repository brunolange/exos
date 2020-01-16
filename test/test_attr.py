import unittest

from exos import setattr_, setattrs


class Car:
    def __init__(self):
        self.make = None
        self.model = None
        self.price = None


class TestCompose(unittest.TestCase):
    def test_setattr_(self):
        car = Car()
        ride = setattr_(car, 'make', 'Volvo')
        self.assertTrue(car is ride)
        self.assertEqual(car.make, 'Volvo')

    def test_setattrs(self):
        car = setattrs(Car(), {'make': 'Jeep', 'model': 'Patriot'}, year=2011)
        self.assertEqual(car.make, 'Jeep')
        self.assertEqual(car.model, 'Patriot')
        self.assertEqual(car.year, 2011)
