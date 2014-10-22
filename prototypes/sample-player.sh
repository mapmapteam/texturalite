#!/usr/bin/env python
# encoding: utf-8
"""
Sound player

"""

from pyo import *

OSC_ADDRESS_BASE = "/texturalite/sound/"
OSC_ADDRESS_SPEED = OSC_ADDRESS_BASE + "speed"
OSC_ADDRESS_AMP = OSC_ADDRESS_BASE + "amp"
OSC_ADDRESS_TERMINATE = OSC_ADDRESS_BASE + "terminate"

OSC_PORT = 12345
N_STATES = 2

SOUND_FILES = ["./flute.aif", 
               "./baseballmajeur_m.aif"]
N_STATES = len(SOUND_FILES)

# Start server
server = Server(sr=44100, nchnls=2, buffersize=512, duplex=0).boot()

server.start()

players = [ SfPlayer(SOUND_FILES[i], loop=True, speed=1).play() for i in range(N_STATES) ]
mixer = Mixer(outs=1, chnls=2, time=0.050)
for i in range(N_STATES):
    mixer.addInput(i, players[i])
    mixer.setAmp(i, 0, 0) # disable both

mixer.out()

def oscProcess(address, *args):
    if (address == OSC_ADDRESS_SPEED):
        players[args[0]].setSpeed(args[1])
    else:
        mixer.setAmp(args[0], 0, args[1])

oscRecvSpeed = OscDataReceive(OSC_PORT, OSC_ADDRESS_SPEED, oscProcess)
oscRecvSpeed.addAddress(OSC_ADDRESS_AMP)
oscRecvSpeed.addAddress(OSC_ADDRESS_TERMINATE)

# 

currentFileIndex = 0

while (True):
    time.sleep(1)

#while (True):
#    time.sleep(5.0)
#    currentFileIndex = (currentFileIndex+1) % len(soundFiles)
#    player.setSound(SOUND_FILES[currentFileIndex])

server.stop()
time.sleep(0.25)
server.shutdown()    
#s.gui(locals())

