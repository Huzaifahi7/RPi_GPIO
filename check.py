import RPi.GPIO as gpio
import time

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
    gpio.output(left_motor_cw,gpio.HIGH)
    gpio.output(right_motor_cw,gpio.HIGH)


def turnleft():
    gpio.output(right_motor_cw,gpio.HIGH)
    gpio.output(left_motor_cw,gpio.LOW)
    time.sleep(0.8)
    gpio.outpu(right_motor_cw,gpio.LOW)

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
try:

    stop()
    goforward()
    time.sleep(10)
    turnleft()
    time.sleep(10)
    stop()
except KeyboardInterrupt:
    pass
finally:
    gpio.cleanup()