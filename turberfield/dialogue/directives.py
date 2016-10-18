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
from docutils.nodes import BackLinkable, Element, General, Labeled, Targetable
import docutils.parsers.rst
from docutils.parsers.rst.directives.body import ParsedLiteral


class Character(docutils.parsers.rst.Directive):

    # See http://docutils.sourceforge.net/docutils/parsers/rst/directives/parts.py

    class Definition(General, BackLinkable, Element, Labeled, Targetable):

        @staticmethod
        def string_import(arg, namespace=True):
            bits = arg.split(".")
            index = max(n for n, i in enumerate(bits) if i[0].islower())
            start = 1 if namespace else 0
            modName = ".".join(bits[start:index + 1])
            mod = importlib.import_module(modName)
            obj = mod
            for name in bits[index + 1:]:
                obj = getattr(obj, name)
            
            return obj

        @staticmethod
        def string_split(arg):
            return arg.split()

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "states": Definition.string_split,
        "types": Definition.string_split,
    }
    has_content = True
    node_class = Definition


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
