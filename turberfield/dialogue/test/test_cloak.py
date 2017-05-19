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


from collections.abc import Callable
import copy
import itertools
import logging
import unittest

from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.player import rehearse
from turberfield.dialogue.sequences.cloak.logic import references
from turberfield.dialogue.sequences.cloak.logic import game
from turberfield.dialogue.sequences.cloak.logic import Location
from turberfield.dialogue.sequences.cloak.logic import Narrator
from turberfield.dialogue.sequences.cloak.logic import Progress


class CastingTests(unittest.TestCase):

    def setUp(self):
        self.references = references
        self.folder = copy.deepcopy(game)

    def test_foyer_scenescript(self):
        script = next(SceneScript.scripts(**self.folder._asdict()))
        with script as scene:
            model = scene.cast(scene.select(self.references)).run()
            for n, (shot, item) in enumerate(model):
                self.assertIsInstance(shot, Model.Shot)
                self.assertIsInstance(
                    item,
                    (Model.Audio, Model.Property, Model.Line, Model.Memory)
                )

                if isinstance(item, Model.Memory):
                    self.assertEqual(Progress.described, item.state)
                    self.assertTrue(item.text)
                    self.assertFalse("|" in item.text)
                    self.assertTrue(item.html)
                    self.assertFalse("|" in item.html)

class SceneTests(unittest.TestCase):

    def setUp(self):
        self.references = references
        self.folder = copy.deepcopy(game)

    def test_locations(self):
        log = logging.getLogger("turberfield")
        narrator = next(i for i in self.references if isinstance(i, Narrator))

        class MockHandler:

            def __init__(self, parent, folder, references):
                self.parent = parent
                self.folder = folder
                self.references = references
                self.repeats = 0

            def __call__(self, obj, *args, **kwargs):
                if isinstance(obj, Callable):
                    interlude = obj
                    folder, index, ensemble = args
                    if folder.paths[index] == "foyer.rst":
                        self.parent.assertEqual(Location.foyer, narrator.get_state(Location))
                        if self.repeats == 0:
                            interlude(self.folder, self.references, cmd="south")
                            self.parent.assertEqual(Location.bar, narrator.get_state(Location))
                        elif self.repeats == 1:
                            interlude(self.folder, self.references, cmd="west")
                            self.parent.assertEqual(Location.cloakroom, narrator.get_state(Location))
                        else:
                            self.parent.assertEqual(2, self.repeats)

                    elif folder.paths[index] == "bar.rst":
                        self.parent.assertEqual(0, self.repeats)
                        self.parent.assertEqual(Location.bar, narrator.get_state(Location))
                        interlude(self.folder, self.references, cmd="north")
                        self.parent.assertEqual(Location.foyer, narrator.get_state(Location))

                    elif folder.paths[index] == "cloakroom.rst":
                        self.parent.assertEqual(1, self.repeats)
                        self.parent.assertEqual(Location.cloakroom, narrator.get_state(Location))
                        interlude(self.folder, self.references, cmd="east")
                        self.parent.assertEqual(Location.foyer, narrator.get_state(Location))
                        self.repeats += 1
                    yield folder

        test_handler = MockHandler(self, self.folder, self.references)
        rv = list(rehearse(
            self.folder, self.references, test_handler, repeat=0, roles=1
        ))
