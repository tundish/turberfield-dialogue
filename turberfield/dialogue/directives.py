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

from docutils.nodes import BackLinkable, Element, General, Labeled, Targetable
import docutils.parsers.rst
from docutils.parsers.rst.directives.body import ParsedLiteral


class Character(docutils.parsers.rst.Directive):

    """
    http://docutils.sourceforge.net/docutils/parsers/rst/directives/parts.py
    """

    class Definition(General, BackLinkable, Element, Labeled, Targetable):

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
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class RoleDirective(docutils.parsers.rst.Directive):

    """
    http://docutils.sourceforge.net/docutils/parsers/rst/directives/parts.py
    """

    Node = namedtuple("Node", ["name", "note", "relationships"])
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}
    has_content = True

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        # Create the admonition node, to be populated by `nested_parse`.
        text = '\n'.join(self.content)
        text_nodes, messages = self.state.inline_text(text, self.lineno)
        node = docutils.nodes.literal_block(text, '', *text_nodes, **self.options)
        node.line = self.content_offset + 1
        self.add_name(node)
        return [node] + messages
        kwargs = {
            i: getattr(self, i, None)
            for i in (
                "name", "arguments", "options", "content", "lineno", "content_offset",
                "block_text", "state", "state_machine"
            )
        }
        dialogueNode = self.node_class(**kwargs)
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, dialogueNode)
        return [dialogueNode]


