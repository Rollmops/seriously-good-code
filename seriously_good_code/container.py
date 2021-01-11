import unittest
from contextlib import contextmanager
from dataclasses import dataclass
from time import time
from typing import Set


@contextmanager
def time_it():
    start = time()
    yield
    print(time() - start)


class Container:
    @dataclass
    class _Group:
        amount_per_container: float
        containers: Set["Container"]

    def __init__(self):
        self._group = Container._Group(amount_per_container=0.0, containers={self})

    def add_water(self, amount: float):
        new_amount_per_container = self._group.amount_per_container + amount / len(self._group.containers)

        if new_amount_per_container < 0:
            raise RuntimeError("Insufficient amount of water in the containers")

        self._group.amount_per_container = new_amount_per_container

    def connect_to(self, other: "Container"):
        amount_in_group = self._group.amount_per_container * len(self._group.containers)
        for container_in_group in other._group.containers:
            self._group.containers.add(container_in_group)
            other._group = self._group

        self._group.amount_per_container = amount_in_group / len(self._group.containers)

    @property
    def amount(self):
        return self._group.amount_per_container


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
