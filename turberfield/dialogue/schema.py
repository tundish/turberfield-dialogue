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

from collections import OrderedDict
import enum

from turberfield.utils.db import SQLOperation
from turberfield.utils.db import Table
from turberfield.utils.misc import gather_installed


class SchemaBase:

    tables = OrderedDict(
        (table.name, table) for table in [
        Table(
            "entity",
            cols=[
              Table.Column("id", int, True, False, False, None, None),
              Table.Column("session", str, False, False, True, None, None),
              Table.Column("name", str, False, False, True, None, None),
            ]
        ),
        Table(
            "state",
            cols=[
              Table.Column("id", int, True, False, False, None, None),
              Table.Column("class", str, False, False, True, None, None),
              Table.Column("name", str, False, False, True, None, None),
              Table.Column("value", int, False, False, False, None, None),
            ]
        ),
        Table(
            "touch",
            cols=[
              Table.Column("sbjct", int, False, False, False, None, "entity"),
              Table.Column("objct", int, False, True, False, None, "entity"),
            ]
        )
    ])

    @classmethod
    def populate(cls, db, *args):
        states = [i for i in args if isinstance(i, enum.Enum)]
        entities = [i for i in args if i not in states]
        for state in states:
            pass
        for entity in entities:
            pass
        return 0

    @classmethod
    def reference(cls, db, *kwargs):
        pass


class Selection(SQLOperation):

    @property
    def sql(self):
        lines = []
        for table in self.tables:
            lines.append(
                "select {columns} from {table.name}".format(
                    table=table,
                    columns=", ".join(i.name for i in table.cols),
                )
            )
        return (";\n".join(lines), {})

    def run(self, con, log=None):
        cur = super().run(con)
        return cur.fetchall()
