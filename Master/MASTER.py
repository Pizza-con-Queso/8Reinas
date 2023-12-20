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



def pantalla(mensaje_coso):
    ev3 = EV3Brick()
    
    ev3.screen.print(mensaje_coso)
    
    wait(5000)
    
    ev3.screen.clear()

whoiam = int(nombre()[5])

pantalla(whoiam)


posiciones = []

posicion_act = 0
ult_reina_com = 0

def prep_men(posicion_act):
	mensaje = "r"+str(whoiam)+"p"+str(posicion_act)
	print(mensaje)
	posiciones.append(mensaje)
 	print("Mensaje ingresado:", posiciones)
	pantalla(mensaje)

server = BluetoothMailboxServer()


'''
Pruebas!!
'''
server.wait_for_connection(3)
mbox1 = TextMailbox('reina2', server)
mbox2 = TextMailbox('reina3', server)
mbox3 = TextMailbox('reina4', server)
pantalla("Conectados")

#-----------------------------------------------------#

ev3 = EV3Brick()

# motor_izquierdo = Motor(Port.B)
# motor_derecho = Motor(Port.C)

# robot = DriveBase(motor_izquierdo, motor_derecho, wheel_diameter=55, axle_track=104)

def avanzar(num):
    # ev3.screen.print('Hello!')
	# robot.straight(num)
	posicion_act =+ num
	prep_men(posicion_act)
	
def envio(posiciones):
	for i in range(len(posiciones)):
		if len(posiciones) == 1:
      		# print("Enviando ", 1)
			mbox1.send(posiciones[i])
			pantalla("Enviamos: " + posiciones[i])
			wait(5000)
		elif len(posiciones) == 2:
			mbox2.send(posiciones[i]) 
			pantalla("Enviamos: " + posiciones[i])
			wait(5000)
		elif len(posiciones) == 3:
		 	mbox3.send(posiciones[i])
			pantalla("Enviamos: " + posiciones[i])
			wait(5000)
		elif len(posiciones) == 4:
			ev3.play_notes(['C','C','D','D'])
			pass

while True:
	# mbox1.wait()
	# mbox2.wait()
	# mbox3.wait()
	if len(posiciones) == 0:
    	# print("Primer if")
		avanzar(1)
		# print("Avance")
		envio(posiciones)
		ult_reina_com = 1
		# print("Envio")
	
	if ult_reina_com == 1: #
		mbox1.wait_new() 
		print(mbox1.read())
		pantalla("Recibimos R2 " + mbox1.read())
		if len(mbox1.read()) == 4:
			#pantalla("Recibimos R1 " + mbox1.read())
			posiciones.append(mbox1.read())
			envio(posiciones)
			ult_reina_com = 2
		else:
			posiciones.pop(0)
			ult_reina_com = 0
	
	if ult_reina_com == 2:
		mbox2.wait_new() 
		print(mbox2.read())
		pantalla(mbox2.read())
		if len(mbox2.read()) == 4:
			pantalla("Recibimos R3")
			posiciones.append(mbox2.read())
			envio(posiciones)
			ult_reina_com = 3
		else:
			posiciones.pop(1)
			pantalla('ErrordePos')
			mbox1.send("error")
			ult_reina_com = 1

	if ult_reina_com == 3:
		mbox3.wait_new() 
		if len(mbox3.read()) == 4:
			pantalla("Recibimos R4")
			posiciones.append(mbox3.read())
			envio(posiciones)
			ult_reina_com = 0
		else:
			posiciones.pop(2)
			mbox2.send("error")
			ult_reina_com = 2