import  RPi.GPIO as GPIO
import sys
import time
sys.path.append('/home/pi/camshift.py')



PWMA = 18
AIN1   =  22
AIN2   =  27

PWMB = 23
BIN1 = 25
BIN2 = 24

BtnPin  = 19
Gpin    = 5
Rpin    = 6

 
T_SensorRight = 26
T_SensorLeft  = 13

SensorRight = 16
SensorLeft  = 12

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

GPIO.setup(AIN2,GPIO.OUT)
GPIO.setup(AIN1,GPIO.OUT)
GPIO.setup(PWMA,GPIO.OUT)

GPIO.setup(BIN1,GPIO.OUT)
GPIO.setup(BIN2,GPIO.OUT)
GPIO.setup(PWMB,GPIO.OUT)

GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V) 
GPIO.setup(T_SensorRight,GPIO.IN)
GPIO.setup(T_SensorLeft,GPIO.IN)

GPIO.setup(SensorRight,GPIO.IN)
GPIO.setup(SensorLeft,GPIO.IN)

class Car(object):
    def __init__(self):
        Car.L_Motor= GPIO.PWM(PWMA,100)
        Car.L_Motor.start(0)

        Car.R_Motor = GPIO.PWM(PWMB,100)
        Car.R_Motor.start(0)

        
    def up(self,speed):
        Car.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        Car.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
    
    def down(self,speed):
        Car.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        Car.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1

    def left(self,speed):
        Car.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        Car.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1

    def right(self,speed):
        Car.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        Car.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1

    def stop(self):
        Car.L_Motor.ChangeDutyCycle(0)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,False) #AIN1

        Car.R_Motor.ChangeDutyCycle(0)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,False) #BIN1
        
    def tracking(self):
        try:
            while True:
                SR = GPIO.input(T_SensorRight)
                SL = GPIO.input(T_SensorLeft)
                if SL == False and SR == False:
                    print "t_up"
                    self.up(50)
                elif SL == True and SR ==False:
                    print "Left"
                    self.left(50)
                elif SL==False and SR ==True:
                    print "Right"
                    self.right(50)
                else:
                    self.stop()
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            self.stop()

    def avoid(self):
        try:
            while True:
                SR_2 = GPIO.input(SensorRight)
                SL_2 = GPIO.input(SensorLeft)
                if SL_2 and SR_2:
                    print("t_up")
                    self.up(50)
                elif not SR_2 and not SL_2:
                    print("back")
                    self.stop()
                    time.sleep(0.5)
                    self.down(50)
                    time.sleep(1.2)
                    self.left(50)
                    time.sleep(0.5)
                elif not SR_2:
                    print("Left")
                    self.left(50)
                    time.sleep(0.8)
                else:
                    print("Right")
                    self.right(50)
                    time.sleep(0.8)
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            GPIO.cleanup()
