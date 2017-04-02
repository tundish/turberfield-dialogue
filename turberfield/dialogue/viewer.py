#!/usr/bin/env python3
#   coding: UTF-8

import argparse
import cgi
import cgitb
import datetime
import http.server
import itertools
import logging
from logging.handlers import WatchedFileHandler
import os.path
import platform
import sys
import textwrap
import time
import urllib.parse
import uuid
import wave
import webbrowser

from blessings import Terminal
import pkg_resources
import simpleaudio

from turberfield.dialogue import __version__
from turberfield.dialogue.directives import Pathfinder
from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript
import turberfield.dialogue.schema
from turberfield.utils.assembly import Assembly
from turberfield.utils.db import Connection
from turberfield.utils.db import Creation
from turberfield.utils.db import Insertion
from turberfield.utils.misc import log_setup

DFLT_PORT = 8080
DFLT_DB = ":memory:"

__doc__ = """
A utility to run through a sequence of dialogue.

The rehearsal can be viewed in a terminal or by web browser.

Eg::

    turberfield-rehearse @turberfield/dialogue/demo.cli

"""


class TerminalHandler:

    @staticmethod
    def handle(obj):
        return obj

    @staticmethod
    def handle_audio(obj):
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
            playObj.wait_done()
        return obj

    def handle_line(self, obj):
        print(
            textwrap.indent(
                "{t.normal}{obj.persona._name}".format(
                    obj=obj, t=self.terminal
                ),
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
        print("MEMORY")
        return obj

    def handle_property(self, obj):
        setattr(obj.object, obj.attr, obj.val)
        print(
            "{t.dim}{obj.object._name}.{obj.attr} = {obj.val}{t.normal}".format(
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
        with self.terminal.location(0, self.terminal.height - 1):
            print(
                "{t.dim}{obj.fP}{t.normal}".format(
                    obj=obj, t=self.terminal
                ),
                file=self.terminal.stream
            )
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

    def __init__(self, terminal, pause=1.5, dwell=0.2):
        self.terminal = terminal
        self.pause = pause
        self.dwell = dwell
        self.shot = None

    def __call__(self, obj, *args, loop, **kwargs):
        if isinstance(obj, Model.Line):
            yield self.handle_line(obj)
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
        else:
            yield self.handle(obj)

def run_through(script, ensemble, log, roles=1):
    then = datetime.datetime.now()
    with script as dialogue:
        try:
            model = dialogue.cast(
                dialogue.select(ensemble, roles=roles)
            ).run()
        except (AttributeError, ValueError) as e:
            log.error(". ".join(getattr(e, "args", e) or e))
            return
        else:
            yield from model

def rehearsal(folder, ensemble, log=None):
    # TODO: This function drives terminal
    log = log or logging.getLogger("turberfield")
    scripts = SceneScript.scripts(**folder._asdict())
    for script, interlude in itertools.zip_longest(
        scripts, itertools.cycle(folder.interludes)
    ):
        prev = None
        seq = run_through(script, ensemble, log)
        for n, (shot, item) in enumerate(seq):
            if isinstance(item, Model.Property):
                log.info("Assigning {val} to {object}.{attr}".format(**item._asdict()))
                setattr(item.object, item.attr, item.val)
            elif isinstance(item, Model.Audio):
                log.info("Launch {resource} from {package}.".format(**item._asdict()))
            elif isinstance(item, Model.Memory):
                log.info("{subject} {state} {object}; {text}".format(**item._asdict()))
                pass

        log.info("Time: {0}".format(datetime.datetime.now() - then))
        if interlude is None:
            rv = folder
        else:
            pass
            #rv = await interlude(folder, ensemble, log=log, loop=loop)

        if rv is not folder:
            log.info("Interlude branching to {0}".format(rv))
            return rv

def rehearse(sequence, ensemble, handler, db=None, log=None, loop=None):
    log = log or logging.getLogger("turberfield")
    folder = Pathfinder.string_import(
        sequence, relative=False, sep=":"
    )
    personae = Pathfinder.string_import(
        ensemble, relative=False, sep=":"
    )
    scripts = SceneScript.scripts(**folder._asdict())

    con = Connection(**Connection.options(db))
    with con as db:
        for table in turberfield.dialogue.schema.tables.values():
            rv = Creation(table).run(db)

        for person in personae:
            rv = Insertion(
                turberfield.dialogue.schema.tables["entity"],
                data={
                    "session": "1",
                    "name": person._name
                }
            ).run(db)

        op = turberfield.dialogue.schema.Selection(
            turberfield.dialogue.schema.tables["entity"]
        )
        print(op.sql)
        rv = op.run(db)
        print(rv)

    for script, interlude in itertools.zip_longest(
        scripts, itertools.cycle(folder.interludes)
    ):
        yield from handler(script, loop=loop)
        seq = list(run_through(script, personae, log))
        for shot, item in seq:
            yield from handler(shot, loop=loop)
            yield from handler(item, loop=loop)

        yield from handler(interlude, loop=loop)

def cgi_consumer(args):
    params = vars(args)
    params["session"] = uuid.uuid4().hex
    opts = urllib.parse.urlencode(params)
    url = "http://localhost:{0}/{1}/turberfield-rehearse?{2}".format(
        args.port, args.locn, opts
    )
    rv = textwrap.dedent("""
        Content-type:text/html

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
        <body class="loading">
        <h1>...</h1>
        <blockquote id="line">
        <header class="persona"></header>
        <p class="data"></p>
        </blockquote>
        <span id="event"></span>
        <script>
            if (!!window.EventSource) {{
                var source = new EventSource("{url}");
            }} else {{
                alert("Your browser does not support Server-Sent Events.");
            }}

            source.addEventListener("audio", function(e) {{
                var fx = new Promise(function(resolve, reject) {{
                    var src = e.data;
                    var repeat = false;
                    var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    var track = audioCtx.createBufferSource();
                    var request = new XMLHttpRequest();

                    request.open("GET", src, true);
                    request.responseType = "arraybuffer";

                    request.onload = function() {{
                        var audioData = request.response;

                        audioCtx.decodeAudioData(audioData, function(buffer) {{
                            var myBuffer = buffer;
                            track.buffer = myBuffer;
                            track.connect(audioCtx.destination);
                            track.loop = repeat;
                            resolve(track);
                          }},

                          function(e){{reject(e)}});

                    }}
                    request.send();
                }});

                fx.then(function(result){{
                    result.start(0);
                }});

            }}, false);

            source.addEventListener("line", function(e) {{
                var event = document.getElementById("event");
                event.innerHTML = "";
                var obj = JSON.parse(e.data);
                var quote = document.getElementById("line");
                var speaker = quote.getElementsByClassName("persona")[0];
                var line = quote.getElementsByClassName("data")[0];

                speaker.innerHTML = obj.persona.name.firstname;
                speaker.innerHTML += " ";
                speaker.innerHTML += obj.persona.name.surname;
                line.innerHTML = obj.html;
                
            }}, false);

            source.addEventListener("memory", function(e) {{
                var obj = JSON.parse(e.data);
                var event = document.getElementById("event");
                event.innerHTML = obj.html;
            }}, false);

            source.addEventListener("property", function(e) {{
                var obj = JSON.parse(e.data);
                var event = document.getElementById("event");
                event.innerHTML = "<";
                event.innerHTML += obj.object._name;
                event.innerHTML += ">.";
                event.innerHTML += obj.attr;
                event.innerHTML += " = ";
                event.innerHTML += obj.val.name;
            }}, false);

            source.addEventListener("open", function(e) {{
                console.log("Connection was opened.");
            }}, false);

            source.addEventListener("error", function(e) {{
                console.log("Error: connection lost.");
            }}, false);

        </script>
        </body>
        </html>
    """).format(url=url).lstrip()
    return rv

def cgi_producer(args):
    print("Content-type:text/event-stream")
    print()
    for shot, item, pause in rehearse(args.sequence, args.ensemble):
        print("event: {0}".format(type(item).__name__.lower()), end="\n")
        time.sleep(pause)
        #TODO: dispatch handler
        if isinstance(item, Model.Audio):
            path = pkg_resources.resource_filename(item.package, item.resource)
            print("data: {0}\n".format(path[len(sys.prefix):]), end="\n")
        else:
            print("data: {0}\n".format(Assembly.dumps(item)), end="\n")
        sys.stdout.flush()
        yield item

def presenter(args):
    handler = TerminalHandler(Terminal())
    if args.log_level != logging.DEBUG:
        with handler.terminal.fullscreen():
            yield from rehearse(args.sequence, args.ensemble, handler)
            input("Press return.")
    else:
        yield from rehearse(args.sequence, args.ensemble, handler)

def main(args):
    log = logging.getLogger(log_setup(args))
    if args.web:
        os.chdir(sys.prefix)
        log.warning("Web mode: running scripts from directory {0}".format(os.getcwd()))
        params = {
            k: getattr(args, k)
            for k in (
                "log_level", "log_path", "port",
                "session", "locn", "ensemble", "sequence"
            )
        }
        opts = urllib.parse.urlencode(params)
        url = "http://localhost:{0}/{1}/turberfield-rehearse?{2}".format(
            args.port, args.locn, opts
        )
        webbrowser.open_new_tab(url)
        Handler = http.server.CGIHTTPRequestHandler
        Handler.cgi_directories = ["/{0}".format(args.locn)]
        httpd = http.server.HTTPServer(("", args.port), Handler)

        log.info("serving at port {0}".format(args.port))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            log.info("Shutdown.")
            return 0

    elif "SERVER_NAME" in os.environ:
        form = cgi.FieldStorage()
        params = {key: form[key].value if key in form else "" for key in vars(args).keys()}
        args = argparse.Namespace(**params)
        cgitb.enable()
        if not args.session:
            log.info("Consumer view.")
            print(cgi_consumer(args))
        else:
            log.info("Producer view.")
            list(cgi_producer(args))
    else:
        for line in presenter(args):
            log.debug(line)
    return 0

def parser(description=__doc__):
    rv =  argparse.ArgumentParser(
        description,
        fromfile_prefix_chars="@"
    )
    rv.add_argument(
        "--version", action="store_true", default=False,
        help="Print the current version number")
    rv.add_argument(
        "-v", "--verbose", required=False,
        action="store_const", dest="log_level",
        const=logging.DEBUG, default=logging.INFO,
        help="Increase the verbosity of output")
    rv.add_argument(
        "--log", default=None, dest="log_path",
        help="Set a file path for log output")
    rv.add_argument(
        "--ensemble", default="",
        help="Give an import path to a list of Personae."
    )
    rv.add_argument(
        "--sequence", default="",
        help="Give an import path to a SceneScript folder."
    )
    rv.add_argument(
        "--web", action="store_true", default=False,
        help="Activate the web interface")
    rv.add_argument(
        "--session", required=False, default="",
        help="Internal session path")
    rv.add_argument(
        "--locn", required=False,
        default="Scripts" if "windows" in platform.system().lower() else "bin",
        help="Internal script location")
    rv.add_argument(
        "--port", type=int, default=DFLT_PORT,
        help="Set the port number of the web interface [{}]".format(DFLT_PORT))
    return rv

def run():
    p = parser()
    args = p.parse_args()
 
    rv = 0
    if args.version:
        sys.stdout.write(__version__)
        sys.stdout.write("\n")
    else:
        rv = main(args)

    if rv == 2:
        sys.stderr.write("\n Missing command.\n\n")
        p.print_help()

    sys.exit(rv)

if __name__ == "__main__":
    run()
