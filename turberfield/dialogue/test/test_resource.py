#!/usr/bin/env python3
# encoding: UTF-8

# This file is part of turberfield.
#
# Turberfield is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Turberfield is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with turberfield.  If not, see <http://www.gnu.org/licenses/>.

from collections import namedtuple
import copy
import enum
import sys
import textwrap
import unittest
import uuid

from turberfield.dialogue.types import Player

class ResourceTests(unittest.TestCase):
    phrases = [
        "Explicit is better than implicit.",
        "Simple is better than complex.",
        "Complex is better than complicated.",
        "Readability counts.",
        "Special cases aren't special enough to break the rules.",
        "Practicality beats purity.",
        "Errors should never pass silently."
    ]

    class Session:

        def __init__(self, host="localhost", id=None):
            self.host = host
            self.id = id or uuid.uuid4().hex
            self.resources = []

        @property
        def addition(self):
            return next(reversed(self.resources), None)

        @addition.setter
        def addition(self, item):
            self.resources.append(item)

    Resource = namedtuple("Resource", ["label", "path"])

    def test_session(self):
        s = ResourceTests.Session()
        self.assertTrue(s.host)
        self.assertTrue(s.id)
        self.assertFalse(s.resources)

    def test_session_addition(self):
        s = ResourceTests.Session()
        self.assertIsNone(s.addition)
        s.addition = 1
        self.assertEqual(1, s.addition)
        self.assertTrue(s.resources)
        self.assertEqual([1], s.resources)

    def test_resource_activation(self):

        references = [
            ResourceTests.Resource(p, "phrases/{0}".format(n + 1)
            for n, p in enumerate(ResourceTests.phrases)
        ]
        references.extend([
            Player(name="Mr Tim Peters"),
            Player(name="tundish"),
            ResourceTests.Session()
        ])

        self.fail(references)
