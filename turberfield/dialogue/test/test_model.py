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

from turberfield.dialogue.types import Player
from turberfield.dialogue.model import SceneScript


class PropertyDirectiveTests(unittest.TestCase):

    player = Player(name="Prof William Fuzzer Q.A Testfixture") 

    def test_property_getter(self):
        content = textwrap.dedent("""
            .. entity:: P

            Scene
            ~~~~~

            Shot
            ----

            [P]_

                Hi, I'm |P_FIRSTNAME|.

            .. |P_FIRSTNAME| property:: P.name.firstname
            """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        script.cast(script.select([self.player]))
        model = script.run()
        shot, line = next(iter(model))
        self.assertEqual("scene", shot.scene)
        self.assertEqual("shot", shot.name)
        self.assertEqual("Hi, I'm  William .", line.text)

    def test_nickname_getter(self):
        content = textwrap.dedent(
            """
            .. entity:: P

            Scene
            ~~~~~

            Shot
            ----

            [P]_

                You can call me |P_NICKNAME|.

            .. |P_NICKNAME| property:: P.nickname
            """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        script.cast(script.select([self.player]))
        model = script.run()
        shot, line = next(iter(model))
        self.assertEqual("scene", shot.scene)
        self.assertEqual("shot", shot.name)
        self.assertIn(line.text, (
            "You can call me  Fuzzer .",
            "You can call me  Q.A ."))
