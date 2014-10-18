#!/usr/bin/env python
# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# VideoControl
#
# Copyright 2010 Alexandre Quessy
# http://www.toonloop.com
#
# Toonloop is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Toonloop is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the gnu general public license
# along with Toonloop.  If not, see <http://www.gnu.org/licenses/>.
#
"""
VJ conductor
"""
import os
import sys
from twisted.internet import reactor
from twisted.internet import task
import random

class UrnRandom(object):
    """
    Pick random numbers from 0 to n - 1, avoiding repetitions.
    """
    def __init__(self, size=1):
        self._size = size
        self._elements = []
        self.reset()

    def reset(self):
        self._elements = range(self._size)
        self._elements = random.shuffle(self._elements)

    def pick(self):
        if self._size == 0:
            return None
        if len(self._elements) == 0:
            self.reset()
        ret = self._elements[0]
        self._elements = self._elements[1:] # pop
        return ret

    def set_size(self, size):
        self._size = size
        self.reset()


class VeeJay(object):
    """
    Chooses movie files to play.
    """
    def __init__(self, configuration):
        """
        @param configuration: vctrl.config.Configuration instance.
        """
        self.configuration = configuration
        self.clips = []
        self._current_cue_index = -1 # Initial non-existing cue
        self._urn = UrnRandom()
        self._init_urn()

    def _init_urn(self):
        num = len(self.get_cues())
        self._urn.set_size(num)

    def get_cues(self):
        return self.configuration.cues

    def start(self):
        self.play_next()

    def play_next(self):
        index = self._urn.pick()
        video_cue = self.get_cues()[index]
        reactor.callLater(video_cue.duration, self.play_next)

        print("TODO: send OSC message to play %s" % (video_cue.uri))

