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
import asyncio
import logging
import logging.handlers
import sys
import wave

import simpleaudio
import turberfield.dialogue.cli
from turberfield.utils.misc import log_setup

__doc__ = """
WAV file player.

"""

def main(args):
    loop = asyncio.get_event_loop()
    logName = log_setup(args, loop=loop)
    log = logging.getLogger(logName)
    try:
        log.info(args)

        data = wave.open(args.input, "rb")
        nChannels = data.getnchannels()
        bytesPerSample = data.getsampwidth()
        sampleRate = data.getframerate()
        nFrames = data.getnframes()
        framesPerMilliSecond = nChannels * sampleRate // 1000

        offset = framesPerMilliSecond * args.start
        duration = nFrames - offset
        if duration <= 0:
            log.error("Start beyond limits.")
            return 2
        duration = min(
            duration,
            framesPerMilliSecond * args.duration if args.duration is not None else duration
        )

        data.readframes(offset)

        frames = data.readframes(duration)
        for i in range(args.loop):
            waveObj = simpleaudio.WaveObject(frames, nChannels, bytesPerSample, sampleRate)
            playObj = waveObj.play()
            playObj.wait_done()
            # playObj.is_playing()

    except Exception as e:
        log.error(getattr(e, "args", e) or e) 
    finally:
        loop.close()

    return 0


def parser(descr=__doc__):
    rv = turberfield.dialogue.cli.parser(descr=__doc__)
    rv = argparse.ArgumentParser(description=descr)
    rv.add_argument(
        "--input", required=True,
        help="Set a file path for audio input")
    rv.add_argument(
        "--start", default=0, type=int,
        help="Set the starting offset (ms)")
    rv.add_argument(
        "--duration", default=None, type=int,
        help="Set the clip duration (ms)")
    rv.add_argument(
        "--loop", default=1, type=int,
        help="The number of times to loop the clip")
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
