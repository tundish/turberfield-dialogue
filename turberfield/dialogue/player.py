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

def run_through(script, ensemble, log, roles=1):
    then = datetime.datetime.now()
    with script as dialogue:
        try:
            model = dialogue.cast(
                dialogue.select(ensemble, roles=roles)
            ).run()
        except (AttributeError, ValueError) as e:
            log.error(". ".join(getattr(e, "args", e) or e))
            return
        else:
            yield from model

def rehearse(
    sequence, ensemble, handler, repeat=0, roles=1,
    log=None, loop=None
):
    log = log or logging.getLogger("turberfield.dialogue.player.rehearse")
    folder = Pathfinder.string_import(
        sequence, relative=False, sep=":"
    )
    personae = Pathfinder.string_import(
        ensemble, relative=False, sep=":"
    )
    log.debug(folder)
    log.debug(personae)

    if hasattr(handler, "con"):
        with handler.con as db:
            log.debug(handler.con)
            rv = SchemaBase.populate(db, personae)
            log.info("Populated {0} rows.".format(rv))

    while True:
        scripts = list(SceneScript.scripts(**folder._asdict()))

        for script, interlude in zip(scripts, folder.interludes):
            yield from handler(script, loop=loop)
            log.debug(script)
            seq = list(run_through(script, personae, log, roles=roles))
            for shot, item in seq:
                yield from handler(shot, loop=loop)
                yield from handler(item, loop=loop)

            if seq:
                branch = next(handler(interlude, folder, personae, loop=loop))
                if branch != folder:
                    break
        else:
            if not repeat:
                break
            else:
                repeat -= 1

        folder = branch
