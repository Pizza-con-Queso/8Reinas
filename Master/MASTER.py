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

# pantalla(whoiam)


posiciones = []

posicion_act = 0

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
	# posicion_act =+ num
	prep_men(num)
	
def envio(posiciones):
	for i in range(len(posiciones)):
		if len(posiciones) == 1:
			print("Enviando R2")
			mbox1.send(posiciones[i])
			pantalla("Enviamos: " + posiciones[i])
			wait(5000)
		elif len(posiciones) == 2:
			print("Enviando R3")
			mbox2.send(posiciones[i]) 
			pantalla("Enviamos: " + posiciones[i])
			wait(5000)
		elif len(posiciones) == 3:
			print("Enviando R4")
		 	mbox3.send(posiciones[i])
			pantalla("Enviamos: " + posiciones[i])
			wait(5000)
		elif len(posiciones) == 4:
			ev3.play_notes(['C','C','D','D'])
			pass

while True:
    if len(posiciones) == 0:
        avanzar(1)
        pantalla("Envio")
        envio(posiciones)
        
        pantalla("L 100")
        
    if mbox1.wait_new():
        mensaje1 = mbox1.read()
        print("Mensaje R2: ", mensaje1)
        pantalla("Recibimos R1 " + mensaje1)
        
        if len(mensaje1) == 4:
            pantalla("Recibimos R1\n" + mensaje1)
            posiciones.append(mensaje1)
            envio(posiciones)
        else:
            posiciones.pop(0)
            pantalla("Linea 112")
    if mbox2.wait_new():
        mensaje2 = mbox2.read()
        print("Mensaje R3: ", mensaje2)
        pantalla(mensaje2)
        
        if len(mensaje2) == 4:
            pantalla("Recibimos R2\n"+ mensaje2)
            posiciones.append(mensaje2)
            envio(posiciones)
        else:
            posiciones.pop(1)
            pantalla('ErrordePos')
            mbox1.send("error")
    pantalla("Linea 126")
    if mbox3.wait_new():
        mensaje3 = mbox3.read()
        print("Mensaje R4: ", mensaje3)
        
        if len(mensaje3) == 4:
            pantalla("Recibimos R3\n" + mensaje3)
            posiciones.append(mensaje3)
            envio(posiciones)
        else:
            posiciones.pop(2)
            mbox2.send("error")


