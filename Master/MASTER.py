#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor

from pybricks.messaging import BluetoothMailboxServer, TextMailbox

def nombre():
    try:
            with open('/etc/hostname') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith('reina'):
                        name = line.split()
    except Exception as e:
        print(str(e))
        
    return name[0]




whoiam = int(nombre()[5])

def pantalla(mensaje_coso):
    ev3 = EV3Brick
    # Mensaje que deseas mostrar en la pantalla
    # mensaje = mensaje_coso + str(i)
    # Muestra el mensaje en la pantalla
    ev3.screen.print(mensaje)
    wait(5000)
    # Limpia la pantalla
    ev3.screen.clear()


posiciones = []

posicion_act = 0

def prep_men(posicion_act):
	mensaje = "r"+str(whoiam)+"p"+str(posicion_act)
	print(mensaje)
	posiciones.append(mensaje)
	pantalla(mensaje)

server = BluetoothMailboxServer()

server.wait_for_connection(3)

mbox1 = TextMailbox('reina2', server)

mbox2 = TextMailbox('reina3', server)

mbox3 = TextMailbox('reina4', server)

ev3 = EV3Brick()

motor_izquierdo = Motor(Port.B)
motor_derecho = Motor(Port.C)

robot = DriveBase(motor_izquierdo, motor_derecho, wheel_diameter=55, axle_track=104)

def avanzar(num):
    ev3.screen.print('Hello!')
	# robot.straight(num)
	# posicion_act =+ num
	prep_men(num)
	
def envio(posiciones):
	for i in range(len(posiciones)):
		if len(posiciones) == 1:
			mbox1.send(posiciones[i])
		elif len(posiciones) == 2:
			mbox2.send(posiciones[i]) 
		elif len(posiciones) == 3:
			mbox3.send(posiciones[i])
		elif len(posiciones) == 4:
			# beep
			pass

while True:

	if len(posiciones) == 0:
    	# print("Primer if")
		avanzar(1)
		# print("Avance")
		envio(posiciones)
		# print("Envio")
	
	if mbox1.read(): # 
		if len(mbox1.read()) == 4:
			posiciones.append(mbox1.read())
			envio()
		else:
			posiciones.pop(0)

	if mbox2.read():
		if len(mbox2.read()) == 4:
			posiciones.append(mbox2.read())
			envio()
		else:
			posiciones.pop(1)
			mbox1.send("error")

	if mbox3.read():
		if len(mbox3.read()) == 4:
			posiciones.append(mbox3.read())
			envio()
		else:
			posiciones.pop(2)
			mbox2.send("error")


