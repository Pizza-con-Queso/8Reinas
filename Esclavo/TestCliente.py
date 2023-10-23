from pybricks.hubs import EV3Brick
from pybricks.ev3devices import BluetoothClient
from pybricks.parameters import Button

# Inicializa el ladrillo EV3
ev3 = EV3Brick()

# Configura el cliente Bluetooth para el esclavo
cliente = BluetoothClient("Server")

while not Button.CENTER in ev3.buttons.pressed():
    # Envía datos al servidor
    mensaje = "Hola desde el esclavo"
    cliente.write(mensaje)

    # Espera para recibir datos del servidor
    data = cliente.read(32)
    if data:
        # Procesa los datos o realiza acciones necesarias
        ev3.screen.clear()
        ev3.screen.draw_text(10, 10, "Mensaje del servidor")
        ev3.screen.draw_text(10, 30, data.decode('utf-8'))
        ev3.speaker.beep()

# Cierra la conexión antes de salir del programa
cliente.disconnect()