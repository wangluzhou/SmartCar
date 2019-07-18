''''
Real Time Face Recogition
	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

'''

import cv2
import numpy as np
import os 
from preparation import recognize

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/Face_Recognition/trainer.yml')
cascadePath = "/home/pi/Face_Recognition/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX
threshold = 60    #set threshold to be 50

id = 0
names = ['None', 'Lord of awesomeness', 'tonytony']

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height
minW = 64
minH = 48

while True:

    ret, img = cam.read()     #read an image
    img = cv2.flip(img, 1) # Flip horizontally

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (minW, minH))

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)      # use rectangle() to draw a rectangle

        name = recognize(gray[y:y+h,x:x+w], threshold, names)
        
        cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xFF # Press 'ESC' for exiting video
    if k == 27:
        break

# clean up
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
