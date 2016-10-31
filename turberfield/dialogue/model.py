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
import operator
import os.path
import sys

from turberfield.dialogue.directives import Character
from turberfield.dialogue.directives import Property
from turberfield.utils.misc import group_by_type

import pkg_resources
import docutils


class Model(docutils.nodes.GenericNodeVisitor):

    Shot = namedtuple("Shot", ["name", "scene", "items"])
    Act = namedtuple("Act", ["persona", "object", "attr", "val"])
    Line = namedtuple("Line", ["persona", "text", "html"])

    def __init__(self, fP, document):
        super().__init__(document)
        self.fP = fP
        self.optional = tuple(i.__name__ for i in (Character.Definition, Property.Getter))
        self.log = logging.getLogger("turberfield.dialogue.{0}".format(os.path.basename(self.fP)))
        self.section_level = 0
        self.scenes = []
        self.shots = []
        self.speaker = None

    def __iter__(self):
        for shot in self.shots:
            for item in shot.items:
                if isinstance(item, Model.Act):
                    self.log.info("Setting {object}.{attr} to {val}".format(**item._asdict()))
                    setattr(item.object, item.attr, item.val)
                yield shot, item

    def default_visit(self, node):
        self.log.debug(node)

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    def visit_Setter(self, node):
        ref, attr = node["arguments"][0].split(".")
        character = next(
            character
            for character in self.document.citations
            if ref.lower() in character.attributes["names"])
        val = node.string_import(node["arguments"][1])
        self.shots[-1].items.append(Model.Act(self.speaker, character.persona, attr, val))

    def visit_title(self, node):
        if isinstance(node.parent, docutils.nodes.section):
            if self.section_level == 1:
                self.scenes.append(node.parent.attributes["names"][0])
            elif self.section_level == 2:
                self.shots.append(Model.Shot(
                    node.parent.attributes["names"][0],
                    self.scenes[-1],
                    []))

    def visit_paragraph(self, node):
        if self.section_level != 2:
            return
        text = []
        html = []
        for c in node.children:
            if isinstance(c, docutils.nodes.substitution_reference):
                defn = self.document.substitution_defs[c.attributes["refname"]]
                for tgt in defn.children:
                    if isinstance(tgt, Property.Getter):
                        ref, dot, attr = tgt["arguments"][0].partition(".")
                        character = next(
                            character
                            for character in self.document.citations
                            if ref.lower() in character.attributes["names"])

                        val = operator.attrgetter(attr)(character.persona)
                        text.append(val)
                        html.append('<span class="ref">{0}</span>'.format(val))
            elif isinstance(c, docutils.nodes.strong):
                text.append(c.rawsource)
                html.append('<strong class="text">{0}</strong>'.format(c.rawsource.replace("*", "")))
            elif isinstance(c, docutils.nodes.Text):
                text.append(c.rawsource)
                html.append('<span class="text">{0}</span>'.format(c.rawsource))

        if (text or html) and self.section_level == 2:
            self.shots[-1].items.append(Model.Line(self.speaker, " ".join(text), "\n".join(html)))

    def visit_citation_reference(self, node):
        character = next(
            character
            for character in self.document.citations
            if node.attributes["refname"] in character.attributes["names"])
        self.speaker = character.persona

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
        report_level=2, rfc_references=1,
        strict_visitor=False, tab_width=4,
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

    def select(self, personae, relative=False, roles=1):

        def constrained(character):
            return len(character["options"])

        rv = OrderedDict()
        pool = list(personae)
        self.log.debug(pool)
        characters = sorted(group_by_type(self.doc)[Character.Definition], key=constrained, reverse=True)
        for c in characters:
            types = filter(None, (c.string_import(t, relative) for t in c["options"].get("types", [])))
            spec = tuple(types) or (object, )
            persona = next((i for i in pool if isinstance(i, spec)), None)
            rv[c] = persona
            if list(rv.values()).count(persona) == roles:
                pool.remove(persona)
        return rv

    def cast(self, mapping):
        # See 'citation' method in
        # http://docutils.sourceforge.net/docutils/parsers/rst/states.py
        for c, p in mapping.items():
            self.doc.note_citation(c)
            self.doc.note_explicit_target(c, c)
            c.persona = p
            self.log.debug("{0} to be played by {1}".format(
                c["names"][0].capitalize(), p)
            )
        return self

    def run(self):
        model = Model(self.fP, self.doc)
        self.doc.walk(model)
        return model

