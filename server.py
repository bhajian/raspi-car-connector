#!/usr/bin/env python
import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
from time import ctime          # Import necessary modules
import websocket
import thread
import time

ctrl_cmd = ['car/goForward', 'car/goBackward', 'car/turnLeft/coarse', 'car/turnRight/coarse', 'car/stop', 'system/cpu_temp', 'car/home', 'car/distance', 'camera/right', 'camera/left', 'camera/up', 'camera/down', 'camera/home', 'car/setSpeed/', 'car/turn/angle/', 'car/forward/', 'car/backward/']

video_dir.setup()
car_dir.setup()
motor.setup()     # Initialize the Raspberry Pi GPIO connected to the DC motor.
video_dir.home_x_y()
car_dir.home()

def on_message(ws, data):
    print data
    # Analyze the command received and control the car accordingly.
    #if not data:

    if data == ctrl_cmd[0]:
        print 'motor moving forward'
        motor.forward()
    elif data == ctrl_cmd[1]:
        print 'recv backward cmd'
        motor.backward()
    elif data == ctrl_cmd[2]:
        print 'recv left cmd'
        car_dir.turn_left()
    elif data == ctrl_cmd[3]:
        print 'recv right cmd'
        car_dir.turn_right()
    elif data == ctrl_cmd[6]:
        print 'recv home cmd'
        car_dir.home()
    elif data == ctrl_cmd[4]:
        print 'recv stop cmd'
        motor.ctrl(0)
    elif data == ctrl_cmd[5]:
        print 'read cpu temp...'
        temp = cpu_temp.read()
        ws.send('[%s] %0.2f' % (ctime(), temp))
    elif data == ctrl_cmd[8]:
        print 'recv x+ cmd'
        video_dir.move_increase_x()
    elif data == ctrl_cmd[9]:
        print 'recv x- cmd'
        video_dir.move_decrease_x()
    elif data == ctrl_cmd[10]:
        print 'recv y+ cmd'
        video_dir.move_increase_y()
    elif data == ctrl_cmd[11]:
        print 'recv y- cmd'
        video_dir.move_decrease_y()
    elif data == ctrl_cmd[12]:
        print 'home_x_y'
        video_dir.home_x_y()
    elif data[0:12] == ctrl_cmd[13]:     # Change the speed
        print data
        numLen = len(data) - len('car/setSpeed/')
        if numLen == 1 or numLen == 2 or numLen == 3:
            tmp = data[-numLen:]
        #    print 'tmp(str) = %s' % tmp
            spd = int(tmp)
        #    print 'spd(int) = %d' % spd
            if spd < 24:
                spd = 24
        motor.setSpeed(spd)
    elif data[0:14] == ctrl_cmd[14]:	#Turning Angle
        #print 'data =', data
        numLen = len(data) - len('car/turn/angle/')
        if numLen == 1 or numLen == 2 or numLen == 3:
            angle = data[-numLen:]
        try:
            angle = int(angle)
            car_dir.turn(angle)
        except:
            print 'Error: angle =', angle
    elif data[0:11] == ctrl_cmd[15]:
        numLen = len(data) - len('car/forward/')
        if numLen == 1 or numLen == 2 or numLen == 3:
            spd = data[-numLen:]
        #spd = 30
        try:
            spd = int(spd)
            motor.forward(spd)
        except:
            print 'Error speed =', spd
    elif data[0:12] == ctrl_cmd[16]:
        print 'data =', data
        numLen = len(data) - len('car/backward/')
        if numLen == 1 or numLen == 2 or numLen == 3:
            spd = data[-numLen:]
        #spd = data.split('=')[1]
        try:
            spd = int(spd)
            motor.backward(spd)
        except:
            print 'ERROR, speed =', spd

    else:
        print 'Command Error! Cannot recognize command: ' + data




def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        for i in range(30000):
            temp = cpu_temp.read()
            ws.send('[%s] %0.2f' % (ctime(), temp))
            time.sleep(1)
        time.sleep(1)
        ws.close()
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://behnam.mybluemix.net/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    ws.run_forever()
