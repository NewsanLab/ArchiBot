import board
import pwmio
from adafruit_motor import servo
import digitalio
import busio
import time

ang_rodilla = None
ang_pata_abierta = None
ang_pata_cerrada = None
lectura_bt = None
index = None

pmw_pins = [board.GP2, board.GP3, board.GP4, board.GP7, board.GP28, board.GP27, board.GP22, board.GP21, board.GP14, board.GP15]
servos = []
for pin in pmw_pins:
  pwm = pwmio.PWMOut(pin, frequency = 50)
  servos.append(servo.Servo(pwm))

laser = digitalio.DigitalInOut(board.GP26)
laser.direction = digitalio.Direction.OUTPUT

hc05 = busio.UART(board.GP12, board.GP13, baudrate = 9600)

def mover_laser_arriba():
  global ang_rodilla, ang_pata_abierta, ang_pata_cerrada, lectura_bt, index
  if (servos[9].angle <= 178):
    servos[9].angle = (servos[9].angle + 1)

def mover_laser_abajo():
  global ang_rodilla, ang_pata_abierta, ang_pata_cerrada, lectura_bt, index
  if (servos[9].angle >= 2):
    servos[9].angle = (servos[9].angle - 1)
    
def mover_laser_derecha():
  global ang_rodilla, ang_pata_abierta, ang_pata_cerrada, lectura_bt, index
  if (servos[8].angle >= 2):
    servos[8].angle = (servos[9].angle - 1)

def mover_laser_izquierda():
  global ang_rodilla, ang_pata_abierta, ang_pata_cerrada, lectura_bt, index
  if (servos[8].angle <= 178):
    servos[8].angle = (servos[9].angle + 1)

def caminar_atras_agachado():
  global ang_rodilla, ang_pata_abierta, ang_pata_cerrada, lectura_bt, index
  servos[4].angle = 160
  servos[2].angle = 160
  servos[1].angle = 40
  servos[7].angle = 140
  servos[5].angle = 40
  servos[3].angle = 140
  time.sleep(0.2)
  servos[4].angle = 145
  servos[2].angle = 145
  servos[0].angle = 160
  servos[6].angle = 160
  servos[3].angle = 40
  servos[5].angle = 140
  servos[1].angle = 140
  servos[7].angle = 40
  time.sleep(0.2)
  servos[0].angle = 145
  servos[6].angle = 145

def caminar_atras_parado():
  global ang_rodilla, ang_pata_abierta, ang_pata_cerrada, lectura_bt, index
  servos[4].angle = 140
  servos[2].angle = 140
  servos[1].angle = 40
  servos[7].angle = 140
  servos[5].angle = 40
  servos[3].angle = 140
  time.sleep(0.2)
  servos[4].angle = 90
  servos[2].angle = 90
  servos[0].angle = 140
  servos[6].angle = 140
  servos[3].angle = 40
  servos[5].angle = 140
  servos[1].angle = 140
  servos[7].angle = 40
  time.sleep(0.2)
  servos[0].angle = 90
  servos[6].angle = 90

def caminar_adelante_parado():
  global ang_rodilla, ang_pata_abierta, ang_pata_cerrada, lectura_bt, index
  servos[4].angle = 140
  servos[2].angle = 140
  servos[1].angle = 140
  servos[7].angle = 40
  servos[5].angle = 140
  servos[3].angle = 40
  time.sleep(0.2)
  servos[4].angle = 90
  servos[2].angle = 90
  servos[0].angle = 140
  servos[6].angle = 140
  servos[3].angle = 140
  servos[5].angle = 40
  servos[1].angle = 40
  servos[7].angle = 140
  time.sleep(0.2)
  servos[0].angle = 90
  servos[6].angle = 90


def caminar_adelante_agachado():
  global ang_rodilla, ang_pata_abierta, ang_pata_cerrada, lectura_bt, index
  servos[4].angle = 160
  servos[2].angle = 160
  servos[1].angle = 140
  servos[7].angle = 40
  servos[5].angle = 140
  servos[3].angle = 40
  time.sleep(0.2)
  servos[4].angle = 145
  servos[2].angle = 145
  servos[0].angle = 160
  servos[6].angle = 160
  servos[3].angle = 140
  servos[5].angle = 40
  servos[1].angle = 40
  servos[7].angle = 140
  time.sleep(0.2)
  servos[0].angle = 145
  servos[6].angle = 145

def align_legs(ang):
  servos[0].angle = ang
  servos[2].angle = ang
  servos[4].angle = ang
  servos[6].angle = ang

def calibrar():
  global ang_rodilla, ang_pata_abierta, ang_pata_cerrada, lectura_bt, index
  servos[5].angle = 90
  servos[1].angle = 90
  servos[7].angle = 90
  servos[3].angle = 90
  align_legs(90)
  time.sleep(1)
  servos[9].angle = 90
  servos[8].angle = 90
  time.sleep(1)


def dance():
  global ang_rodilla, ang_pata_abierta, ang_pata_cerrada, lectura_bt, index
  calibrar()
  servos[4].angle = 140
  servos[0].angle = 140
  servos[5].angle = 145
  servos[1].angle = 35
  time.sleep(0.4)
  for index in range(3):
    servos[3].angle = 130
    servos[7].angle = 130
    time.sleep(0.3)
    servos[3].angle = 50
    servos[7].angle = 50
    time.sleep(0.3)
  calibrar()

def giros(ang_rodilla, ang_pata_abierta, ang_pata_cerrada):
  global lectura_bt, index
  servos[0].angle = ang_pata_abierta
  servos[6].angle = ang_pata_abierta
  servos[7].angle = ang_rodilla
  servos[1].angle = ang_rodilla
  time.sleep(0.1)
  align_legs(ang_pata_cerrada)
  time.sleep(0.1)
  servos[4].angle = ang_pata_abierta
  servos[2].angle = ang_pata_abierta
  servos[5].angle = ang_rodilla
  servos[3].angle = ang_rodilla
  time.sleep(0.1)
  align_legs(ang_pata_cerrada)
  servos[5].angle = 90
  servos[1].angle = 90
  servos[7].angle = 90
  servos[3].angle = 90
  time.sleep(0.1)

def disparar():
  global ang_rodilla, ang_pata_abierta, ang_pata_cerrada, lectura_bt, index
  laser.value = True
  time.sleep(0.4)
  laser.value = False


def main():
  calibrar()
  while True:
    lectura_bt = hc05.read(1)
    if (lectura_bt == b"F"):
      caminar_adelante_parado()
    elif (lectura_bt == b"B"):
      caminar_atras_parado()
    elif (lectura_bt == b"L"):
      giros(150, 120, 90)
    elif (lectura_bt == b"R"):
      giros(30, 120, 90)
    elif (lectura_bt == b"Y"):
      caminar_adelante_agachado()
    elif (lectura_bt == b"H"):
      caminar_atras_agachado()
    elif (lectura_bt == b"G"):
      giros(130, 150, 135)
    elif (lectura_bt == b"J"):
      giros(50, 150, 135)
    elif (lectura_bt == b"S"):
      hc05.reset_input_buffer()
    elif (lectura_bt == b"2"):
      mover_laser_arriba()
    elif (lectura_bt == b"8"):
      mover_laser_abajo()
    elif (lectura_bt == b"4"):
      mover_laser_izquierda()
    elif (lectura_bt == b"6"):
      mover_laser_derecha()
    elif (lectura_bt == b"T"):
      disparar()
    elif (lectura_bt == b"D"):
      dance()

main()