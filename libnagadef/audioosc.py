#!/usr/bin/env python
from twisted.internet import reactor
from txosc import async
from txosc import osc

class AudioOsc(object):
    """
    Sends OSC to audio player
    """
    def __init__(self, osc_port=11111, osc_host="localhost"):
        """
        """
        self._osc_port = osc_port
        self._osc_host = osc_host
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

    def set_volumes(self, vol_0, vol_1):
        path = "/texturalite/sound/amp"
        message0 = osc.Message(path)
        message0.add(0)
        message0.add(float(vol_0))
        self._send_osc(message0)

        message1 = osc.Message(path)
        message0.add(1)
        message0.add(float(vol_1))
        self._send_osc(message1)

    def set_speeds(self, speed0, speed1):
        path = "/texturalite/sound/speed"
        message0 = osc.Message(path)
        message0.add(0)
        message0.add(float(speed_0))
        self._send_osc(message0)

        message1 = osc.Message(path)
        message0.add(1)
        message0.add(float(speed_1))
        self._send_osc(message1)

