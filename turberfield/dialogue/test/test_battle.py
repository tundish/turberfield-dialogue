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
import datetime
import enum
import io
import itertools
import logging
import os
import sys
import textwrap
import tempfile
import unittest
import uuid

from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.sequences.battle_royal.types import Animal
from turberfield.dialogue.sequences.battle_royal.types import Outcome
from turberfield.dialogue.sequences.battle_royal.types import Tool
import turberfield.dialogue.viewer
from turberfield.utils.misc import log_setup

import pkg_resources


class LoaderTests(unittest.TestCase):

    def test_scripts(self):
        folder = SceneScript.Folder(
            "turberfield.dialogue.sequences.battle_royal", "test", ["combat.rst"], itertools.repeat(None)
        )
        rv = list(SceneScript.scripts(**folder._asdict()))
        self.assertEqual(1, len(rv))
        self.assertIsInstance(rv[0], SceneScript)

    def test_scripts_bad_pkg(self):
        folder = SceneScript.Folder(
            "turberfield.dialogue.sequences.not_there", "test", ["combat.rst"], itertools.repeat(None)
        )
        rv = list(SceneScript.scripts(**folder._asdict()))
        self.assertFalse(rv)

    def test_scripts_bad_scenefile(self):
        folder = SceneScript.Folder(
            "turberfield.dialogue.sequences.battle_royal", "test", ["not_there.rst"], itertools.repeat(None)
        )
        rv = list(SceneScript.scripts(**folder._asdict()))
        self.assertFalse(rv)

class CastingTests(unittest.TestCase):

    Persona = namedtuple("Persona", ["uuid", "title", "names"])
    Location = namedtuple("Location", ["name", "capacity"])

    def setUp(self):
        self.personae = {
            Animal(name="Itchy"),
            Animal(name="Scratchy"),
            Tool(name="Rusty Chopper"),
        }
        folder = SceneScript.Folder(
            "turberfield.dialogue.sequences.battle_royal", "test", ["combat.rst"], itertools.repeat(None)
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
                c, p = next((c, p) for c, p in casting.items() if "fighter_2" in c["names"])
                self.assertIsInstance(p, Animal, p)

    def test_cgi(self):
        p = turberfield.dialogue.viewer.parser()
        fd, fp = tempfile.mkstemp(suffix=".db")
        try:
            ns = p.parse_args([
                "--ensemble", "turberfield.dialogue.sequences.battle_royal.types:ensemble",
                "--sequence", "turberfield.dialogue.sequences.battle_royal:folder",
                "--db", fp,
                #"-v"
            ])
            self.assertEqual("turberfield", log_setup(ns))
            stream = io.StringIO()
            then = datetime.datetime.now()
            rv = list(turberfield.dialogue.viewer.cgi_producer(ns, stream))
            elapsed = datetime.datetime.now() - then
            self.assertEqual(8, elapsed.seconds, elapsed.seconds)

            lines = stream.getvalue().splitlines()
            self.assertEqual("Content-type:text/event-stream", lines[0])
            self.assertEqual("", lines[1])
            seq = iter(lines[2:])
            for i in range(4):
                line = next(seq)
                self.assertTrue(line.startswith("event:"))
                line = next(seq)
                self.assertTrue(line.startswith("data:"))
                line = next(seq)
                self.assertFalse(line)
        finally:
            os.close(fd)
            os.remove(fp)

    def test_run(self):
        self.assertFalse(any(i.state for i in self.personae))
        with self.script as script:
            model = script.cast(script.select(self.personae)).run()
            for n, (shot, item) in enumerate(model):
                self.assertIsInstance(shot, Model.Shot)
                self.assertIsInstance(
                    item,
                    (Model.Audio, Model.Property, Model.Line, Model.Memory)
                )

        # Last item is a Memory
        self.assertIs(Outcome.defeated, item.state)
        self.assertTrue(item.text)
        self.assertFalse("|" in item.text)
        self.assertTrue(item.html)
        self.assertFalse("|" in item.html)
