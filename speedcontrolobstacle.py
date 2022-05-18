import RPi.GPIO as gpio
import time
import serial

#motor notations
left_motor_cw=31
left_motor_ccw=32
right_motor_cw=15
right_motor_ccw=16
speed=50
frequency=100
limit=100
tim=0.8

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(left_motor_cw,gpio.OUT)
gpio.setup(left_motor_ccw,gpio.OUT)
gpio.setup(right_motor_cw,gpio.OUT)
gpio.setup(right_motor_ccw,gpio.OUT)

l_cw=gpio.PWM(left_motor_cw,frequency)
l_ccw=gpio.PWM(left_motor_ccw,frequency)
r_cw=gpio.PWM(right_motor_cw,frequency)
r_ccw=gpio.PWM(right_motor_ccw,frequency)


def goforward():
    print('going forward')
    stop()
    l_cw.start(speed)
    r_cw.start(speed)

def distances():
    global distance
    distance=[]
    ser.write(b'g')
    arduis=ser.readlines()
    distance=[int(i.decode('ascii').rstrip('\r\n')) for i in arduis]

def turnleft():
    stop()
    print('turning left')
    r_cw.start(speed)
    time.sleep(tim)
    r_cw.stop()

def turnright():
    stop()
    print('turning right')
    l_cw.start(speed)
    time.sleep(tim)
    l_cw.stop()

def gobackward():
    stop()
    print('going backward')
    l_ccw.start(speed)
    r_ccw.start(speed)
    time.sleep(tim)

def stop():
    print('stopped')
    l_cw.stop()
    r_cw.stop()
    l_ccw.stop()
    r_ccw.stop()

ser =serial.Serial('/dev/ttyACM0',baudrate=9600,timeout=1)
distance=[]
stop()
while True:
    try:
        distances()
        print(distance)
        if len(distance)==0:
            continue
        elif distance[0]<limit and distance[1]<limit and distance[2]<limit:
            gobackward()
            turnleft()
            stop()
        elif distance[0]<limit:
            turnright()
        elif distance[1]<limit:
            turnleft()
        elif distance[2]<limit:
            turnleft()
        else:
            goforward()
    except KeyboardInterrupt:
        gpio.cleanup()
        break