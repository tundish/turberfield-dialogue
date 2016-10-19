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


import collections.abc
from collections import namedtuple
import sys
import textwrap
import unittest
import uuid

from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.sequences.battle_royal.types import Animal

import pkg_resources


class LoaderTests(unittest.TestCase):

    def test_scripts(self):
        folder = SceneScript.Folder(
            "turberfield.dialogue.sequences.battle_royal", "test", ["combat.rst"]
        )
        rv = list(SceneScript.scripts(**folder._asdict()))
        self.assertEqual(1, len(rv))
        self.assertIsInstance(rv[0], SceneScript)

    def test_scripts_bad_pkg(self):
        folder = SceneScript.Folder("turberfield.dialogue.sequences.not_there", "test", ["combat.rst"])
        rv = list(SceneScript.scripts(**folder._asdict()))
        self.assertFalse(rv)

    def test_scripts_bad_scenefile(self):
        folder = SceneScript.Folder(
            "turberfield.dialogue.sequences.battle_royal", "test", ["not_there.rst"]
        )
        rv = list(SceneScript.scripts(**folder._asdict()))
        self.assertFalse(rv)

class CastingTests(unittest.TestCase):

    Persona = namedtuple("Persona", ["uuid", "title", "names"])
    Location = namedtuple("Location", ["name", "capacity"])

    def setUp(self):
        self.personae = {
            Animal(uuid.uuid4(), None, ("Itchy",)),
            Animal(uuid.uuid4(), None, ("Scratchy",)),
            CastingTests.Persona(uuid.uuid4(), None, ("Rusty", "Chopper",)),
        }
        folder = SceneScript.Folder(
            "turberfield.dialogue.sequences.battle_royal", "test", ["combat.rst"]
        )
        self.script = next(SceneScript.scripts(**folder._asdict()))

    def test_casting_adds_citation_definition(self):
        with self.script as script:
            self.assertFalse(script.doc.citations)
            self.assertEqual(3, len(script.doc.citation_refs))
            casting = script.select(self.personae)
            self.assertIsInstance(casting, collections.abc.Mapping, casting)
            script.cast(casting)
            self.assertEqual(3, len(script.doc.citations))
            self.assertEqual(3, len(script.doc.citation_refs))

    def test_casting_respects_type(self):
        for n in range(16):
            self.setUp()
            with self.subTest(n=n), self.script as script:
                casting = script.select(self.personae)
                p, c = next((p, c) for p, c in casting.items() if "fighter_2" in c["names"])
                self.assertIsInstance(p, Animal, p)
