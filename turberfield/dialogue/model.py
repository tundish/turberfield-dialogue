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
from collections import namedtuple
from collections import OrderedDict
import itertools
import logging
import os.path
import sys

from turberfield.dialogue.directives import Character
from turberfield.dialogue.directives import Property
from turberfield.utils.misc import group_by_type

import pkg_resources
import docutils


class SceneScript:
    """
    Holds metadata for a scene file (.rst).

    A SceneScript contains one or more scenes. Each scene consists of one or more shots.

    """

    Folder = namedtuple("Folder", ["pkg", "doc", "paths"])

    log = logging.getLogger("turberfield.dialogue.scenescript")

    settings=argparse.Namespace(
        debug = False, error_encoding="utf-8",
        error_encoding_error_handler="backslashreplace", halt_level=4,
        auto_id_prefix="", id_prefix="", language_code="en",
        pep_references=1,
        report_level=2, rfc_references=1, tab_width=4,
        warning_stream=sys.stderr
    )

    docutils.parsers.rst.directives.register_directive(
        "character", Character
    )

    docutils.parsers.rst.directives.register_directive(
        "property", Property
    )

    @classmethod
    def scripts(cls, pkg, doc, paths=[]):
        for path in paths:
            try:
                fP = pkg_resources.resource_filename(pkg, path)
            except ImportError:
                cls.log.warning(
                    "No package called {}".format(pkg)
                )
            else:
                if not os.path.isfile(fP):
                    cls.log.warning(
                        "No script file at {}".format(os.path.join(*pkg.split(".") + [path]))
                    )
                else:
                    yield cls(fP, doc)


    @staticmethod
    def read(text, name=None):
        doc = docutils.utils.new_document(name, SceneScript.settings)
        parser = docutils.parsers.rst.Parser()
        parser.parse(text, doc)
        return doc

    def __init__(self, fP, doc=None):
        self.fP = fP
        self.doc = doc

    def __enter__(self):
        with open(self.fP, "r") as script:
            self.doc = self.read(script.read())
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def select(self, personae, relative=False):

        def constrained(character):
            return len(character["options"])

        rv = OrderedDict()
        pool = list(personae)
        characters = sorted(group_by_type(self.doc)[Character.Definition], key=constrained, reverse=True)
        for c in characters:
            types = filter(None, (c.string_import(t, relative) for t in c["options"].get("types", [])))
            spec = tuple(types) or (object, )
            persona = next((i for i in pool if isinstance(i, spec)), None)
            pool.remove(persona)
            rv[persona] = c
        return rv

    def cast(self, mapping):
        # See 'citation' method in
        # http://docutils.sourceforge.net/docutils/parsers/rst/states.py
        for p, c in mapping.items():
            self.doc.note_citation(c)
            self.doc.note_explicit_target(c, c)
            c.persona = p
            self.log.debug("{0} cast as {1}".format(p, c["names"][0]))
        return self

