import unittest
from dataclasses import dataclass


class Container:
    @dataclass
    class _Group:
        amount: float = 0.0
        container_count: int = 1

    def __init__(self):
        self._group = Container._Group()

    def add_water(self, amount: float):
        new_amount = self._group.amount + amount

        if new_amount < 0:
            raise RuntimeError("Insufficient water")

        self._group.amount = new_amount

    def connect_to(self, other: "Container"):
        if self is other:
            return
        self._group.amount += other._group.amount
        self._group.container_count += other._group.container_count
        other._group = self._group

    @property
    def amount(self) -> float:
        return self._group.amount / self._group.container_count


class UseCaseTest(unittest.TestCase):

    def test_use_case(self):
        a = Container()
        b = Container()
        c = Container()
        d = Container()

        a.add_water(12)
        d.add_water(8)
        a.connect_to(b)
        b.connect_to(c)

        self.assertEqual(4, a.amount)
        self.assertEqual(4, b.amount)
        self.assertEqual(4, c.amount)
        self.assertEqual(8, d.amount)

    def test_insufficient_water_single(self):
        a = Container()
        a.add_water(1)
        a.add_water(2)
        a.add_water(2)
        with self.assertRaises(RuntimeError):
            a.add_water(-10.0)

    def test_insufficient_water_multiple(self):
        a = Container()
        b = Container()
        c = Container()

        a.add_water(12)
        a.connect_to(b)
        b.connect_to(c)

        with self.assertRaises(RuntimeError):
            a.add_water(-13)

    def test_connect_to_myself(self):
        a = Container()
        a.add_water(12)
        a.connect_to(a)

        self.assertEqual(12, a.amount)

    def test_bidirectional_connection(self):
        a = Container()
        b = Container()

        a.add_water(12)
        a.connect_to(b)
        b.connect_to(a)

        self.assertEqual(6, a.amount)

    def test_arbitrary_use_case(self):
        a = Container()
        b = Container()
        c = Container()

        a.add_water(2)
        b.add_water(4)
        a.connect_to(b)
        c.add_water(6)
        b.add_water(6)
        c.connect_to(a)

        self.assertEqual(6, a.amount)
        self.assertEqual(6, b.amount)
        self.assertEqual(6, c.amount)