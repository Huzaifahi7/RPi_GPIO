import RPi.GPIO as gpio
import time
import serial

#motor notations
left_motor_cw=31
left_motor_ccw=32
right_motor_cw=15
right_motor_ccw=16
'''
motor_a_left=11
motor_a_right=37
motor_b_left=15
motor_b_right=13'''

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(left_motor_cw,gpio.OUT)
gpio.setup(left_motor_ccw,gpio.OUT)
gpio.setup(right_motor_cw,gpio.OUT)
gpio.setup(right_motor_ccw,gpio.OUT)


def goforward():
    print('going forward')
    gpio.output(left_motor_cw,gpio.HIGH)
    gpio.output(right_motor_cw,gpio.HIGH)
    
def distances():
    global distance
    distance=[]
    ser.write(b'g')
    arduis=ser.readlines()
    distance=[int(i.decode('ascii').rstrip('\r\n')) for i in arduis]

def turnleft():
    print('turning left')
    gpio.output(right_motor_cw,gpio.HIGH)
    gpio.output(left_motor_cw,gpio.LOW)
    time.sleep(0.8)
    gpio.output(right_motor_cw,gpio.LOW)

def turnright():
    print('turning right')
    gpio.output(left_motor_cw,gpio.HIGH)
    gpio.output(right_motor_cw,gpio.LOW)
    time.sleep(0.8)
    gpio.output(left_motor_cw,gpio.LOW)

def gobackward():
    print('going backward')
    gpio.output(left_motor_ccw,gpio.HIGH)
    gpio.output(right_motor_ccw,gpio.HIGH)
    time.sleep(0.8)

def stop():
    print('stopped')
    gpio.output(left_motor_cw,gpio.LOW)
    gpio.output(left_motor_ccw,gpio.LOW)
    gpio.output(right_motor_cw,gpio.LOW)
    gpio.output(right_motor_ccw,gpio.LOW)
ser =serial.Serial('/dev/ttyACM0',baudrate=9600,timeout=1)
distance=[]
goforward()
while True:
    distances()
    print(distance)
    try:
        if len(distance)==0:
            continue
        if distance[0]<50 and distance[1]<50:
            gobackward()
            turnleft()
        elif distance[0]<50:
            turnright()
        elif distance[1]<50:
            turnleft()
    except KeyboardInterrupt:
        gpio.cleanup()
        
