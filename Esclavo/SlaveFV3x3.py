#!/usr/bin/env pybricks-micropython
from pybricks.messaging import BluetoothMailboxServer, BluetoothMailboxClient, TextMailbox
from pybricks.hubs import EV3Brick
from pybricks.tools import wait
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, GyroSensor


def pantalla(mensaje_coso):
	ev3 = EV3Brick()
		
	ev3.screen.print(mensaje_coso)
		
	wait(4000)
		
	ev3.screen.clear()


'''
---------------------------------------------------------------------------------------------------------------
		Variables globales
		whoiam:   representa el número de la reina que corresponde, deriva de la función
									de consulta al robot previamente formateado.
		posicion_actual:            representa la posición en la que se encuentra el robot en este momento,
									de ser cero el robot está fuera del tablero y si está entre 1 a 8, se
									encuentra en una posición ubicado.
		posiciones_otras_reinas:    representa la lista de las reinas que se encuentran posicionadas 
									anteriormente. No incluye la posición de whoiam.
---------------------------------------------------------------------------------------------------------------
'''

posicion_actual = 0
posiciones_otras_reinas = [] # Input: [número del robot, número de la posición]

motor_izquierdo = Motor(Port.D)
motor_derecho = Motor(Port.A)
robot = DriveBase(motor_izquierdo, motor_derecho, wheel_diameter=55, axle_track=104)
robot.settings(straight_speed=40)
gyro = GyroSensor(Port.S1)
gyro.reset_angle(0)

'''
Función de nombre del robot
'''

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

'''
---------------------------------------------------------------------------------------------------------------
		Función que calcula la posición de la reina respecto a las reinas anteriores, 
		sólo opera cuando es la reina a la que le corresponde avanzar. Retorna n, el cual si es igual al número
		del robot la posición se considera válida, de lo contrario avanza a una nueva posición.

		posiciones:   lista de listas de las posiciones de las reinas anteriores. Ej: [[1,1], [2,3]]
		whoiam: número propio de la reina.
		posicion_actual:    posición actual de la reina
---------------------------------------------------------------------------------------------------------------
'''
def calcular_posicion_anterior(posiciones, whoiam, posicion_actual):
	n = 0
	for i in range(len(posiciones)):
		if calcular_pendiente(posiciones[i][0], posiciones[i][1], whoiam, posicion_actual):
			n = n + 1
		else:
			break
	return n


'''
---------------------------------------------------------------------------------------------------------------
		Función de avance para el robot.
---------------------------------------------------------------------------------------------------------------
'''

def avanzar(posicion_actual):
	GSPK = 2
	speed = 20
	posicion_actual = posicion_actual + 1
	if posicion_actual > 3:
		while robot.distance() >= 0: 
			correction = (0 - gyro.angle())*GSPK
			robot.drive(-speed,correction)
		robot.stop()
		motor_izquierdo.brake()
		motor_derecho.brake()
		return 0
	else:
		distancia = 150*posicion_actual
		while robot.distance() <= distancia: # 
			correction = (0 - gyro.angle())*GSPK
			robot.drive(speed,correction)
		robot.stop()
		motor_izquierdo.brake()
		motor_derecho.brake()
		wait(2000)
		return posicion_actual


'''
---------------------------------------------------------------------------------------------------------------
		Función de cálculo de pendiente, en caso de encontrarse en la trayectoria de las esquinas o en la 
		misma posición que la reina consultada, este retorna falso, caso contrario cuando la reina de ubicarse 
		ahí no generaría conflicto con esa reina en particular.

		x1:   Eje x de la reina posicionada, también es el número de la reina que corresponde.
		y1:   Eje y de la reina posicionada.
		x2:   Eje x de la reina, esta se desea posicionar.
		y2:   Eje y de la reina, posible posición del tablero que se consulta 
								(siempre es de 1 a 8, la dimensión del tablero).
---------------------------------------------------------------------------------------------------------------
'''

def calcular_pendiente(x1, y1, x2, y2):
	pendiente = (y2 - y1) / (x2 - x1)
	if pendiente == float(1) or pendiente == float(0) or pendiente == float(-1):
		return False
	else:
		return True
		

'''
---------------------------------------------------------------------------------------------------------------
		Función que ingresa todas las posiciones recibidas por mensaje a una lista de posiciones
---------------------------------------------------------------------------------------------------------------
'''

def depurar_ingreso_blue(mensaje, whoiam):
	x, y = int(mensaje[1]), int(mensaje[3])
	# global whoiam
	posiciones_otras_reinas.append([x,y])
'''
---------------------------------------------------------------------------------------------------------------
		Forma de llamar a las funciones.
---------------------------------------------------------------------------------------------------------------
'''

ev3 = EV3Brick()

SERVER = 'reina1'
client = BluetoothMailboxClient()
mbox = TextMailbox(nombre(), client)
wait(10000)
client.connect(SERVER)

while True:
	mbox.wait()
	if len(mbox.read())==4*(whoiam-1):
	  for i in range(0, len(mbox.read()), 4):
	     depurar_ingreso_blue(mbox.read()[i:i+4],whoiam)
	  pantalla("Recibimos! ")

	if mbox.read() == 'exito':
	  break
		
	while True:
	  if posicion_actual == 3:
	     posicion_actual = avanzar(posicion_actual)
	     mbox.send('error')
	     posiciones_otras_reinas = []
	     break
	  posicion_actual = avanzar(posicion_actual)
	  if calcular_posicion_anterior(posiciones_otras_reinas,whoiam,posicion_actual) == whoiam-1:
	     mbox.send("r"+str(whoiam)+"p"+str(posicion_actual))
	     break