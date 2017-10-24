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
from collections import OrderedDict
import datetime
import itertools
import logging
import logging.handlers
import math
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
    def format_dialogue(shots):
        pad = int(math.log10(sum(len(rows) for rows in shots.values()) + 1)) + 1
        return "\n".join(textwrap.dedent("""
            <table>
            <thead>
            <tr>
            <th>Character</th>
            <th>Dialogue</th>
            <th>Notes</th>
            </tr>
            </thead>

            <tbody>
            {body}
            </tbody>

            <tfoot>
            <tr>
            <td></td>
            <td></td>
            <td>{elapsed:.1f} sec</td>
            </tr>
            </tfoot>
            </table>
        """).format(
            elapsed=sum(i[-1] for i in rows if i is not None),
            body = "\n".join("<tr><td>{name}</td>\n<td>{text}</td>\n<td>{notes}</td>\n</tr>".format(
                name=" ".join(i.capitalize() for i in name.split()),
                text=text,
                notes="{0:02.2f} sec. {1:0{2}}".format(span, n + 1, pad)
            ) for n, (name, text, span) in enumerate(rows))
        ) for shot, rows in shots.items())


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
        self.shot = None
        self.shots = OrderedDict()

    def __call__(self, obj):
        if isinstance(obj, Model.Line):
            yield self.handle_line(obj)
        elif isinstance(obj, Model.Shot):
            shot = obj._replace(items=None)
            if shot != self.shot:
                self.shots[shot] = []
                self.shot = shot
            yield obj
        else:
            yield obj

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
        self.shots[self.shot].append((name, text, span))
        return obj

    def to_html(self, metadata, **kwargs):
        return textwrap.dedent("""
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
            dialogue=self.format_dialogue(self.shots)
        ).lstrip()

def main(args):
    log = logging.getLogger(log_setup(args))
    folders, references = resolve_objects(args)
    performer = Performer(folders, references)
    handler = HTMLHandler(dwell=args.dwell, pause=args.pause)
    for i in range(args.repeat + 1):
        for item in performer.run(strict=args.strict, roles=args.roles):
            list(handler(item))
    print(handler.shots, file=sys.stderr)
    print(handler.to_html(metadata=performer.metadata))


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
