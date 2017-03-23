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
import webbrowser

from blessings import Terminal
import pkg_resources

from turberfield.dialogue import __version__
from turberfield.dialogue.directives import Pathfinder
from turberfield.dialogue.model import SceneScript
from turberfield.utils.assembly import Assembly
from turberfield.utils.misc import log_setup

DFLT_PORT = 8080
DFLT_DB = ":memory:"

__doc__ = """
A utility to run through a sequence of dialogue.

The rehearsal can be viewed in a terminal or by web browser.

Eg::

    turberfield-rehearse @turberfield/dialogue/demo.cli

"""


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

        for n, (shot, item) in enumerate(model):
            yield (shot, item)

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

def producer(args, log=None):
    log = log or logging.getLogger("turberfield")
    folder = Pathfinder.string_import(
        args.sequence, relative=False, sep=":"
    )
    ensemble = Pathfinder.string_import(
        args.ensemble, relative=False, sep=":"
    )
    scripts = SceneScript.scripts(**folder._asdict())
    for script, interlude in itertools.zip_longest(
        scripts, itertools.cycle(folder.interludes)
    ):
        prev = None
        seq = run_through(script, ensemble, log)
        for n, (shot, item) in enumerate(seq):
            yield item
            time.sleep(1)

def cgi_consumer(args):
    params = vars(args)
    params["session"] = uuid.uuid4().hex
    opts = urllib.parse.urlencode(params)
    url = "http://localhost:{0}/turberfield-rehearse?{1}".format(args.port, opts)
    rv = textwrap.dedent("""
        Content-type:text/html

        <!doctype html>
        <html lang="en">
        <head>
        <meta charset="utf-8" />
        <title>Rehearsal</title>
        </head>
        <body class="loading">
        <h1>...</h1>
        <div id="data"></div>
        <script>
            var fx;

            if (!!window.EventSource) {{
                var source = new EventSource("{url}");
            }} else {{
                alert("Your browser does not support Server-Sent Events.");
            }}

            source.addEventListener("audio", function(e) {{
                var obj = JSON.parse(e.data)
                var url = ("/" + obj.package.replace(/\./g, "/") + "/" + obj.resource);
                fx = document.createElement("audio");
                fx.setAttribute("src", url);
                fx.play();
                console.log(url);
            }}, false);

            source.addEventListener("line", function(e) {{
                console.log(e.data);
            }}, false);

            source.addEventListener("memory", function(e) {{
                console.log(e.data);
            }}, false);

            source.addEventListener("property", function(e) {{
                console.log(e.data);
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
    for n, item in enumerate(producer(args)):
        print("event: {0}".format(type(item).__name__.lower()), end="\n")
        print("data: {0}\n".format(Assembly.dumps(item)), end="\n")
        sys.stdout.flush()

    return n

def greet(terminal):
    with terminal.location(0, terminal.height - 1):
        print("This is ", terminal.underline("pretty!"), file=terminal.stream)

def main(args):
    log = logging.getLogger(log_setup(args))
    if args.web:
        locn = "Scripts" if "windows" in platform.system().lower() else "bin"
        os.chdir(os.path.join(sys.prefix, locn))
        log.warning("Web mode: running scripts from directory {0}".format(os.getcwd()))
        params = {
            k: getattr(args, k)
            for k in (
                "log_level", "log_path", "port",
                "session", "ensemble", "sequence"
            )
        }
        opts = urllib.parse.urlencode(params)
        url = "http://localhost:{0}/turberfield-rehearse?{1}".format(args.port, opts)
        webbrowser.open_new_tab(url)
        Handler = http.server.CGIHTTPRequestHandler
        Handler.cgi_directories = ["/"]
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
            cgi_producer(args)
    else:
        print(cgi_consumer(args))
        term = Terminal()
        greet(term)
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
