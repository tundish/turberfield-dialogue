#!/usr/bin/env python3
#   -*- encoding: UTF-8 -*-

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
import asyncio
import logging
import logging.handlers
import sys

import simpleaudio
import turberfield.dialogue

__doc__ = """
WAV file player.

"""


def log_setup(args, name="turberfield.dialogue", loop=None):
    log = logging.getLogger(name)

    log.setLevel(args.log_level)
    logging.getLogger("asyncio").setLevel(args.log_level)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-7s %(name)s|%(message)s")
    ch = logging.StreamHandler()

    if args.log_path is None:
        ch.setLevel(args.log_level)
    else:
        fh = logging.handlers.WatchedFileHandler(args.log_path)
        fh.setLevel(args.log_level)
        fh.setFormatter(formatter)
        log.addHandler(fh)
        ch.setLevel(logging.WARNING)

    if loop is not None and args.log_level == logging.DEBUG:
        try:
            loop.set_debug(True)
        except AttributeError:
            log.info("Upgrade to Python 3.4.2 for asyncio debug mode")
        else:
            log.info("Event loop debug mode is {}".format(loop.get_debug()))
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return name

def main(args):
    loop = asyncio.get_event_loop()
    logName = log_setup(args, loop=loop)
    log = logging.getLogger(logName)
    try:
        log.info(args)

        waveObj = simpleaudio.WaveObject.from_wave_file(args.input)
        playObj = waveObj.play()
        playObj.wait_done()
    except Exception as e:
        log.error(getattr(e, "args", e) or e) 
    finally:
        loop.close()

    return 0


def parser(descr=__doc__):
    rv = argparse.ArgumentParser(description=descr)
    rv.add_argument(
        "--version", action="store_true", default=False,
        help="Print the current version number")
    rv.add_argument(
        "-v", "--verbose", required=False,
        action="store_const", dest="log_level",
        const=logging.DEBUG, default=logging.INFO,
        help="Increase the verbosity of output")
    rv.add_argument(
        "--input", required=True,
        help="Set a file path for audio input")
    rv.add_argument(
        "--interval", default=None, type=int,
        help="Set the indexing interval (s)")
    rv.add_argument(
        "--log", default=None, dest="log_path",
        help="Set a file path for log output")
    return rv


def run():
    p = parser()
    args = p.parse_args()
    if args.version:
        sys.stdout.write(turberfield.dialogue.__version__ + "\n")
        rv = 0
    else:
        rv = main(args)
    sys.exit(rv)


if __name__ == "__main__":
    run()
