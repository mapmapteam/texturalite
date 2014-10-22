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
Sends OSC to MapMap
"""
from twisted.internet import reactor
from txosc import async
from txosc import osc

class MapMapOsc(object):
    """
    Sends OSC to MapMap
    """
    def __init__(self, osc_port=12345, osc_host="localhost"):
        """
        """
        self._osc_port = 12345
        self._osc_host = "localhost"
        self._client_proto = None
        self._client_port = None
        self._init_osc()

    def _init_osc(self):
        self._client_proto = async.DatagramClientProtocol()
        self._client_port = reactor.listenUDP(0, self._client_proto)

    def _send_osc(self, message):
        """
        Sends a message using UDP and stops the Reactor
        @param message: OSC message
        @type message: L{txosc.osc.Message}
        """
        self._client_proto.send(message, (self._osc_host, self._osc_port))
        #print("Sent %s to %s:%d" % (message, self._osc_host, self._osc_port))

    def _create_play_message(self, mapping_id, uri):
        path = "/mapmap/paint/media/load"
        message = osc.Message(path)
        message.add(mapping_id)
        message.add(str(uri))
        return message

    def play(self, mapping_id, filepath):
        print("play %s" % (filepath))
        message = self._create_play_message(mapping_id, filepath)
        self._send_osc(message)

    def speed(self, mapping_id, speed_percent):
        path = "/mapmap/paint/media/speed"
        message = osc.Message(path)
        message.add(mapping_id)
        message.add(float(speed_percent))
        self._send_osc(message)

