#!/usr/bin/env python
# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Toonloop clips player
#
# Copyright 2010 Alexandre Quessy
# http://www.toonloop.com
#
# Original idea by Alexandre Quessy
# http://alexandre.quessy.net
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
Main entry point of the application.
"""
import os
import sys
import optparse
from twisted.internet import reactor
from libnagadef import __version__
from libnagadef import vj
from libnagadef import config

DEFAULT_DIRECTORY = "~/Videos"
DEFAULT_CONFIG_FILE = "~/.nagadef"

def run():
    parser = optparse.OptionParser(usage="%prog [configuration file name]", version=str(__version__))
    parser.add_option("-c", "--config-file", type="string", help="Specifies the JSON config file. You can also simply specify the config file as the first argument.")
    parser.add_option("-v", "--verbose", action="store_true", help="Makes the logging output verbose.")
    (options, args) = parser.parse_args()
    
    # Parse config file name:
    config_file = None
    if options.config_file:
        config_file = options.config_file
    elif len(args) >= 1:
        config_file = args[0]
    else:
        config_file = os.path.expanduser(DEFAULT_CONFIG_FILE)
        # ???
        # if os.path.exists(config_file):
        #     config_file = check_dir
    
    try:
        configuration = config.load_from_file(config_file)
    except RuntimeError, e:
        print(e)
        sys.exit(1)

    if options.verbose:
        configuration.verbose = True

    _vj = vj.VeeJay(configuration)
    try:
        _vj.start()
    except RuntimeError, e:
        print("ERROR playing next cue: %s" % (e))
        sys.exit(1)

    try:
        reactor.run()
    except KeyboardInterrupt:
        print("")
        sys.exit(0)

