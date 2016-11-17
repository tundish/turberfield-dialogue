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


import argparse
import asyncio
from collections import OrderedDict
import datetime
import logging
import logging.handlers
import shutil
import sys
import textwrap
import time
import uuid
import wave

import turberfield.dialogue.cli
from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.types import Player
from turberfield.utils.misc import gather_installed
from turberfield.utils.misc import log_setup

__doc__ = """
WAV file player.

"""

def ensemble_menu(log):
    log.info("Painting ensemble menu...")
    castList = OrderedDict(gather_installed("turberfield.interfaces.ensemble", log=log))
    print("\n")
    print(
        *["\t{0}: {1} ({2} members)".format(n, k, len(v)) for n, (k, v) in enumerate(castList.items())],
        sep="\n")
    index = int(input("\nChoose an ensemble: "))
    choice = list(castList.keys())[index]
    log.info("Selected ensemble '{0}'.".format(choice))
    return castList[choice]

def seq_menu(log):
    log.info("Painting sequence menu...")
    seqList = OrderedDict(gather_installed("turberfield.interfaces.sequence", log=log))
    print("\n")
    print(
        *["\t{0}: {1} ({2} members)".format(n, k, len(v.paths)) for n, (k, v) in enumerate(seqList.items())],
        sep="\n")
    index = int(input("\nChoose a sequence: "))
    choice = list(seqList.keys())[index]
    log.info("Selected sequence '{0}'.".format(choice))
    return seqList[choice]

def clear_screen():
    n = shutil.get_terminal_size().lines
    print("\n" * n, end="")
    return n

async def view(queue, log=None, loop=None):
    log = log or logging.getLogger("turberfield.dialogue.view")
    loop = loop or ayncio.get_event_loop()
    prev = None
    while True:
        try:
            shot, item = await queue.get()
        except TypeError as e:
            log.debug("Got sentinel.")
            queue.task_done()
            prev = None
            return

        if prev and shot is not prev:
            log.info("Pause...")
            time.sleep(2)
            clear_screen()

        if isinstance(item, Model.Line):
            print("\n")
            print(item.persona.name.firstname, item.persona.name.surname, sep=" ")
            print(textwrap.indent(item.text, " " * 16))
            time.sleep(1.5 + 0.2 * item.text.count(" "))

        prev = shot
        queue.task_done()

async def run_through(folder, ensemble, queue, log=None, loop=None):
    log = log or logging.getLogger("turberfield.dialogue.run_through")
    loop = loop or ayncio.get_event_loop()
    scripts = SceneScript.scripts(**folder._asdict())
    for script, interlude in zip(scripts, folder.interludes):
        then = datetime.datetime.now()
        with script as dialogue:
            try:
                model = dialogue.cast(dialogue.select(ensemble, roles=1)).run()
            except (AttributeError, ValueError) as e:
                log.error(". ".join(getattr(e, "args", e) or e))
                return

            for n, (shot, item) in enumerate(model):
                await queue.put((shot, item))
                await queue.join()

                if isinstance(item, Model.Property):
                    log.info("Assigning {val} to {object}.{attr}".format(**item._asdict()))
                    setattr(item.object, item.attr, item.val)
                elif isinstance(item, Model.Memory):
                    log.info("{subject} {state} {object}; {text}".format(**item._asdict()))
                    pass

        log.info("Time: {0}".format(datetime.datetime.now() - then))
        rv = await interlude(folder, ensemble, log=log, loop=loop)
        if rv is not folder:
            log.info("Interlude branching to {0}".format(rv))
            return rv

    await queue.put(None)
    return None

def main(args):
    loop = asyncio.get_event_loop()
    logName = log_setup(args, loop=loop)
    log = logging.getLogger(logName)

    folder = seq_menu(log)
    cast = ensemble_menu(log)
    player = Player(name="Mr Tim Finch")
    ensemble = { player } | cast
    queue = asyncio.Queue(maxsize=1, loop=loop)
    projectionist = loop.create_task(view(queue, loop=loop))
    start = datetime.datetime.now()

    try:
        while folder:
            folder = loop.run_until_complete(run_through(folder, ensemble, queue, loop=loop))
        else:
            log.info("Playing time: {0}".format(datetime.datetime.now() - start))
    finally:
        queue.put_nowait(None)
        projectionist.cancel()
        loop.close()

    return 0

def run():
    p = turberfield.dialogue.cli.parser()
    args = p.parse_args()
    if args.version:
        sys.stdout.write(turberfield.dialogue.__version__ + "\n")
        rv = 0
    else:
        rv = main(args)
    sys.exit(rv)


if __name__ == "__main__":
    run()
