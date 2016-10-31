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


class DataObject:

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<{0}> {1}".format(type(self).__name__, vars(self))

class Persona(DataObject):

    Name = namedtuple("Name", ["title", "firstname", "nicknames", "surname"])

    def __init__(self, **kwargs):
        bits = kwargs.pop("name").split()
        self.name = Persona.Name(bits[0], bits[1], bits[2:-1], bits[-1])
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
