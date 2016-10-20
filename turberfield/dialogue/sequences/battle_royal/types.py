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
class Availability(enum.Enum):
    mist = 0
    passive = 1
    active = 2

class Animal(Stateful):

    def __init__(self, id_, title, names):
        self.id_, self.title, self._names = id_, title, names
        self.name = self._names[0]

class Furniture(Stateful):

    def __init__(self, id_, names):
        self.id_, self.names = id_, names

class Tool(Stateful):

    def __init__(self, id_, names):
        self.id_, self.names = id_, names
