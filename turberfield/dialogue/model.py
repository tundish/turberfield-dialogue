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

from turberfield.dialogue.directives import Entity as EntityDirective
from turberfield.dialogue.directives import Property as PropertyDirective
from turberfield.dialogue.directives import Memory as MemoryDirective
from turberfield.utils.misc import group_by_type

import pkg_resources
import docutils


class Model(docutils.nodes.GenericNodeVisitor):

    Shot = namedtuple("Shot", ["name", "scene", "items"])
    Property = namedtuple("Property", ["entity", "object", "attr", "val"])
    Memory = namedtuple("Memory", ["subject", "object", "state", "text", "html"])
    Line = namedtuple("Line", ["persona", "text", "html"])

    def __init__(self, fP, document):
        super().__init__(document)
        self.fP = fP
        self.optional = tuple(
            i.__name__ for i in (
                EntityDirective.Declaration, MemoryDirective.Definition,
                PropertyDirective.Getter, PropertyDirective.Setter
            )
        )
        self.log = logging.getLogger("turberfield.dialogue.{0}".format(os.path.basename(self.fP)))
        self.section_level = 0
        self.scenes = []
        self.shots = []
        self.speaker = None
        self.memory = None

    def __iter__(self):
        for shot in self.shots:
            for item in shot.items:
                yield shot, item

    def get_entity(self, ref):
        return next((
            entity
            for entity in self.document.citations
            if ref.lower() in entity.attributes["names"]),
            None)

    def default_visit(self, node):
        self.log.debug(node)

    def default_departure(self, node):
        self.log.debug("Departed.")

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    def visit_Setter(self, node):
        ref, attr = node["arguments"][0].split(".")
        entity = self.get_entity(ref)
        val = node.string_import(node["arguments"][1])
        self.shots[-1].items.append(Model.Property(self.speaker, entity.persona, attr, val))

    def visit_Definition(self, node):
        state = node.string_import(node["arguments"][0])
        subj = self.get_entity(node["options"].get("subject"))
        obj = self.get_entity(node["options"].get("object"))
        self.memory = Model.Memory(subj.persona, obj.persona, state, None, None)

    def visit_title(self, node):
        self.log.debug(self.section_level)
        if isinstance(node.parent, docutils.nodes.section):
            if self.section_level == 1:
                self.scenes.append(node.parent.attributes["names"][0])
            elif self.section_level == 2:
                self.shots.append(Model.Shot(
                    node.parent.attributes["names"][0],
                    self.scenes[-1],
                    []))

    def visit_paragraph(self, node):
        text = []
        html = []
        for c in node.children:
            if isinstance(c, docutils.nodes.substitution_reference):
                try:
                    defn = self.document.substitution_defs[c.attributes["refname"]]
                except KeyError:
                    self.log.warning("Bad substitution ref before line {0}: {1.rawsource}".format(node.line, c))
                    raise
                for tgt in defn.children:
                    if isinstance(tgt, PropertyDirective.Getter):
                        ref, dot, attr = tgt["arguments"][0].partition(".")
                        entity = self.get_entity(ref)
                        val = operator.attrgetter(attr)(entity.persona)
                        text.append(val)
                        html.append('<span class="ref">{0}</span>'.format(val))
            elif isinstance(c, docutils.nodes.strong):
                text.append(c.rawsource)
                html.append('<strong class="text">{0}</strong>'.format(c.rawsource.replace("*", "")))
            elif isinstance(c, docutils.nodes.Text):
                text.append(c.rawsource)
                html.append('<span class="text">{0}</span>'.format(c.rawsource))

        if self.memory:
            self.shots[-1].items.append(self.memory._replace(text=" ".join(text), html="\n".join(html)))
            self.memory = None
        elif (text or html) and self.section_level == 2:
            self.shots[-1].items.append(Model.Line(self.speaker, " ".join(text), "\n".join(html)))

    def visit_citation_reference(self, node):
        entity = self.get_entity(node.attributes["refname"])
        self.speaker = entity.persona

class SceneScript:
    """
    Holds metadata for a scene file (.rst).

    A SceneScript contains one or more scenes. Each scene consists of one or more shots.

    """

    Folder = namedtuple("Folder", ["pkg", "doc", "paths", "interludes"])

    log = logging.getLogger("turberfield.dialogue.scenescript")

    settings=argparse.Namespace(
        character_level_inline_markup=False,
        debug = False, error_encoding="utf-8",
        error_encoding_error_handler="backslashreplace", halt_level=4,
        auto_id_prefix="", id_prefix="", language_code="en",
        pep_references=1,
        report_level=2, rfc_references=1,
        strict_visitor=False, tab_width=4,
        warning_stream=sys.stderr
    )

    docutils.parsers.rst.directives.register_directive(
        "entity", EntityDirective
    )

    docutils.parsers.rst.directives.register_directive(
        "property", PropertyDirective
    )

    docutils.parsers.rst.directives.register_directive(
        "memory", MemoryDirective
    )

    @classmethod
    def scripts(cls, pkg, doc, paths=[], **kwargs):
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

        def constrained(entity):
            return len(entity["options"])

        rv = OrderedDict()
        pool = list(personae)
        self.log.debug(pool)
        entities = sorted(group_by_type(self.doc)[EntityDirective.Declaration], key=constrained, reverse=True)
        for e in entities:
            types = filter(None, (e.string_import(t, relative) for t in e["options"].get("types", [])))
            spec = tuple(types) or (object, )
            persona = next((i for i in pool if isinstance(i, spec)), None)
            rv[e] = persona
            if list(rv.values()).count(persona) == roles:
                try:
                    pool.remove(persona)
                except ValueError:
                    self.log.info("No persona matches spec {0}".format(spec))
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
        self.doc.walkabout(model)
        return model

