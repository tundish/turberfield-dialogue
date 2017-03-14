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


from collections import namedtuple
import importlib

import docutils.nodes
from docutils.nodes import BackLinkable, Element, General, Inline
from docutils.nodes import Labeled, Targetable, TextElement
import docutils.parsers.rst


class Pathfinder:

    @staticmethod
    def string_import(arg, relative=False):
        bits = arg.split(".")
        index = min(n for n, i in enumerate(bits) if i and i[0].isupper())
        start = 1 if relative else 0
        modName = ".".join(bits[start:index])
        try:
            mod = importlib.import_module(modName)
        except ImportError:
            return None

        obj = mod
        for name in bits[index:]:
            obj = getattr(obj, name)

        return obj

    @staticmethod
    def string_split(arg):
        return arg.split()


class Entity(docutils.parsers.rst.Directive):

    # See http://docutils.sourceforge.net/docutils/parsers/rst/directives/parts.py

    class Declaration(Pathfinder, General, BackLinkable, Element, Labeled, Targetable):
        pass

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "states": Declaration.string_split,
        "types": Declaration.string_split,
    }
    has_content = True
    node_class = Declaration


    def run(self):
        kwargs = {
            i: getattr(self, i, None)
            for i in (
                "name", "arguments", "options", "content", "lineno", "content_offset",
                "block_text", "state", "state_machine"
            )
        }
        node = self.node_class(**kwargs)
        name = docutils.nodes.fully_normalize_name(self.arguments[0])
        node["names"] = list(set(node["names"]) | {name})
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]

class Property(docutils.parsers.rst.Directive):

    class Getter(Inline, TextElement, Pathfinder):
        pass

    class Setter(Element, Inline, Pathfinder):
        pass

    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {}
    has_content = False

    def run(self):
        kwargs = {
            i: getattr(self, i, None)
            for i in (
                "name", "arguments", "options", "content", "lineno", "content_offset",
                "block_text", "state", "state_machine"
            )
        }
        if len(self.arguments) == 1:
            node = Property.Getter(**kwargs)
        else:
            node = Property.Setter(**kwargs)
        return [node]

class FX(docutils.parsers.rst.Directive):

    class Cue(Element, Inline, Pathfinder):
        pass

    required_arguments = 2
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "offset": int,
        "duration": int,
        "loop": int,
    }
    has_content = False

    def run(self):
        kwargs = {
            i: getattr(self, i, None)
            for i in (
                "name", "arguments", "options", "content", "lineno", "content_offset",
                "block_text", "state", "state_machine"
            )
        }
        node = FX.Cue(**kwargs)
        return [node]

class Memory(docutils.parsers.rst.Directive):

    class Definition(Inline, TextElement, Pathfinder):
        pass

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {"subject": str, "object": str}
    has_content = True

    def run(self):
        kwargs = {
            i: getattr(self, i, None)
            for i in (
                "name", "arguments", "options", "content", "lineno", "content_offset",
                "block_text", "state", "state_machine"
            )
        }
        node = Memory.Definition(**kwargs)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]
