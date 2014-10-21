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

