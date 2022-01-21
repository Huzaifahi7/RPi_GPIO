import _thread
import time
from typing import final
import serial
import RPi.GPIO as gpio

#motor notations
left_motor_cw=31
left_motor_ccw=32
right_motor_cw=15
right_motor_ccw=16


gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(left_motor_cw,gpio.OUT)
gpio.setup(left_motor_ccw,gpio.OUT)
gpio.setup(right_motor_cw,gpio.OUT)
gpio.setup(right_motor_ccw,gpio.OUT)


def goforward():
    gpio.output(left_motor_cw,gpio.HIGH)
    gpio.output(right_motor_cw,gpio.HIGH)
    print('going forward')

def turnleft():
    gpio.output(right_motor_cw,gpio.HIGH)
    gpio.output(left_motor_cw,gpio.LOW)
    time.sleep(0.8)
    gpio.output(right_motor_cw,gpio.LOW)

def turnright():
    gpio.output(left_motor_cw,gpio.HIGH)
    gpio.output(right_motor_cw,gpio.LOW)
    time.sleep(0.8)
    gpio.outpu(left_motor_cw,gpio.LOW)

def gobackward():
    gpio.output(left_motor_ccw,gpio.HIGH)
    gpio.output(right_motor_ccw,gpio.HIGH)

def stop():
    gpio.output(left_motor_cw,gpio.LOW)
    gpio.output(left_motor_ccw,gpio.LOW)
    gpio.output(right_motor_cw,gpio.LOW)
    gpio.output(right_motor_ccw,gpio.LOW)

def checkanddriveright():
    while int(distance[-1][0]) < 30:
        stop()
        print(int(distance[-1][0]))
        turnleft()
        print('turn left didnt work trying again')
    print('turn left worked now going forward')
    goforward()

def checkanddriveleft():
    while int(distance[-1][1]) < 30:
        stop()
        print(int(distance[-1][1]))
        turnright()
        print('turn right didnt work trying again')
    print('turn right worked now going forward')
    goforward()      

# Define a function for the thread
def serial_monitor(iss):
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
                checkanddriveright()
            elif int(distance[-1][1]) < 30:
                stop()
                print(int(distance[-1][1]))
                checkanddriveleft()
        except KeyboardInterrupt:
            pass
        finally:
            gpio.cleanup()

distance=[]
try:
    _thread.start_new_thread(serial_monitor,(1,))
    _thread.start_new_thread(motor_control,(1,))
except KeyboardInterrupt:
    print ("Error: unable to start thread")
finally:
    gpio.cleanup()
while 1:
    pass
gpio.cleanup()

