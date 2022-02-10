import _thread
from typing import final
import serial
import RPi.GPIO as gpio
import time
#motor notations
left_motor_cw=31
left_motor_ccw=32
right_motor_cw=15
right_motor_ccw=16


def goforward():
    global left_motor_ccw,left_motor_cw,right_motor_ccw,right_motor_cw
    gpio.output(left_motor_cw,gpio.HIGH)
    gpio.output(right_motor_cw,gpio.HIGH)
    print('going forward')

def turnleft():
    global let_motor_ccw,left_motor_cw,right_motor_ccw,right_motor_cw
    gpio.output(right_motor_cw,gpio.HIGH)
    gpio.output(left_motor_cw,gpio.LOW)
    print('turning left')
    time.sleep(0.8)
    gpio.output(right_motor_cw,gpio.LOW)

def turnright():
    global left_motor_ccw,left_motor_cw,right_motor_ccw,right_motor_cw
    gpio.output(left_motor_cw,gpio.HIGH)
    gpio.output(right_motor_cw,gpio.LOW)
    print('turning right')
    time.sleep(0.8)
    gpio.output(left_motor_cw,gpio.LOW)

def gobackward():
    global left_motor_ccw,left_motor_cw,right_motor_ccw,right_motor_cw
    gpio.output(left_motor_ccw,gpio.HIGH)
    gpio.output(right_motor_ccw,gpio.HIGH)
    print('going backward')

def stop():
    global left_motor_ccw,left_motor_cw,right_motor_ccw,right_motor_cw
    gpio.output(left_motor_cw,gpio.LOW)
    gpio.output(left_motor_ccw,gpio.LOW)
    gpio.output(right_motor_cw,gpio.LOW)
    gpio.output(right_motor_ccw,gpio.LOW)

def checkanddriveright():
    while int(distance[-1][0]) < 30:
        stop()
        turnleft()
        time.sleep(1)
        if int(distance[-1][0]) < 30:
            break
    goforward()

def checkanddriveleft():
    while int(distance[-1][1]) < 30:
        stop()
        turnright()
        time.sleep(1)
        if int(distance[-1][1]) < 30:
            break
    goforward()

# Define a function for the thread
def serial_monitor(iss):
    gpio.setmode(gpio.BOARD)
    gpio.setwarnings(False)
    gpio.setup(left_motor_cw,gpio.OUT)
    gpio.setup(left_motor_ccw,gpio.OUT)
    gpio.setup(right_motor_cw,gpio.OUT)
    gpio.setup(right_motor_ccw,gpio.OUT)
    global distance
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if len(distance)>10:
            distance=[distance[-1]]
        if ser.in_waiting > 0:
            line = ser.readline().decode('ascii').rstrip()
            distance.append(line.split(' '))


def motor_control(ssi):
    goforward()
    while True:
        try:
            if int(distance[-1][0]) < 30:
                stop()
                print(int(distance[-1][0]))
                print('in checkanddriveright')
                checkanddriveright()
            elif int(distance[-1][1]) < 30:
                stop()
                print(int(distance[-1][1]))
                print('in checkanddriveleft')
                checkanddriveleft()
            else:
                goforward()
        except:
            pass

distance=[]
try:
    _thread.start_new_thread(serial_monitor,(1,))
    _thread.start_new_thread(motor_control,(1,))
except KeyboardInterrupt:
    print ("Error: unable to start thread")
finally:
    gpio.cleanup()
try:
    while 1:
        pass
except KeyboardInterrupt:
    pass
finally:
    gpio.cleanup()
