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
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet.serialport import SerialPort
from twisted.python import usage

def setBit(v, index, x):
    """Set the index:th bit of v to x, and return the new value."""
    mask = 1 << index
    v &= ~mask
    if x:
        v |= mask
    return v

class CliOptions(usage.Options):
    """
    Parses command-line options for our applications
    """
    optParameters = [
        ['baudrate', 'b', 115200, 'Serial baudrate'],
        ['port', 'p', '/dev/ttyACM0', 'Serial port to use'],]


class Capsule:
    """
    Representation of the capsule
    """

    def __init__(self, comm):
        self.motor = False
        self.fan   = False
        self.comm  = comm
    
    def setMotor(self, motorValue):
        self.sendMessage(0, motorValue, self.fan);

    def setFan(self, fanValue):
        self.sendMessage(0, self.motor, fanValue);

    def sendMessage(self, msgType, msgMotor, msgFan):
        msg = 0
        msg = setBit(msg, 0, msgType)
        msg = setBit(msg, 1, msgMotor)
        msg = setBit(msg, 2, msgFan)
        self.motor = msgMotor
        self.fan   = msgFan
        self.comm.write(msg)

class Echo(SerialPort):
    """
    Prints the data received from the arduino
    """

    def __init__(self):
        self.capsule = Capsule(self);

    def processData(self, data):
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
        reactor.callLater(0, self.doSomething)

    def doSomething(self):
        self.capsule.setMotor(not self.capsule.motor);
        reactor.callLater(1000, self.doSomething)


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
        raise SystemExit, 1

    baudrate = o.opts['baudrate']
    port = o.opts['port']
    logging.debug('About to open port %s' % port)
    s = SerialPort(Echo(), port, reactor, baudrate=baudrate)
    reactor.run()


if __name__ == '__main__':
    run()

