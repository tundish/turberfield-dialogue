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
import datetime
import itertools
import logging
import logging.handlers
import sys
import time

from turberfield.dialogue.cli import add_casting_options
from turberfield.dialogue.cli import add_common_options
from turberfield.dialogue.cli import add_performance_options
from turberfield.dialogue.cli import resolve_objects
from turberfield.dialogue.directives import Pathfinder
from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.performer import Performer
from turberfield.dialogue.types import Player
from turberfield.utils.misc import gather_installed
from turberfield.utils.misc import config_parser
from turberfield.utils.misc import log_setup

__doc__ = """
Script viewer.

Example:

python -m turberfield.dialogue.viewer \
--sequence=turberfield.dialogue.sequences.battle_royal:folder \
--ensemble=turberfield.dialogue.sequences.battle_royal.types:ensemble

"""

def handler(item):
    yield item

def main(args):
    log = logging.getLogger(log_setup(args))
    folders, references = resolve_objects(args)
    performer = Performer(folders, references)
    for i in range(args.repeat + 1):
        for item in performer.run(strict=args.strict, roles=args.roles):
            for obj in handler(item):
                print(obj)


def run():
    p = add_performance_options(
        add_casting_options(
            add_common_options(
                argparse.ArgumentParser(
                    __doc__,
                    fromfile_prefix_chars="@"
                )
            )
        )
    )
    args = p.parse_args()
    if args.version:
        sys.stderr.write(__version__ + "\n")
        rv = 0
    else:
        rv = main(args)
    sys.exit(0)

if __name__ == "__main__":
    run()
