#!/usr/bin/env python3
#   coding: UTF-8

import argparse
import cgi
import cgitb
import http.server
import logging
from logging.handlers import WatchedFileHandler
import os.path
import platform
import sys
import tempfile
import urllib.parse
import webbrowser

from blessings import Terminal
import pkg_resources

from turberfield.dialogue import __version__

DFLT_PORT = 8080
DFLT_DB = ":memory:"

__doc__ = """
An experimental script which can operate in CLI, web or terminal mode.

TODO:

https://medium.com/code-zen/python-generator-and-html-server-sent-events-3cdf14140e56#.k9y3ez6se
"""

def build_logger(args, name="turberfield"):
    log = logging.getLogger(name)
    log.setLevel(args.log_level)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-7s %(name)s|%(message)s")
    ch = logging.StreamHandler()

    if args.log_path is None:
        ch.setLevel(args.log_level)
    else:
        fh = WatchedFileHandler(args.log_path)
        fh.setLevel(args.log_level)
        fh.setFormatter(formatter)
        log.addHandler(fh)
        ch.setLevel(logging.WARNING)

    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log

def hello(args):
    print("Content-type:text/html")
    print()
    print("<html>")
    print('<head>')
    print('<title>SSE</title>')
    print('</head>')
    print('<body>')
    form = cgi.FieldStorage()
    for k in form.keys():
        print('<p>{0}: {1}</p>'.format(k, form[k].value))
    print('</body>')
    print('</html>')

def greet(terminal):
    with terminal.location(0, terminal.height - 1):
        print("This is ", terminal.underline("pretty!"), file=terminal.stream)

def main(args):
    log = build_logger(args)
    if args.web:
        locn = "Scripts" if "windows" in platform.system().lower() else "bin"
        os.chdir(os.path.join(sys.prefix, locn))
        log.warning("Web mode: running scripts from directory {0}".format(os.getcwd()))
        fd, session = tempfile.mkstemp(text=True)
        opts = urllib.parse.urlencode({"session": session})
        url = "http://localhost:8080/turberfield-rehearse" + "?" + opts
        webbrowser.open_new_tab(url)
        Handler = http.server.CGIHTTPRequestHandler
        Handler.cgi_directories = ["/"]
        httpd = http.server.HTTPServer(("", args.port), Handler)

        log.info("serving at port {0}".format(args.port))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            os.close(fd)
            log.info("Shutdown.")
            return 0

    if "SERVER_NAME" in os.environ:
        cgitb.enable()
        hello(args)
        log.info(args.cgi)
    else:
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
        "--web", action="store_true", default=False,
        help="Activate the web interface")
    rv.add_argument(
        "--port", type=int, default=DFLT_PORT,
        help="Set the port number of the web interface [{}]".format(DFLT_PORT))
    rv.add_argument("cgi", nargs="*")
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
