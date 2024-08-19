import board
import adafruit_74hc595
import busio
import digitalio
import simpleio

hc05 = busio.UART(board.GP8, board.GP9, baudrate = 9600)

def control_motor(sr, motor_pins, value_a, value_b):
    motor = sr.get_pin(motor_pins[0])
    motor.value = value_a
    motor = sr.get_pin(motor_pins[1])
    motor.value = value_b

def reset_pin_74hc595(sr):
    for i in range(8):
        pin = sr.get_pin(i)
        pin.value = False

def init_pwm(pin):
    pwm = digitalio.DigitalInOut(pin)
    pwm.direction = digitalio.Direction.OUTPUT
    return pwm

def forward(sr):
    control_motor(sr, [0, 1], False, True)
    control_motor(sr, [2, 3], False, True)
    control_motor(sr, [4, 5], False, True)
    control_motor(sr, [6, 7], False, True)

def back(sr):
    control_motor(sr, [0, 1], True, False)
    control_motor(sr, [2, 3], True, False)
    control_motor(sr, [4, 5], True, False)
    control_motor(sr, [6, 7], True, False)

def left(sr):
    control_motor(sr, [0, 1], False, True) # delantero izquierdo
    control_motor(sr, [2, 3], False, True) # trasero izquierdo
    control_motor(sr, [6, 7], True, False) # delantero derecho
    control_motor(sr, [4, 5], True, False) # trasero derecho

def right(sr):
    control_motor(sr, [6, 7], False, True) # delantero derecho
    control_motor(sr, [4, 5], False, True) # trasero derecho
    control_motor(sr, [0, 1], True, False) # delantero izquierdo
    control_motor(sr, [2, 3], True, False) # trasero izquierdo

def stop(sr):
    control_motor(sr, [0, 1], False, False)
    control_motor(sr, [2, 3], False, False) # Stop motor
    control_motor(sr, [4, 5], False, False)
    control_motor(sr, [6, 7], False, False)

def main():
    sr = adafruit_74hc595.ShiftRegister74HC595(busio.SPI(board.GP6, MOSI=board.GP7), digitalio.DigitalInOut(board.GP2))
    masa = digitalio.DigitalInOut(board.GP18)
    masa.direction = digitalio.Direction.OUTPUT
    masa.value = False
    pwm1 = init_pwm(board.GP3)
    pwm2 = init_pwm(board.GP4)
    pwm3 = init_pwm(board.GP5)
    pwm4 = init_pwm(board.GP11)

    pwm1.value = True # pin 0, 1
    pwm2.value = True # pin 2, 3
    pwm3.value = True # pin 4, 5
    pwm4.value = True # pin 6, 7
    
    # para olvidar el ultimo estado, sino siempre recuerda el ultimo estado y arranca desde ahi 
    reset_pin_74hc595(sr)

    while True:
        bt = hc05.read(1)
        if (bt == b"C"):
            stop(sr)
            hc05.reset_input_buffer()
        if (bt == b"W"):
            forward(sr)
        if (bt == b"S"):
            back(sr)
        if (bt == b"A"):
            left(sr)
        if (bt == b"D"):
            right(sr)
        if (bt == b"B"):
            simpleio.tone(board.BUZZER, 370, duration = 0.3)

main()
