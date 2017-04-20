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


import enum
import sys
import textwrap
import unittest

from turberfield.dialogue.directives import Entity
from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Player
from turberfield.dialogue.model import SceneScript


class PropertyDirectiveTests(unittest.TestCase):

    personae = [
        Player(name="Prof William Fuzzer Q.A Testfixture"),
        Player(name="Ms Anna Conda"),
        Player(name="A Big Hammer")
    ]

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
        script.cast(script.select([self.personae[0]]))
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
        script.cast(script.select([self.personae[0]]))
        model = script.run()
        shot, line = next(iter(model))
        self.assertEqual("scene", shot.scene)
        self.assertEqual("shot", shot.name)
        self.assertIn(line.text, (
            "You can call me  Fuzzer .",
            "You can call me  Q.A ."))

class FXDirectiveTests(unittest.TestCase):

    def test_fx(self):
        content = textwrap.dedent(
            """
            Scene
            ~~~~~

            Shot
            ----

            .. fx:: turberfield.dialogue.sequences.battle_royal whack.wav
               :offset: 0
               :duration: 3000
               :loop: 1

            """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        model = script.run()
        shot, cue = next(iter(model))
        self.assertEqual(
            "turberfield.dialogue.sequences.battle_royal",
            cue.package
        )
        self.assertEqual("whack.wav", cue.resource)
        self.assertEqual(0, cue.offset)
        self.assertEqual(3000, cue.duration)
        self.assertEqual(1, cue.loop)

class SelectTests(unittest.TestCase):

    @enum.unique
    class Aggression(EnumFactory, enum.Enum):
        calm = 0
        angry = 1

    @enum.unique
    class Contentment(EnumFactory, enum.Enum):
        sad = 0
        happy = 1

    def test_entitys_with_declared_state_and_content(self):

        content = textwrap.dedent("""
            .. entity:: FIGHTER_1
               :states: turberfield.dialogue.test.test_model.SelectTests.Aggression.angry

            .. entity:: FIGHTER_2
               :states: turberfield.dialogue.test.test_model.SelectTests.Contentment.sad

            .. entity:: WEAPON

               A weapon which makes a noise in use. 
            """)
        ensemble = PropertyDirectiveTests.personae[:]
        ensemble[0].set_state(SelectTests.Contentment.sad)
        self.assertEqual(
            SelectTests.Contentment.sad,
            ensemble[0].get_state(SelectTests.Contentment)
        )
        script = SceneScript("inline", doc=SceneScript.read(content))
        rv = script.select(ensemble)
        self.assertEqual(ensemble[0], list(rv.values())[1])
