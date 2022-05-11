import time
import serial
import RPi.GPIO as gpio
#motor notations
gpio.setmode(gpio.BOARD)
left_motor_cw=31
left_motor_ccw=32
right_motor_cw=15
right_motor_ccw=16
gpio.setup(left_motor_cw,gpio.OUT)
gpio.setup(left_motor_ccw,gpio.OUT)
gpio.setup(right_motor_cw,gpio.OUT)
gpio.setup(right_motor_ccw,gpio.OUT)
def distances():
    global distance
    distance=[]
    ser.write(b'g')
    arduis=ser.readlines()
    distance=[int(i.decode('ascii').rstrip('\r\n')) for i in arduis]


def goforward():
    global left_motor_ccw,left_motor_cw,right_motor_ccw,right_motor_cw
    print('going forward')
    gpio.output(left_motor_cw,gpio.HIGH)
    gpio.output(right_motor_cw,gpio.HIGH)
    

def turnleft():
    global left_motor_ccw,left_motor_cw,right_motor_ccw,right_motor_cw
    print('turning left')
    gpio.output(right_motor_cw,gpio.HIGH)
    gpio.output(left_motor_cw,gpio.LOW)
    time.sleep(0.8)
    gpio.output(right_motor_cw,gpio.LOW)

def turnright():
    global left_motor_ccw,left_motor_cw,right_motor_ccw,right_motor_cw
    print('turning right')
    gpio.output(left_motor_cw,gpio.HIGH)
    gpio.output(right_motor_cw,gpio.LOW)
    time.sleep(0.8)
    gpio.outpu(left_motor_cw,gpio.LOW)

def gobackward():
    global left_motor_ccw,left_motor_cw,right_motor_ccw,right_motor_cw
    gpio.output(left_motor_ccw,gpio.HIGH)
    gpio.output(right_motor_ccw,gpio.HIGH)

def stop():
    global left_motor_ccw,left_motor_cw,right_motor_ccw,right_motor_cw
    gpio.output(left_motor_cw,gpio.LOW)
    gpio.output(left_motor_ccw,gpio.LOW)
    gpio.output(right_motor_cw,gpio.LOW)
    gpio.output(right_motor_ccw,gpio.LOW)

def checkanddriveright():
    while True:
        stop()
        turnright()
        distances()
        if distance[0]>50:
            break
    goforward()

def checkanddriveleft():
    while True:
        stop()
        turnleft()
        distances()
        if distance[1]>50:
            break
    goforward()

def motor_control():
    print('in motor control')
    goforward()
    while True:
        try:
            distances()
            if len(distance)==0:
              continue
            if distance[0]<50:
                checkanddriveright()
            elif distance[1]<50:
                checkanddriveleft()
        except KeyboardInterrupt:
            gpio.cleanup()
        finally:
            gpio.cleanup()
print('asking for serial communication')
ser= serial.Serial('/dev/ttyACM0',baudrate=9600,timeout=1)
distance=[]
print('serial connection done')
motor_control()
