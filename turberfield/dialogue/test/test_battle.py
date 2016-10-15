#!/usr/bin/env python
#   -*- encoding: UTF-8 -*-

# This file is part of Turberfield Dialogue.
#
# Turberfield Dialogue is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Turberfield Dialogue is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Turberfield Dialogue.  If not, see <http://www.gnu.org/licenses/>.

import textwrap
import unittest

from turberfield.dialogue.directives import RoleDirective
from turberfield.dialogue.model import group_by_type
from turberfield.dialogue.model import SceneScript

class RoleDirectiveTests(unittest.TestCase):

    def test_role(self):
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
