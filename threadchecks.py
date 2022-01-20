
import _thread
from operator import length_hint
import time
import serial


# Define a function for the thread
def serial_monitor(iss):
    global line,ls
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if len(ls)>10:
            ls=[ls[-1]]
        if ser.in_waiting > 0:
            line = ser.readline().decode('ascii').rstrip()
            ls.append(line)


def motor_control(ssi):
    while True:
        print(ls[-1],type(ls[-1]))
        time.sleep(.1)

ls=[]
line=0
try:
    _thread.start_new_thread(serial_monitor,(1,))
    _thread.start_new_thread(motor_control,(1,))
except:
    print ("Error: unable to start thread")

while 1:
    pass

