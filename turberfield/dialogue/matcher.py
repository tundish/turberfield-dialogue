#!/usr/bin/env python3
# encoding: utf-8

import bisect
from collections import OrderedDict
from collections.abc import Mapping
import enum
import numbers
import operator
import unittest

class Matcher:

    @staticmethod
    def flatten_mapping(obj, path=[]):
        leaves = {k: v for k, v in obj.items() if not isinstance(v, Mapping)}
        children = (k for k in obj if k not in leaves)
        for key in children:
            yield from Matcher.flatten_mapping(obj[key], path=path[:] + [key])

        yield from (
            (tuple(path + [k]), Matcher.simplify(getattr(v, "value", v)))
            for k, v in leaves.items()
        )

    @staticmethod
    def mapping_key(obj):
        return sorted(list(Matcher.flatten_mapping(obj)))

    @staticmethod
    def simplify(val):
        if val is None:
            return ""
        elif isinstance(val, numbers.Complex):
            return str(abs(val))
        elif isinstance(val, numbers.Number):
            return str(val)
        else:
            return val


class Scale(enum.IntEnum):
    one = 1
    two = 2


class Surface(enum.Enum):
    o = complex(0, 0)
    a = complex(3, 0)
    b = complex(3, 4)


class Discrete(enum.Enum):
    stop = 0
    start = 1


class DictComparisonTests(unittest.TestCase):

    def test_dict_equality(self):
        a = {"a": 1}
        b = OrderedDict([("a", 1)])
        self.assertEqual(a, b)

    def test_subtraction(self):
        a = {"a": 1}
        b = OrderedDict([("a", 2)])
        self.assertRaises(TypeError, operator.sub, a, b)

    def test_bisect(self):
        seq = ({"a": 1}, OrderedDict([("a", 2)]))
        keys = [Matcher.mapping_key(i) for i in seq]
        self.assertEqual(1, bisect.bisect_left(keys, Matcher.mapping_key({"a": 1.5})))

    def test_sort(self):
        a = {"a": 2}
        b = OrderedDict([("a", 1)])
        self.assertEqual([b, a], list(sorted((a, b), key=Matcher.mapping_key)))

    def test_sort_none(self):
        a = {"a": 2}
        b = OrderedDict([("a", None)])
        self.assertEqual([b, a], list(sorted((a, b), key=Matcher.mapping_key)))


class EnumComparisonTests(unittest.TestCase):

    def test_bisect_complex_values(self):
        self.assertGreater(abs(Surface.b.value), abs(Surface.a.value))
        seq = ({"a": Surface.o}, OrderedDict([("a", Surface.b)]))
        keys = [Matcher.mapping_key(i) for i in seq]
        self.assertEqual(1, bisect.bisect_left(keys, Matcher.mapping_key({"a": Surface.a})))

    def test_sort_complex_values(self):
        self.assertGreater(abs(Surface.a.value), abs(Surface.o.value))
        a = {"a": Surface.a}
        b = OrderedDict([("a", Surface.o)])
        self.assertEqual([b, a], list(sorted((a, b), key=Matcher.mapping_key)))

    def test_sort_nested_enums_with_complex_values(self):
        self.assertGreater(abs(Surface.a.value), abs(Surface.o.value))
        a = {"a": {"b": Surface.a}}
        b = {"a": {"b": Surface.o}}
        self.assertEqual([b, a], list(sorted((a, b), key=Matcher.mapping_key)))

    def test_intenum_types(self):
        a = {"a": Scale.two}
        b = OrderedDict([("a", Scale.one)])
        self.assertEqual([b, a], list(sorted((a, b), key=Matcher.mapping_key)))

    def test_sort_discrete_enum_types(self):
        a = {"a": Discrete.start}
        b = OrderedDict([("a", Discrete.stop)])
        self.assertEqual([b, a], list(sorted((a, b), key=Matcher.mapping_key)))

if __name__ == "__main__":
    unittest.main()
