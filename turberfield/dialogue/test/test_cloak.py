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


import copy
import unittest

from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.sequences.cloak.logic import references
from turberfield.dialogue.sequences.cloak.logic import game
from turberfield.dialogue.sequences.cloak.logic import Progress


class CastingTests(unittest.TestCase):

    def setUp(self):
        self.references = references
        self.folder = copy.deepcopy(game)

    def test_foyer_scene(self):
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
