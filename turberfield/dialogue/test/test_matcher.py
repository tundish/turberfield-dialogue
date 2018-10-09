#!/usr/bin/env python3
# encoding: utf-8

import bisect
from collections import OrderedDict
from collections.abc import Mapping
import enum
import numbers
import operator
import unittest

from turberfield.dialogue.matcher import Matcher
from turberfield.dialogue.model import SceneScript


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

class MatcherTests(unittest.TestCase):

    def setUp(self):
        self.folders = [
            SceneScript.Folder(
                "turberfield.dialogue.test", "Folder 2", {"pos": 1},
                ["two.rst"], None),
            SceneScript.Folder(
                "turberfield.dialogue.test", "Folder 1", {"pos": 0},
                ["one.rst"], None),
            SceneScript.Folder(
                "turberfield.dialogue.test", "Folder 4", {"pos": 3},
                ["four.rst"], None),
            SceneScript.Folder(
                "turberfield.dialogue.test", "Folder 3", {"pos": 2},
                ["three.rst"], None),
        ]

    def test_exact_match(self):
        matcher = Matcher(self.folders)
        self.assertEqual(4, len(matcher.keys))
        rv = list(matcher.choice(self.folders[2].metadata))
        self.assertEqual(1, len(rv))
        self.assertEqual({"pos": 3}, rv[0].metadata)
