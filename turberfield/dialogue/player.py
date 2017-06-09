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

import datetime
import itertools
import logging

from turberfield.dialogue.directives import Pathfinder
from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.schema import SchemaBase

def run_through(script, ensemble, roles=1):
    """
    :py:class:`turberfield.dialogue.model.SceneScript`.
    """
    then = datetime.datetime.now()
    with script as dialogue:
        selection = dialogue.select(ensemble, roles=roles)
        if not any(selection.values()):
            return

        try:
            model = dialogue.cast(selection).run()
        except (AttributeError, ValueError) as e:
            log = logging.getLogger("turberfield.dialogue.player.run_through")
            log.warning(". ".join(getattr(e, "args", e) or e))
            return
        else:
            yield from model

def rehearse(folder, references, handler, repeat=0, roles=1, loop=None):
    """Cast a set of objects into a sequence of scene scripts. Deliver the performance.

    :param folder: A :py:class:`turberfield.dialogue.model.SceneScript.Folder`.
    :param references: A sequence of Python objects.
    :param handler: A callable object. This will be invoked with every event from the
                    performance.

    This function is a generator. It yields events from the performance.

    """

    yield from handler(references, loop=loop)

    while True:
        scripts = list(SceneScript.scripts(**folder._asdict()))

        for index, script, interlude in zip(itertools.count(), scripts, folder.interludes):
            yield from handler(script, loop=loop)
            seq = list(run_through(script, references, roles=roles))
            for shot, item in seq:
                yield from handler(shot, loop=loop)
                yield from handler(item, loop=loop)

            if seq:
                branch = next(handler(interlude, folder, index, references, loop=loop))
                if branch is None:
                    return
                elif branch != folder:
                    break
        else:
            if not repeat:
                break
            else:
                repeat -= 1

        folder = branch
