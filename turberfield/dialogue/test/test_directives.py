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


import textwrap
import unittest

from turberfield.dialogue.directives import Character
from turberfield.dialogue.model import SceneScript

from turberfield.utils.misc import group_by_type


class CharacterDirectiveTests(unittest.TestCase):

    def test_empty_personae(self):
        content = textwrap.dedent("""
            .. character:: FIGHTER_1

            .. character:: FIGHTER_2

            .. character:: WEAPON

            """)
        objs = SceneScript.read(content)
        print(objs)
        groups = group_by_type(objs)
        self.assertEqual(3, len(groups[Character.Definition]), groups)

    def test_personae_with_description(self):
        content = textwrap.dedent("""
            .. character:: FIGHTER_1

            .. character:: FIGHTER_2

            .. character:: WEAPON

               A weapon which makes a noise in use. 
            """)
        doc = SceneScript.read(content)
        for n, obj in enumerate(doc):
            with self.subTest(n=n):
                self.assertIsInstance(obj, Character.Definition)
