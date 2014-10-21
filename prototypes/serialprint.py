#!/usr/bin/env python
"""
Prints data received from the Arduino.
Part of the Texturalite project.
Authors: Alexandre Quessy, Sofian Audry.
Date: 2014
Dependencies: python-twisted python-serial
"""
import logging
import sys
import serial
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet import task
from twisted.internet.serialport import SerialPort
from twisted.python import usage


class CliOptions(usage.Options):
    """
    Parses command-line options for our applications
    """
    optParameters = [
        ['baudrate', 'b', 115200, 'Serial baudrate'],
        ['port', 'p', '/dev/ttyACM0', 'Serial port to use'],]


class Echo(LineReceiver):
    """
    Prints the data received from the arduino
    """
    def __init__(self, app):
        self._app = app

    def processData(self, data):
        if data == "y":
            self._app.set_hand_connected(True)
        elif data == "n":
            self._app.set_hand_connected(False)
        print(data)

    def lineReceived(self, line):
        try:
            data = line.rstrip()
            #logging.debug(data)
            self.processData(data)
        except ValueError:
            logging.error('Unable to parse data %s' % line)
            return

    def connectionMade(self):
        self._app.connection_made_cb()


class Application(object):
    """
    Our main logic.
    """
    def __init__(self, baudrate, serial_port):
        """
        Constructor.
        """
        self._arduino_connected = False
        # Stores the state of the capsule.
        self._capsule = {
            "hands": False,
            "motor": False,
            "fan": False,
            }
        logging.debug('About to open port %s' % serial_port)
        try:
            self._serial = SerialPort(Echo(self), serial_port, reactor, baudrate=baudrate)
        except serial.serialutil.SerialException, e:
            print(e)
            sys.exit(1)
        self._looping_call = task.LoopingCall(self._looping_call_cb)
        self._looping_call.start(50, now=False)

    def _looping_call_cb(self):
        """
        Called at a regular interval.
        """
        if not self._arduino_connected:
            return
        # if the arduino is connected:

        # toggle motor
        self._capsule["motor"] = not self._capsule["motor"]
        self.set_motor(self._capsule["motor"])

        # toggle fan
        self._capsule["fan"] = not self._capsule["fan"]
        self.set_fan(self._capsule["fan"])

        print("%s" % (self._capsule))


    def set_hand_connected(self, is_connected):
        self._capsule["hands"] = is_connected
        if is_connected:
            print("yes")
        else:
            print("no")

    def connection_made_cb(self):
        self._arduino_connected = True

    def set_motor(self, is_enabled):
        """
        Turn on or off the motor.
        """
        if is_enabled:
            self._serial.sendLine("M")
        else:
            self._serial.sendLine("m")

    def set_fan(self, is_enabled):
        """
        Turn on or off the fan.
        """
        if is_enabled:
            self._serial.sendLine("F")
        else:
            self._serial.sendLine("f")


def run():
    """
    Main entry of our application.
    """
    o = CliOptions()
    try:
        o.parseOptions()
    except usage.UsageError, errortext:
        logging.error('%s %s' % (sys.argv[0], errortext))
        logging.info('Try %s --help for usage details' % sys.argv[0])
        sys.exit(1)
    baudrate = o.opts['baudrate']
    port = o.opts['port']
    app = Application(baudrate, port)
    reactor.run()


if __name__ == '__main__':
    run()

