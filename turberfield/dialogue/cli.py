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


import argparse
from collections import OrderedDict
import logging
import shutil
import textwrap

DEFAULT_PAUSE_SECS = 1.5
DEFAULT_DWELL_SECS = 0.2

def pause(shot, item, dwell=1.5, rate=1):
    return dwell + rate * 0.2 * item.text.count(" ")

def line(shot, item):
    print("\n")
    print(item.persona.name.firstname, item.persona.name.surname, sep=" ")
    print(textwrap.indent(item.text, " " * 16))
 
def ensemble_menu(log):
    log.info("Painting ensemble menu...")
    castList = OrderedDict(gather_installed("turberfield.interfaces.ensemble", log=log))
    print("\n")
    print(
        *["\t{0}: {1} ({2} members)".format(n, k, len(v)) for n, (k, v) in enumerate(castList.items())],
        sep="\n")
    index = int(input("\nChoose an ensemble: "))
    choice = list(castList.keys())[index]
    log.info("Selected ensemble '{0}'.".format(choice))
    return castList[choice]

def seq_menu(log):
    log.info("Painting sequence menu...")
    seqList = OrderedDict(gather_installed("turberfield.interfaces.sequence", log=log))
    print("\n")
    print(
        *["\t{0}: {1} ({2} members)".format(n, k, len(v.paths)) for n, (k, v) in enumerate(seqList.items())],
        sep="\n")
    index = int(input("\nChoose a sequence: "))
    choice = list(seqList.keys())[index]
    log.info("Selected sequence '{0}'.".format(choice))
    return seqList[choice]

def clear_screen():
    n = shutil.get_terminal_size().lines
    print("\n" * n, end="")
    return n

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
        "--log", default=None, dest="log_path",
        help="Set a file path for log output")
    return rv

def add_common_options(parser):
    parser.add_argument(
        "--version", action="store_true", default=False,
        help="Print the current version number")
    parser.add_argument(
        "-v", "--verbose", required=False,
        action="store_const", dest="log_level",
        const=logging.DEBUG, default=logging.INFO,
        help="Increase the verbosity of output")
    parser.add_argument(
        "--log", default=None, dest="log_path",
        help="Set a file path for log output")
    return parser

def add_casting_options(parser):
    parser.add_argument(
        "--references", default="",
        help="Give an import path to a list of Python references."
    )
    parser.add_argument(
        "--sequence", default="",
        help="Give an import path to a sequence of SceneScript folders."
    )
    parser.add_argument(
        "--roles", type=int, default=1,
        help="The number of roles [1] permitted for each member of cast."
    )
    parser.add_argument(
        "--strict", action="store_true", default=False,
        help="Only perform fully-cast scene files.")
    return parser

def add_performance_options(parser):
    parser.add_argument(
        "--repeat", type=int, default=0,
        help="Repeat the rehearsal [0] times."
    )
    parser.add_argument(
        "--pause", type=float, default=DEFAULT_PAUSE_SECS,
        help="Time in seconds [{0}] to pause after a line.".format(DEFAULT_PAUSE_SECS)
    )
    parser.add_argument(
        "--dwell", type=float, default=DEFAULT_DWELL_SECS,
        help="Time in seconds [{0}] to dwell on each word.".format(DEFAULT_DWELL_SECS)
    )
    return parser
