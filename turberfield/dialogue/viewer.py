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
import logging
import logging.handlers
import shutil
import sys
import textwrap
import time
import uuid
import wave

import simpleaudio
import turberfield.dialogue.cli
from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.sequences.battle_royal.types import Animal
from turberfield.dialogue.sequences.battle_royal.types import Availability
from turberfield.dialogue.sequences.battle_royal.types import Tool
from turberfield.utils.misc import gather_installed
from turberfield.utils.misc import log_setup

__doc__ = """
WAV file player.

"""

def cast_menu(log):
    print("Cast menu\n=========\n\n")
    castList = OrderedDict(gather_installed("turberfield.interfaces.cast", log=log))
    print(*["\t{0}: {1} ({2} members)".format(n, k, len(v)) for n, (k, v) in enumerate(castList.items())], sep="\n")
    index = int(input("\nChoose a cast: "))
    choice = list(castList.keys())[index]
    log.info("Selected cast '{0}'.".format(choice))
    return castList[choice]

def clear_screen():
    n = shutil.get_terminal_size().lines
    print("\n" * n, end="")
    return n

def main(args):
    loop = asyncio.get_event_loop()
    logName = log_setup(args, loop=loop)
    log = logging.getLogger(logName)

    cast = cast_menu(log)

    try:
        cast = {
            Animal(uuid.uuid4(), None, ("Itchy",)),
            Animal(uuid.uuid4(), None, ("Scratchy",)),
            Tool(uuid.uuid4(), ("Rusty", "Chopper",)),
        }
        while True:
            personae = {
                i for i in cast
                if Availability.passive not in i.state.values()
            }
            folder = SceneScript.Folder(
                "turberfield.dialogue.sequences.battle_royal", "demo", ["combat.rst"]
            )
            scriptFile = next(SceneScript.scripts(**folder._asdict()))
            with scriptFile as script:
                model = script.cast(script.select(personae, roles=1)).run()
                for n, (shot, item) in enumerate(model):
                    if hasattr(item, "text"):
                        print("\n")
                        print(item.persona.name)
                        print(textwrap.indent(item.text, " " * 16))
                        time.sleep(2)

            time.sleep(4)
    except (AttributeError, ValueError) as e:
        # log.error(getattr(e, "args", e) or e)
        # No casting match
        log.info("No valid casting selection.")
    finally:
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
