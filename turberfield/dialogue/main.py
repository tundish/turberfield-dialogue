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
from turberfield.dialogue.handlers import TerminalHandler
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

~/py3.5/bin/python -m turberfield.dialogue.main \
 @turberfield/dialogue/sequences/battle/rehearse.cli | \
 ~/py3.5/bin/weasyprint -p - dialogue.pdf

"""

class HTMLHandler:


    @staticmethod
    def format_dialogue(rows):
        return """
            <table>
                  <thead>
                    <tr>
                      <th>Header content 1</th>
                      <th>Header content 2</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Body content 1</td>
                      <td>Body content 2</td>
                    </tr>
                  </tbody>
                  <tfoot>
                    <tr>
                      <td>Footer content 1</td>
                      <td>Footer content 2</td>
                    </tr>
                  </tfoot>
                </table>
        """

    @staticmethod
    def format_metadata(**kwargs):
        return "<dl>\n{0}\n</dl>".format(
            "\n".join(
                "<dt>{0}</dt>\n{1}\n".format(
                    key.capitalize(),
                    "\n".join(
                        "<dd>{0}</dd>".format(val)
                        for val in kwargs[key]
                    )
                ) 
                for key in kwargs
            )
        )

    def __init__(self, dwell, pause):
        self.dwell = dwell
        self.pause = pause
        self.speaker = None
        self.rows = []

    def __call__(self, obj):
        if isinstance(obj, Model.Line):
            yield self.handle_line(obj)
        elif isinstance(obj, SceneScript):
            yield self.handle_scenescript(obj)

    def handle_line(self, obj):
        if obj.persona is None:
            return 0

        # TODO: Fix this properly in turberfield-dialogue
        text = obj.text.replace("   ", " ").replace("  ", " ")
        if self.speaker is not obj.persona:
            self.speaker = obj.persona
            try:
                name = "{0.firstname} {0.surname}".format(self.speaker.name).strip()
            except AttributeError:
                name = None
        else:
            name = ""

        span = self.pause + self.dwell * text.count(" ")
        self.rows.append((name, text, span))

    def write(self, metadata, **kwargs):
        rv = textwrap.dedent("""
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
            {metadata}
            {dialogue}
            </body>
            </html>
        """).format(
            metadata=self.format_metadata(**metadata),
            dialogue=self.format_dialogue(self.rows)
        ).lstrip()
        print(rv)
        print(self.rows)

def main(args):
    log = logging.getLogger(log_setup(args))
    folders, references = resolve_objects(args)
    performer = Performer(folders, references)
    handler = HTMLHandler(dwell=args.dwell, pause=args.pause)
    for i in range(args.repeat + 1):
        for item in performer.run(strict=args.strict, roles=args.roles):
            list(handler(item))
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
