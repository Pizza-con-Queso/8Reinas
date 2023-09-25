#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from pybricks.messaging import BluetoothMailboxClient, TextMailbox

# # This is the name of the remote EV3 or PC we are connecting to.
# SERVER = 'ev3dev'

# # -------Este es el Master-------

# client = BluetoothMailboxClient()
# mbox = TextMailbox('greeting', client)

# print('establishing connection...')
# client.connect(SERVER)
# print('connected!')

# # In this program, the client sends the first message and then waits for the
# # server to reply.
# mbox.send('hello!')
# mbox.wait()
# print(mbox.read())

# Inicializamos la posición actual
import os
from pybricks.messaging import BluetoothMailboxClient, TextMailbox
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button
# This is the name of the remote EV3 or PC we are connecting to.
SERVER = 'reina1'

client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)


try:
        with open('/etc/hostname') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('reina'):
                    name = line.split()
except Exception as e:
    print(str(e))


print(name[0])
print('establishing connection...')
client.connect(SERVER)
print('connected!')

# In this program, the client sends the first message and then waits for the
# server to reply.
mbox.send(name[0])
mbox.wait()
print(mbox.read())
