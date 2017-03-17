#!/usr/bin/env python3
#   coding: UTF-8

import argparse
import cgi
import cgitb
import http.server
import logging
from logging.handlers import WatchedFileHandler
import os.path
import stat
import sys
import tempfile
import urllib.parse
import webbrowser

try:
    from blessings import Terminal
except ImportError:
    blessings = None

import pkg_resources

__version__ = "0.0.0"
__doc__ = """
An experimental script which can operate in CLI, web or terminal mode.

TODO:

https://medium.com/code-zen/python-generator-and-html-server-sent-events-3cdf14140e56#.k9y3ez6se
"""

def build_logger(args, name="pyspike"):
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
        perms = stat.S_IMODE(os.stat(__file__).st_mode)
        if perms != 0o755:
            log.warning("Bad permissions ({0}) for a CGI script".format(oct(perms)))
            return 1
        else:
            locn = os.path.abspath(pkg_resources.resource_filename(__name__, "."))
            os.chdir(locn)
            log.info("Web mode.")

        fd, session = tempfile.mkstemp(text=True)
        opts = urllib.parse.urlencode({"py": sys.executable, "session": session})
        url = "http://localhost:8080/multimode.py" + "?" + opts
        webbrowser.open_new_tab(url)
        PORT = 8080
        Handler = http.server.CGIHTTPRequestHandler
        Handler.cgi_directories = ["/"]
        httpd = http.server.HTTPServer(("", PORT), Handler)

        log.info("serving at port {0}".format(PORT))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            os.close(fd)
            log.info("Shutdown.")
            return 0

    log.info(os.environ)
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
