#!/usr/bin/python
import sys
sys.path.append('/home/pi/Car.py')
sys.path.append('/home/pi/camshift.py')
import pylirc, time
import RPi.GPIO as GPIO
from Car import Car
from camshift import target_tracking

BtnPin  = 19
Gpin    = 5
Rpin    = 6
blocking = 0
def keysacn():
    val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == False:
        val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == True:
        time.sleep(0.01)
        val = GPIO.input(BtnPin)
        if val == True:
            GPIO.output(Rpin,1)
            while GPIO.input(BtnPin) == False:
                GPIO.output(Rpin,0)
        else:
            GPIO.output(Rpin,0)
            
def setup():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
        GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def IR(config):
        if config == 'KEY_CHANNEL':
                myCar = Car()
                myCar.up(50)
                print ('t_up')
        if config == 'KEY_NEXT':
                myCar = Car()
                myCar.stop()
                print ('t_stop')
        if config == 'KEY_PREVIOUS':
                myCar = Car()
                myCar.left(50)
                print ('t_left')
        if config == 'KEY_PLAYPAUSE':
                myCar = Car()
                myCar.right(50)
                print ('t_right')
        if config == 'KEY_VOLUMEUP':
                myCar = Car()
                myCar.down(50)
                print ('t_down')
        if config == 'KEY_NUMERIC_1':
                myCar = Car()
                myCar.tracking()
                print ('tracking')
        if config == 'KEY_NUMERIC_2':
                # Face recognition
                pass
        if config == 'KEY_NUMERIC_3':
                target_tracking()
                print ('Target tracking')
        if config == 'KEY_NUMERIC_4':
                # Destroy the system
                destroy()
        if config == 'KEY_NUMERIC_5':
            print("avoid")
            myCar = Car()
            myCar.avoid()


def loop():
    while True:
        s = pylirc.nextcode(1)  
        while(s):
            for (code) in s:
                myCar = Car()
                myCar.stop()
                print ('Command: ', code["config"])
                IR(code["config"])
                if(not blocking):
                    s = pylirc.nextcode(1)
                else:
                    s = []

def destroy():
    GPIO.cleanup()	
    pylirc.exit()

if __name__ == '__main__':
    setup()
##    keysacn()
    print("setup ok")
    pylirc.init("pylirc", "./conf", blocking)
    try:
        IR('KEY_NUMERIC_3')
    except KeyboardInterrupt:
        destroy()

