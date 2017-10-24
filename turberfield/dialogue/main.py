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
import textwrap
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
Script formatter.

Example:

~/py3.5/bin/python -m turberfield.dialogue.main @turberfield/dialogue/sequences/battle/rehearse.cli

"""

class HTMLHandler:

    template = textwrap.dedent("""
        <!doctype html>
        <html lang="en">
        <head>
        <meta charset="utf-8" />
        <title>Rehearsal</title>
        <style>
        #line {{
            font-family: "monospace";
        }}
        #line .persona::after {{
            content: ": ";
        }}
        #event {{
            font-style: italic;
        }}
        </style>
        </head>
        <body>
        <h1></h1>
        </body>
        </html>
    """).format().lstrip()

    def __call__(self, item):
        yield item

    def write(self, **kwargs):
        pass

def main(args):
    log = logging.getLogger(log_setup(args))
    folders, references = resolve_objects(args)
    performer = Performer(folders, references)
    handler = HTMLHandler()
    for i in range(args.repeat + 1):
        for item in performer.run(strict=args.strict, roles=args.roles):
            for obj in handler(item):
                print(obj)
    print(performer.metadata)
    handler.write(metadata=performer.metadata)


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
