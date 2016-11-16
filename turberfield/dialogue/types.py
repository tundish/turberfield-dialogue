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

from collections import namedtuple
import enum
import random

Name = namedtuple("Name", ["title", "firstname", "nicknames", "surname"])

class EnumFactory:

    @classmethod
    def factory(cls, name=None, **kwargs):
        return cls[name]

@enum.unique
class Ownership(EnumFactory, enum.Enum):
    lost = 0
    acquired = 1

@enum.unique
class Presence(EnumFactory, enum.Enum):
    invisible = 0
    visible = 1
    shine = 2
    fade = 3
    throb = 4

@enum.unique
class Vocabulary(EnumFactory, enum.Enum):
    forgot = 0
    prompted = 1

class DataObject:

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<{0}> {1}".format(type(self).__name__, vars(self))

class Persona(DataObject):

    def __init__(self, **kwargs):
        val = kwargs.pop("name")
        bits = val.split()
        try:
            self.name = Name(bits[0], bits[1], bits[2:-1], bits[-1])
        except IndexError:
            self.name = Name("", val, [], "")
        super().__init__(**kwargs)

    @property
    def nickname(self):
        return random.choice(self.name.nicknames)


class Stateful:

    def __init__(self, **kwargs):
        self._states = {}
        super().__init__(**kwargs)

    @property
    def state(self):
        return self._states

    @state.setter
    def state(self, value):
        self._states[type(value)] = value

    @state.deleter
    def state(self):
        self.state = {}

class Player(Stateful, Persona):
    pass
