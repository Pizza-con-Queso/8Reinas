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
    
    wait(4000)
    
    ev3.screen.clear()

whoiam = int(nombre()[5])


posiciones = []

posicion_act = int(0)

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

def avanzar(posicion_act):
    # ev3.screen.print('Hello!')
	# robot.straight(num)
	posicion_act = posicion_act + 1
	prep_men(posicion_act)
	return posicion_act
	
def envio(posiciones):
	ev3 = EV3Brick()
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
			ev3.speaker.beep()
			pass

while True:

	if len(posiciones) == 0:
		if posicion_act == 4:
			mbox1.send('exito')
			mbox2.send('exito')
			mbox3.send('exito')
			break
		posicion_act = avanzar(posicion_act)
		envio(posiciones)
		ult_reina_com = 1
	
	if ult_reina_com == 1: #
		print('esperando mensaje r2')
		mbox1.wait()
		print('mensaje recibido r2')
		print('mensaje de la reina 2: '+ mbox1.read())
		pantalla("Recibimos R2 " + mbox1.read())
		if len(mbox1.read()) == 4:
			posiciones.append(mbox1.read())
			envio(posiciones) # envio a la siguiente reina
			ult_reina_com = 2
		else:
			posiciones.pop(-1)
			ult_reina_com = 0
	
	if ult_reina_com == 2:
		print('esperando mensaje r3')
		mbox2.wait()
		print('mensaje recibido r3')
		print('mensaje de la reina 3: '+mbox2.read())
		pantalla(mbox2.read())
		if len(mbox2.read()) == 4:
			pantalla("Recibimos R3")
			posiciones.append(mbox2.read())
			envio(posiciones)# envio a la siguiente reina
			ult_reina_com = 3
		else:
			posiciones.pop(-1)
			mbox1.send("error")
			print('mensaje error enviado a reina 2')
			ult_reina_com = 1

	if ult_reina_com == 3:
		print('esperando mensaje r4')
		mbox3.wait() 
		print('mensaje de la reina 4: '+mbox3.read())
		print('mensaje recibido r4')
		if len(mbox3.read()) == 4:
			pantalla("Recibimos R4")
			posiciones.append(mbox3.read())
			envio(posiciones)# beep
			posiciones.pop(-1)
			mbox3.send('avanza')
		else:
			posiciones.pop(-1)
			mbox2.send("error")
			print('mensaje error enviado a reina 3')
			ult_reina_com = 2