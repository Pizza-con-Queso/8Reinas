#!/usr/bin/env pybricks-micropython
# from pybricks.hubs import EV3Brick
# from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
#                                  InfraredSensor, UltrasonicSensor, GyroSensor)
# from pybricks.parameters import Port, Stop, Direction, Button, Color
# from pybricks.tools import wait, StopWatch, DataLog
# from pybricks.robotics import DriveBase
# from pybricks.media.ev3dev import SoundFile, ImageFile
# from pybricks.robotics import DriveMotor

# # This program requires LEGO EV3 MicroPython v2.0 or higher.
# # Click "Open user guide" on the EV3 extension tab for more information.


# # Create your objects here.
# ev3 = EV3Brick()

# rueda_izq = Port()
# rueda_derecha = Port()

# robot = DriveBase()
# from pybricks.messaging import BluetoothMailboxServer, TextMailbox

# server = BluetoothMailboxServer()
# mbox = TextMailbox('greeting', server)

# # The server must be started before the client!
# print('waiting for connection...')
# server.wait_for_connection()
# print('connected!')

# # In this program, the server waits for the client to send the first message
# # and then sends a reply.
# mbox.wait()
# print(mbox.read())
# mbox.send('hello to you!')

# # Write your program here.
# # ev3.speaker.beep()

# from pybricks.hubs import EV3Brick
# from pybricks.ev3devices import Motor
# from pybricks.robotics import DriveBase
# from pybricks.parameters import Port

# # Inicializamos la posición actual
# posicion_actual = 5

# # Inicializamos el robot y los motores
# ev3 = EV3Brick()
# motor_izquierdo = Motor(Port.B)
# motor_derecho = Motor(Port.C)

# # Creamos una instancia de DriveBase para controlar el robot con los dos motores
# robot = DriveBase(motor_izquierdo, motor_derecho, wheel_diameter=55, axle_track=104)

# # while True:
#     # Solicitamos una posición al usuario
# posicion_nueva = 2
# print("hola")
# # Validamos si el usuario quiere salir
# if posicion_nueva == -1:
#     # break  # Salir del bucle si se ingresa -1
#     pass

# # Validamos que la posición ingresada esté dentro del rango permitido
# elif 1 <= posicion_nueva <= 8:
#     # Calculamos la diferencia entre las posiciones
#     diferencia = posicion_nueva - posicion_actual
#     print("if")
#     # Actualizamos la posición actual
#     posicion_actual = posicion_nueva

#     # Movemos el robot hacia adelante o hacia atrás según la diferencia
#     distancia_a_avanzar = diferencia * 100  # Puedes ajustar la velocidad y distancia según tus necesidades

#     robot.straight(distancia_a_avanzar)

#     # Mostramos la diferencia y la posición actual actualizada
#     # print(f"Diferencia: {diferencia}")
#     # print(f"Posición actual: {posicion_actual}")
# else:
#     print("La posición ingresada no está en el rango permitido (1-8).")

# # print("¡Gracias por usar el programa!")

from pybricks.messaging import BluetoothMailboxServer, TextMailbox

server = BluetoothMailboxServer()
mbox = TextMailbox('greeting', server)

# The server must be started before the client!
print('waiting for connection...')
server.wait_for_connection()
print('connected!')

# In this program, the server waits for the client to send the first message
# and then sends a reply.
mbox.wait()
print(mbox.read())


server.wait_for_connection()
mbox.wait()
print(mbox.read())

server.wait_for_connection()
mbox.wait()
print(mbox.read())
mbox.send('hello to you!')