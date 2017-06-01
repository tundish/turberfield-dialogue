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

import asyncio
from collections.abc import Callable
from collections.abc import MutableSequence
import logging
import sys
import textwrap
import time
import wave

import pkg_resources
import simpleaudio

from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.schema import SchemaBase
from turberfield.utils.assembly import Assembly
from turberfield.utils.db import Connection
from turberfield.utils.db import Creation


class TerminalHandler:

    @staticmethod
    def handle_audio(obj, wait=False):
        fp = pkg_resources.resource_filename(obj.package, obj.resource)
        data = wave.open(fp, "rb")
        nChannels = data.getnchannels()
        bytesPerSample = data.getsampwidth()
        sampleRate = data.getframerate()
        nFrames = data.getnframes()
        framesPerMilliSecond = nChannels * sampleRate // 1000

        offset = framesPerMilliSecond * obj.offset
        duration = nFrames - offset
        duration = min(
            duration,
            framesPerMilliSecond * obj.duration if obj.duration is not None else duration
        )

        data.readframes(offset)
        frames = data.readframes(duration)
        for i in range(obj.loop):
            waveObj = simpleaudio.WaveObject(frames, nChannels, bytesPerSample, sampleRate)
            playObj = waveObj.play()
            if obj.loop > 1 or wait:
                playObj.wait_done()
        return obj

    def handle_interlude(self, obj, folder, index, ensemble, loop=None, **kwargs):
        if obj is None:
            return folder
        else:
            return obj(folder, index, ensemble, loop=loop, **kwargs)

    def handle_line(self, obj):
        if obj.persona is None:
            return obj

        name = getattr(obj.persona, "_name", "")
        print(
            textwrap.indent(
                "{t.normal}{name}".format(name=name, t=self.terminal),
                " " * 2
            ),
            end="\n",
            file=self.terminal.stream
        )
        print(
            textwrap.indent(
                "{t.normal}{obj.text}".format(
                    obj=obj, t=self.terminal
                ),
                " " * 10
            ),
            end="\n" * 2,
            file=self.terminal.stream
        )
        interval = self.pause + self.dwell * obj.text.count(" ")
        time.sleep(interval)
        return obj

    def handle_memory(self, obj):
        with self.con as db:
            rv = SchemaBase.note(
                db,
                obj.subject,
                obj.state,
                obj.object,
                text=obj.text,
                html=obj.html,
            )
        return obj

    def handle_property(self, obj):
        try:
            setattr(obj.object, obj.attr, obj.val)
        except AttributeError as e:
            self.log.error(". ".join(getattr(e, "args", e) or e))
        print(
            "{t.dim}{obj.object._name}.{obj.attr} = {obj.val!s}{t.normal}".format(
                obj=obj, t=self.terminal
            ),
            end="\n" * 2,
            file=self.terminal.stream
        )
        return obj

    def handle_scene(self, obj):
        print(
            "{t.dim}{scene}{t.normal}".format(
                scene=obj.scene.capitalize(), t=self.terminal
            ),
            end="\n" * 3,
            file=self.terminal.stream
        )
        time.sleep(self.pause)
        return obj

    def handle_scenescript(self, obj):
        self.log.debug(obj.fP)
        return obj

    def handle_shot(self, obj):
        print(
            "{t.dim}{shot}{t.normal}".format(
                shot=obj.name.capitalize(), t=self.terminal
            ),
            end="\n" * 3,
            file=self.terminal.stream
        )
        return obj

    def handle_creation(self):
        with self.con as db:
            rv = Creation(
                *SchemaBase.tables.values()
            ).run(db)
            db.commit()
            self.log.info("Created {0} tables in {1}.".format(len(rv), self.dbPath))
            return rv

    def handle_references(self, obj):
        with self.con as db:
            rv = SchemaBase.populate(db, obj)
            self.log.info("Populated {0} rows.".format(rv))
            return rv

    def __init__(
        self, terminal, dbPath=None,
        pause=1.5, dwell=0.2, log=None
    ):
        self.terminal = terminal
        self.dbPath = dbPath
        self.pause = pause
        self.dwell = dwell
        self.log = log or logging.getLogger("turberfield.dialogue.handle")
        self.shot = None
        self.con = Connection(**Connection.options(paths=[dbPath] if dbPath else []))
        self.handle_creation()

    def __call__(self, obj, *args, loop, **kwargs):
        if isinstance(obj, Model.Line):
            try:
                yield self.handle_line(obj)
            except AttributeError:
                pass
        elif isinstance(obj, Model.Audio):
            yield self.handle_audio(obj)
        elif isinstance(obj, Model.Memory):
            yield self.handle_memory(obj)
        elif isinstance(obj, Model.Property):
            yield self.handle_property(obj)
        elif isinstance(obj, Model.Shot):
            if self.shot is None or obj.scene != self.shot.scene:
                yield self.handle_scene(obj)
            if self.shot is None or obj.name != self.shot.name:
                yield self.handle_shot(obj)
            else:
                yield obj
            self.shot = obj
        elif isinstance(obj, SceneScript):
            yield self.handle_scenescript(obj)
        elif asyncio.iscoroutinefunction(obj):
            raise NotImplementedError
        elif isinstance(obj, MutableSequence):
            yield self.handle_references(obj)
        elif (obj is None or isinstance(obj, Callable)) and len(args) == 3:
            yield self.handle_interlude(obj, *args, loop=loop, **kwargs)
        else:
            yield obj

class CGIHandler(TerminalHandler):

    def handle_audio(self, obj):
        path = pkg_resources.resource_filename(obj.package, obj.resource)
        pos = path.find("lib", len(sys.prefix))
        if pos != -1:
            print(
                "event: audio",
                "data: ../{0}\n".format(path[pos:]),
                sep="\n",
                end="\n",
                file=self.terminal.stream
            )
            self.terminal.stream.flush()
        return obj

    def handle_line(self, obj):
        print(
            "event: line",
            "data: {0}\n".format(Assembly.dumps(obj)),
            sep="\n",
            end="\n",
            file=self.terminal.stream
        )
        self.terminal.stream.flush()
        interval = self.pause + self.dwell * obj.text.count(" ")
        time.sleep(interval)
        return obj

    def handle_property(self, obj):
        try:
            setattr(obj.object, obj.attr, obj.val)
        except AttributeError as e:
            self.log.error(". ".join(getattr(e, "args", e) or e))

    def handle_scene(self, obj):
        time.sleep(self.pause)
        return obj

    def handle_scenescript(self, obj):
        return obj

    def handle_shot(self, obj):
        return obj
