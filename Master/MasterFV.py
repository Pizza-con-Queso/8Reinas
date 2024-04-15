#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, GyroSensor
from pybricks.messaging import BluetoothMailboxServer, TextMailbox

import urandom

motor_izquierdo = Motor(Port.D)
motor_derecho = Motor(Port.A)
robot = DriveBase(motor_izquierdo, motor_derecho, wheel_diameter=55, axle_track=80)
robot.settings(straight_speed=30)
gyro = GyroSensor(Port.S1)
gyro.reset_angle(0)

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
		
	wait(1000)
		
	ev3.screen.clear()

whoiam = int(nombre()[5])


posiciones = ''

posicion_act = int(0)

ult_reina_com = 0

distancia = 0

def prep_men(posicion_act):
	mensaje = "r"+str(whoiam)+"p"+str(posicion_act)
	return mensaje

server = BluetoothMailboxServer()

lista = []

while True:
	value = urandom.randrange(1,9,1)
	
	print(lista)
	if value not in lista:
		lista.append(value)

	if len(lista) == 8:
		break



# Pruebas!!
print('esperando conexion')
server.wait_for_connection(7)
mbox1 = TextMailbox('reina2', server)
mbox2 = TextMailbox('reina3', server)
mbox3 = TextMailbox('reina4', server)
mbox4 = TextMailbox('reina5', server)
mbox5 = TextMailbox('reina6', server)
mbox6 = TextMailbox('reina7', server)
mbox7 = TextMailbox('reina8', server)
pantalla("Conectados")

#-----------------------------------------------------#

ev3 = EV3Brick()

def avanzar(posicion_act, distancia):
	if lista:
		aux = lista[0] - posicion_act
		posicion_act = lista[0]
		del lista[0]
	else:
		distancia = 0
		aux = 0
	
	distancia += 150*aux 
	GSPK = 2
	speed = 20
	print('distancia: ',distancia)
	print('robotd: ', robot.distance())
	while True:
		if robot.distance() <= distancia: # 
			while robot.distance() <= distancia: # 
				correction = (0 - gyro.angle())*GSPK
				robot.drive(speed,correction)

			robot.stop()
			motor_izquierdo.brake()
			motor_derecho.brake()
			wait(1000)
			break
		else:
			while robot.distance() >= abs(distancia): 
				correction = (0 - gyro.angle())*GSPK
				robot.drive(-speed,correction)
			robot.stop()
			motor_izquierdo.brake()
			motor_derecho.brake()
			wait(1000)
			break

	return posicion_act
	
def envio(posiciones):
	ev3 = EV3Brick()
	if len(posiciones) == 4:
		mbox1.send(posiciones)
	elif len(posiciones) == 8:
		mbox2.send(posiciones) 
	elif len(posiciones) == 12:
		mbox3.send(posiciones)
	elif len(posiciones) == 16:
		mbox4.send(posiciones)
	elif len(posiciones) == 20:  
		mbox5.send(posiciones)
	elif len(posiciones) == 24:
		mbox6.send(posiciones)
	elif len(posiciones) == 28:
		mbox7.send(posiciones)
	elif len(posiciones) == 32:
		ev3.speaker.beep()

while True:
	
	if len(posiciones) == 0:
		if not lista:
			distancia = 0
			mbox1.send('exito')
			mbox2.send('exito')
			mbox3.send('exito')
			mbox4.send('exito')
			mbox5.send('exito')
			mbox6.send('exito')
			mbox7.send('exito')
			avanzar(posicion_act, distancia)
			break
		posicion_act = avanzar(posicion_act, distancia)
		distancia = 150*posicion_act
		posiciones += prep_men(posicion_act)
		envio(posiciones)
		ult_reina_com = 1
	
	if ult_reina_com == 1:
		mbox1.wait()
		pantalla("Recibimos R2 " + mbox1.read())
		if len(mbox1.read()) == 4:
			posiciones += mbox1.read()
			envio(posiciones)
			ult_reina_com = 2
		else:
			posiciones = posiciones[:-4]
			ult_reina_com = 0
	
	if ult_reina_com == 2:
		mbox2.wait()
		pantalla("Recibimos R3 " + mbox2.read())
		if len(mbox2.read()) == 4:
			pantalla("Recibimos R3")
			posiciones += mbox2.read()
			envio(posiciones)# envio a la siguiente reina
			ult_reina_com = 3
		else:
			posiciones = posiciones[:-4]
			mbox1.send("error")
			print('mensaje error enviado a reina 2')
			ult_reina_com = 1

	if ult_reina_com == 3:
		mbox3.wait()
		pantalla("Recibimos R4 " + mbox3.read())
		if len(mbox3.read()) == 4:
			posiciones += mbox3.read()
			envio(posiciones)
			ult_reina_com = 4
		else:
			posiciones = posiciones[:-4]
			mbox2.send("error")
			print('mensaje error enviado a reina 2')
			ult_reina_com = 2
		
		
	if ult_reina_com == 4:
		mbox4.wait()
		pantalla("Recibimos R5 " + mbox4.read())
		if len(mbox4.read()) == 4:
			posiciones += mbox4.read()
			envio(posiciones)
			ult_reina_com = 5
		else:
			posiciones = posiciones[:-4]
			mbox3.send("error")
			ult_reina_com = 3
		
	if ult_reina_com == 5:
		mbox5.wait()
		pantalla("Recibimos R6 " + mbox5.read())
		if len(mbox5.read()) == 4:
			posiciones += mbox5.read()
			envio(posiciones)# envio a la siguiente reina
			ult_reina_com = 6
		else:
			posiciones = posiciones[:-4]
			mbox4.send("error")
			ult_reina_com = 4
		
	if ult_reina_com == 6:
		mbox6.wait()
		pantalla("Recibimos R6 " + mbox6.read())
		if len(mbox6.read()) == 4:
			posiciones += mbox6.read()
			envio(posiciones)# envio a la siguiente reina
			ult_reina_com = 7
		else:
			posiciones = posiciones[:-4]
			mbox5.send("error")
			ult_reina_com = 5
		
	if ult_reina_com == 7:
		mbox7.wait() 
		if len(mbox7.read()) == 4:
			pantalla("Recibimos R4")
			posiciones += mbox7.read()
			envio(posiciones)# beep
			posiciones = posiciones[:-4]
			mbox7.send('avanza')
		else:
			posiciones = posiciones[:-4]
			mbox6.send("error")
			ult_reina_com = 6