
import _thread
import time
import serial


# Define a function for the thread
def serial_monitor():
    global line
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('ascii').rstrip()

def motor_control():
    while True:
        print(line)
        time.sleep(1)
line=0
try:
    _thread.start_new_thread(serial_monitor)
    _thread.start_new_thread(motor_control)
except:
    print ("Error: unable to start thread")

while 1:
    pass