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

from turberfield.dialogue.types import Stateful

@enum.unique
class Animation(enum.Enum):
    angry = 0
    passive = 1
    dying = 2

@enum.unique
class Outcome(enum.Enum):
    defeated = 0
    victorious = 1

class Animal(Stateful):

    def __init__(self, id_, title, names):
        self.id_, self.title, self._names = id_, title, names
        self.name = self._names[0]
        super().__init__()

class Furniture(Stateful):

    def __init__(self, id_, names):
        self.id_, self.names = id_, names
        super().__init__()

class Tool(Stateful):

    def __init__(self, id_, names):
        self.id_, self._names = id_, names
        self.name = " ".join(self._names)
        super().__init__()
