#!/usr/bin/env pybricks-micropython

# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!

from pybricks.messaging import BluetoothMailboxClient, TextMailbox
from pybricks.hubs import EV3Brick
from pybricks.tools import wait
# from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.robotics import DriveBase
from pybricks.parameters import Port


'''
---------------------------------------------------------------------------------------------------------------
        Variables globales
        whoiam:                     representa el número de la reina que corresponde, deriva de la función
                                    de consulta al robot previamente formateado.
        posicion_actual:            representa la posición en la que se encuentra el robot en este momento,
                                    de ser cero el robot está fuera del tablero y si está entre 1 a 8, se
                                    encuentra en una posición ubicado.
        posiciones_otras_reinas:    representa la lista de las reinas que se encuentran posicionadas 
                                    anteriormente. No incluye la posición de whoiam.
---------------------------------------------------------------------------------------------------------------
'''
whoiam = 4
posicion_actual = 0
posiciones_otras_reinas = [[1,1],[2, 3], [3, 5]] # número del robot, número de la posición


'''
---------------------------------------------------------------------------------------------------------------
        Función que permite determinar la distancia que debe moverse el robot por cada uno de los resultados.
        Si este avanza o vuelve a la posición inicial.

        posición:           nueva posición a la que debe moverse
        posicion_actual:    posición en la que se encuentra el robot
---------------------------------------------------------------------------------------------------------------
'''
def moverse_posicion(posicion, posicion_actual):
    if posicion == posicion_actual:
        print("Nos quedamos en el lugar")
        return True
    elif posicion == 0:
        distancia = posicion - posicion_actual
        print("Volvemos a la posición inicial, retrocedemos:", distancia, "distancia")
    else:
        distancia = posicion - posicion_actual
        print("Avanzamos:", distancia, "distancia")


'''
---------------------------------------------------------------------------------------------------------------
        Función que calcula las posibles posiciones disponibles respecto a las reinas anteriores a la propia, 
        sólo opera cuando es la reina a la que le corresponde avanzar. Retorna las posiciones que no generan 
        conflicto con las anteriores, puede ser una lista vacía cuando no existen posiciones.

        posiciones:         lista de listas de las posiciones de las otras reinas. Ej: [[1,1], [2,3]]
        whoiam:             número propio de la reina.
---------------------------------------------------------------------------------------------------------------
'''
def calcular_posicion_anterior(posiciones, whoiam):
    mis_posiciones_disponibles = []
    
    if whoiam == len(posiciones) + 1:

        for i in range(len(posiciones)):
            for j in range(1, 9):
                if calcular_pendiente(posiciones[i][0], posiciones[i][1], whoiam, j):
                    print("Posible posición respecto a la reina", posiciones[i][0], "Posición:", j)
                    mis_posiciones_disponibles.append([whoiam, j])
        mis_posiciones_disponibles = depurar(mis_posiciones_disponibles, len(posiciones))
        print(mis_posiciones_disponibles)
        
        return mis_posiciones_disponibles


'''
---------------------------------------------------------------------------------------------------------------
        Función que calcula las posibles posiciones respecto a las reinas anteriores a la propia, sólo opera
        cuando es la reina a la que le corresponde avanzar.

        posiciones:         lista de listas de las posiciones de las otras reinas. Ej: [[1,1], [2,3]]
        whoiam:             número propio de la reina.
---------------------------------------------------------------------------------------------------------------
'''
def posiciones_respecto_actual(disponibles, posicion_actual):
    # global posicion_actual
    if posicion_actual == 0:
        # MOVERSE ANTES DE CAMBIAR LA POSICIÓN ANTERIOR
        moverse_posicion(disponibles[0][1], posicion_actual)
        posicion_actual = disponibles[0][1]
    else:
        indice_actual = next((i for i, elemento in enumerate(disponibles) if elemento[1] == posicion_actual), None)
        if indice_actual is not None and indice_actual < len(disponibles) - 1:
            # MOVERSE ANTES DE CAMBIAR LA POSICIÓN ANTERIOR
            moverse_posicion(disponibles[indice_actual + 1][1], posicion_actual)
            posicion_actual = disponibles[indice_actual + 1][1]
        else:
            # MOVERSE ANTES DE CAMBIAR LA POSICIÓN ANTERIOR
            moverse_posicion(0, posicion_actual)
            posicion_actual = 0
    print(posicion_actual)
    return posicion_actual


'''
---------------------------------------------------------------------------------------------------------------
        Función que depura el listado de posiciones libres por cada una de las posiciones anteriores, en el 
        caso de aparecer la misma posición k veces (siendo k, la cantidad de reinas anteriores) esta se 
        conserva. La función entrega ordenadas de menor a mayor con respecto al segundo elemento de la sub 
        lista.

        lista_original:         lista de listas de las posiciones de las otras reinas. Ej: [[1,1], [2,3]]
        cant_reinas:            cantidad k de reinas que se debe repetir para que se conserve la posición.
---------------------------------------------------------------------------------------------------------------
'''
def depurar(lista_original, cant_reinas):

    if not lista_original:
        return []

    sublistas_repetidas = []
    sublistas_unicas = set()

    for sublista in lista_original:
        tupla_sublista = tuple(sublista)

        if tupla_sublista in sublistas_unicas:
            sublistas_repetidas.append(sublista)
        else:
            sublistas_unicas.add(tupla_sublista)

    sublistas_filtradas = [list(tupla) for tupla in sublistas_unicas if lista_original.count(list(tupla)) == cant_reinas]

    return sorted(sublistas_filtradas, key=lambda x: x[1])


'''
---------------------------------------------------------------------------------------------------------------
        Función de cálculo de pendiente, en caso de encontrarse en la trayectoria de las esquinas o en la 
        misma posición que la reina consultada, este retorna falso, caso contrario cuando la reina de ubicarse 
        ahí no generaría conflicto con esa reina en particular.

        x1:                     Eje x de la reina posicionada, también es el número de la reina que corresponde.
        y1:                     Eje y de la reina posicionada.
        x2:                     Eje x de la reina, esta se desea posicionar.
        y2:                     Eje y de la reina, posible posición del tablero que se consulta 
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
        Forma de llamar a las funciones.
---------------------------------------------------------------------------------------------------------------
'''
# posiciones_temporal = calcular_posicion_anterior(posiciones_otras_reinas, whoiam)
# if posiciones_temporal:
#     posiciones_respecto_actual(posiciones_temporal, posicion_actual)

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



# This is the name of the remote EV3 or PC we are connecting to.

ev3 = EV3Brick()
motor_izquierdo = Motor(Port.B)
motor_derecho = Motor(Port.C)

robot = DriveBase(motor_izquierdo, motor_derecho, wheel_diameter=55, axle_track=104)


SERVER = 'reina1'

client = BluetoothMailboxClient()
client.connect(SERVER)
mbox = TextMailbox(nombre(), client)

print('establishing connection...')
print('connected!')

# In this program, the client sends the first message and then waits for the
# server to reply.
i = 0
while True:
    print("Estamos en el while")
    mbox.send(nombre())
    mbox.wait()
    mensaje = mbox.read()
    if i == 0:
        robot.straight(int(mensaje))
    else:
        pantalla(mensaje, i)
    # print(mbox.read())
    # pantalla(mensaje, i)
    #break
    i += 1