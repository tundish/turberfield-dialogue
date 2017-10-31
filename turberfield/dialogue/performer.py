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

from collections import defaultdict

from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript


class Performer:

    @staticmethod
    def next(folders, ensemble, strict=True, roles=1):
        for folder in folders:
            scripts = SceneScript.scripts(**folder._asdict())
            for script in scripts:
                with script as dialogue:
                    selection = dialogue.select(ensemble, roles=roles)
                    if all(selection.values()):
                        return (script, selection)
                    elif not strict and any(selection.values()):
                        return (script, selection)
        else:
            return None

    @property
    def stopped(self):
        return not bool(self.next(self.folders, self.ensemble))

    def __init__(self, folders, ensemble):
        self.folders = folders
        self.ensemble = ensemble
        self.metadata = defaultdict(list)
        self.shots = []
        self.script = None
        self.selection = None

    def react(self, obj):
        if isinstance(obj, Model.Property):
            if obj.object is not None:
                setattr(obj.object, obj.attr, obj.val)
        return obj

    def run(self, react=True, strict=True, roles=1):
        try:
            self.script, self.selection = self.next(
                self.folders, self.ensemble,
                strict=strict, roles=roles
            )
        except TypeError:
            raise GeneratorExit
        with self.script as dialogue:
            model = dialogue.cast(self.selection).run()
            for shot, item in model:
                yield shot
                yield item
                if not self.shots or self.shots[-1][:2] != shot[:2]:
                        self.shots.append(shot._replace(items=self.script.fP))
                if react:
                    self.react(item)
            for key, value in model.metadata:
                if value not in self.metadata[key]:
                    self.metadata[key].append(value)
