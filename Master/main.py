#!/usr/bin/env pybricks-micropython

# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!

from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from pybricks.hubs import EV3Brick
from pybricks.tools import wait

    
def pantalla(mensaje_coso, i):
    # Mensaje que deseas mostrar en la pantalla
    mensaje = mensaje_coso + str(i)

    # Muestra el mensaje en la pantalla
    ev3.screen.print(mensaje)
    wait(5000)
    # Limpia la pantalla
    ev3.screen.clear()
# Inicializa el ladrillo EV3
ev3 = EV3Brick()

server = BluetoothMailboxServer()

server.wait_for_connection(2)
# server.wait_for_connection()

mbox1 = TextMailbox('greeting1', server)
mbox2 = TextMailbox('greeting2', server)
# The server must be started before the client!
print('waiting for connection...')
print('connected!')

# In this program, the server waits for the client to send the first message
# and then sends a reply.
i = 0
while True:
    print("en el while")
    
    if mbox1.read():
        mensaje_recibido_cli1 = mbox1.read()
        pantalla(mensaje_recibido_cli1, i)
        mbox1.send('Soy R1!__')
    
    if mbox2.read():
        mensaje_recibido_cli2 = mbox2.read()
        pantalla(mensaje_recibido_cli2, i)
        mbox2.send('hello!__')
    
    i += 1
