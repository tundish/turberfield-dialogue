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

from turberfield.dialogue.directives import RoleDirective
from turberfield.dialogue.model import SceneScript

from turberfield.utils.misc import group_by_type

import pkg_resources

class ScriptTests(unittest.TestCase):

    text = pkg_resources.resource_string(
            "turberfield.dialogue.sequences.battle_royal",
            "combat.rst"
    ).decode("utf-8")

    def setUp(self):
        # Think abbout selection, ordering, etc
        s = SceneScript()
        self.items = s.read(ScriptTests.text)

    def test_text(self):
        print(self.items)

    def tost_role(self):
        content = textwrap.dedent("""
            .. part:: WARDER
               :addisonarches.roles.Regulating: newboy

               An ex-military policeman who now runs a prison wing.

            .. part:: NEWBOY
               :addisonarches.attitudes.Waiting:

               A first-time prisoner.

            .. part:: OLDLAG
               :addisonarches.attitudes.Resentful:

               A hardened recidivist.
            """)
        s = SceneScript()
        objs = s.read(content)
        groups = group_by_type(objs)
        self.assertEqual(3, len(groups[RoleDirective.Node]), groups)
