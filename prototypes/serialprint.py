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
import time
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet import task
from twisted.internet.serialport import SerialPort
from twisted.python import usage

class Timer(object):
    """
    Returns elapsed time.
    """
    def __init__(self):
        self._started = time.time()

    def elapsed(self):
        return time.time() - self._started

    def reset(self):
        self._started = time.time()


class CliOptions(usage.Options):
    """
    Parses command-line options for our applications
    """
    optParameters = [
        ['baudrate', 'b', 115200, 'Serial baudrate'],
        ['port', 'p', '/dev/ttyUSB0', 'Serial port to use'],]


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
        print("Received %s" % (data))

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
        self._serial = None
        self._arduino_connected = False
        self._timer = Timer()
        # Stores the state of the capsule.
        self._capsule = {
            "hands": False,
            "motor": False,
            "fan": False,
            }
        try:
            #logging.debug('About to open port %s' % serial_port)
            print('About to open port %s' % serial_port)
            self._serial = SerialPort(Echo(self), serial_port, reactor, baudrate=baudrate)
            print('Success opening port %s' % serial_port)
        except serial.serialutil.SerialException, e:
            print('Failed opening port %s' % serial_port)
            print(e)
            sys.exit(1)

        print("start task")
        self._looping_call = task.LoopingCall(self._looping_call_cb)
        self._looping_call.start(0.05, now=False)

    def _looping_call_cb(self):
        """
        Called at a regular interval.
        """
        #print("_looping_call_cb")
        if not self._arduino_connected:
            print("Arduino is not connected")
            return
        # if the arduino is connected:

        if self._timer.elapsed() >= 1.0:
            # send read
            self.send_read_hands()

            # toggle motor
            self._capsule["motor"] = not self._capsule["motor"]
            self.set_motor(self._capsule["motor"])

            # toggle fan
            self._capsule["fan"] = not self._capsule["fan"]
            self.set_fan(self._capsule["fan"])

            print("capsule: %s" % (self._capsule))
            self._timer.reset()


    def set_hand_connected(self, is_connected):
        self._capsule["hands"] = is_connected
        if is_connected:
            print("hand yes")
        else:
            print("hand no")

    def connection_made_cb(self):
        self._arduino_connected = True

        # if self._serial is not None:
        #     self.set_motor(True)

    def set_motor(self, is_enabled):
        """
        Turn on or off the motor.
        """
        if is_enabled:
            self.send_to_arduino("M")
        else:
            self.send_to_arduino("m")

    def set_fan(self, is_enabled):
        """
        Turn on or off the fan.
        """
        if is_enabled:
            self.send_to_arduino("F")
        else:
            self.send_to_arduino("f")

    def send_read_hands(self):
        self.send_to_arduino("R")

    def send_to_arduino(self, txt):
        #data = "%s\n" % (txt)
        print("send %s" % (txt))
        self._serial.protocol.sendLine(txt) # transport.write(data)


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

