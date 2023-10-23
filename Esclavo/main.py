#!/usr/bin/env pybricks-micropython

# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!

from pybricks.messaging import BluetoothMailboxClient, TextMailbox
from pybricks.hubs import EV3Brick
from pybricks.tools import wait

# Inicializa el ladrillo EV3
ev3 = EV3Brick()

def pantalla(mensaje_coso, i):
    # Mensaje que deseas mostrar en la pantalla
    mensaje = mensaje_coso + str(i)

    # Muestra el mensaje en la pantalla
    ev3.screen.print(mensaje)
    wait(5000)
    # Limpia la pantalla
    ev3.screen.clear()


# This is the name of the remote EV3 or PC we are connecting to.
SERVER = 'reina1'

client = BluetoothMailboxClient()
mbox = TextMailbox('greeting1', client)

print('establishing connection...')
client.connect(SERVER)
print('connected!')

# In this program, the client sends the first message and then waits for the
# server to reply.
i = 0
while True:
    mbox.send('Soy R2!___')
    mbox.wait()
    mensaje = mbox.read()
    # print(mbox.read())
    pantalla(mensaje, i)
    i += 1