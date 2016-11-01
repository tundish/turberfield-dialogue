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


import sys
import textwrap
import unittest

from turberfield.dialogue.directives import Entity
from turberfield.dialogue.model import SceneScript

from turberfield.utils.misc import group_by_type


class EntityDirectiveTests(unittest.TestCase):

    class Outer:
        class Inner:
            pass

    @unittest.skipIf(
        "discover" not in sys.argv,
        "Testing relative import: Needs ~/py3.5/bin/python -m unittest discover turberfield"
    )
    def test_string_import_relative(self):
        rv = Entity.Definition.string_import(
            ".dialogue.test.test_directives.EntityDirectiveTests",
            relative=True
        )
        self.assertIs(rv, EntityDirectiveTests)

        rv = Entity.Definition.string_import(
            ".dialogue.test.test_directives.EntityDirectiveTests.Outer",
            relative=True
        )
        self.assertIs(rv, EntityDirectiveTests.Outer)

        rv = Entity.Definition.string_import(
            ".dialogue.test.test_directives.EntityDirectiveTests.Outer.Inner",
            relative=True
        )
        self.assertIs(rv, EntityDirectiveTests.Outer.Inner)

    @unittest.skipIf(
        "discover" in sys.argv,
        ("Testing namespace import: "
        "Needs ~/py3.5/bin/python -m unittest turberfield.dialogue.test.test_directives")
    )
    def test_string_import_namespace(self):
        rv = Entity.Definition.string_import(
            "turberfield.dialogue.test.test_directives.EntityDirectiveTests",
            relative=False
        )
        self.assertIs(rv, EntityDirectiveTests)

        rv = Entity.Definition.string_import(
            "turberfield.dialogue.test.test_directives.EntityDirectiveTests.Outer",
            relative=False
        )
        self.assertIs(rv, EntityDirectiveTests.Outer)

        rv = Entity.Definition.string_import(
            "turberfield.dialogue.test.test_directives.EntityDirectiveTests.Outer.Inner",
            relative=False
        )

    def test_empty_entitys(self):
        content = textwrap.dedent("""
            .. entity:: FIGHTER_1

            .. entity:: FIGHTER_2

            .. entity:: WEAPON

            """)
        objs = SceneScript.read(content)
        groups = group_by_type(objs)
        self.assertEqual(3, len(groups[Entity.Definition]), groups)

    def test_entitys_with_options_and_content(self):
        content = textwrap.dedent("""
            .. entity:: FIGHTER_1

            .. entity:: FIGHTER_2
               :types: turberfield.dialogue.test.test_battle.CastingTests.Animal
               :states: active

            .. entity:: WEAPON

               A weapon which makes a noise in use. 
            """)
        doc = SceneScript.read(content)
        for n, obj in enumerate(doc):
            with self.subTest(n=n):
                self.assertIsInstance(obj, Entity.Definition)
                self.assertTrue(obj["names"])

                if n == 0:
                    self.assertFalse(obj["content"])
                elif n == 1:
                    self.assertEqual(
                        ["turberfield.dialogue.test.test_battle.CastingTests.Animal"],
                        obj["options"]["types"]
                    )
                    self.assertEqual(["active"], obj["options"]["states"])
                    self.assertFalse(obj["content"])
                elif n == 2:
                    self.assertTrue(obj["content"])
