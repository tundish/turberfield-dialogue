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
from collections import defaultdict
import itertools
import sys

from turberfield.dialogue.directives import RoleDirective

import docutils


class SceneScript:
    """
    Holds metadata for a scene file (.rst).

    A SceneScript contains one or more scenes. Each scene consists of one or more shots.

    """

    settings=argparse.Namespace(
        debug = False, error_encoding="utf-8",
        error_encoding_error_handler="backslashreplace", halt_level=4,
        auto_id_prefix="", id_prefix="", language_code="en",
        pep_references=1,
        report_level=2, rfc_references=1, tab_width=4,
        warning_stream=sys.stderr
    )

    def __init__(self):
        # TODO: Take metadata from entry point
        docutils.parsers.rst.directives.register_directive(
            "part", RoleDirective
        )

    def read(self, text, name=None):
        doc = docutils.utils.new_document(name, SceneScript.settings)
        parser = docutils.parsers.rst.Parser()
        parser.parse(text, doc)
        return doc.children
