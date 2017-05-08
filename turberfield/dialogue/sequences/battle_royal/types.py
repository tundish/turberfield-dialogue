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

from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Persona
from turberfield.dialogue.types import Stateful
from turberfield.utils.assembly import Assembly

@enum.unique
class Animation(EnumFactory, enum.Enum):
    angry = 0
    passive = 1
    dying = 2

@enum.unique
class Pose(EnumFactory, enum.Enum):
    toppled = 0
    standing = 1

class Animal(Stateful, Persona):
    pass

class Furniture(Stateful, Persona):
    pass

class Tool(Stateful, Persona):
    pass

ensemble = [
    Animal(name="Itchy").set_state(Pose.standing),
    Animal(name="Scratchy").set_state(Pose.standing),
    Tool(name="Ol' Rusty Chopper").set_state(Pose.standing),
    Furniture(name="Dr Hat Stand").set_state(Pose.standing),
    Animation,
    Pose
]

Assembly.register(Animal, Animation, Furniture, Pose, Tool)
