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
import uuid

from turberfield.dialogue.types import Persona
from turberfield.dialogue.types import Stateful
from turberfield.utils.assembly import Assembly

@enum.unique
class Animation(enum.Enum):
    angry = 0
    passive = 1
    dying = 2

@enum.unique
class Outcome(enum.Enum):
    defeated = 0
    victorious = 1

class Animal(Persona, Stateful):
    pass

class Furniture(Persona, Stateful):
    pass

class Tool(Persona, Stateful):
    pass

ensemble = [
    Animal(name="Itchy"),
    Animal(name="Scratchy"),
    Tool(name="Ol' Rusty Chopper"),
    Furniture(name="Dr Hat Stand"),
]

Assembly.register(Animal, Furniture, Tool)
