import cv2
import numpy as np
import os 

def recognize(gray, threshold, names):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('/home/pi/Face_Recognition/trainer.yml')

    id, distance = recognizer.predict(gray)
    if (distance < threshold):
        name = names[id]
        rate = 1 - float(distance)/float(threshold)
        confidence = "{0}%".format(round(rate * 100))
    else:
        name = "tonytony"
        confidence = '{0}%'.format(0)

    return name
     

def shift(frame, roiHist, roiBox, termination):
    # convert the current frame to the HSV color space
    # and perform mean shift
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    backProj = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)
    
    # apply cam shift to the back projection, convert the
    # points to a bounding box, and then draw them
    (r, roiBox) = cv2.CamShift(backProj, roiBox, termination)
    pts = np.int0(cv2.boxPoints(r))
    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
    
    return frame, roiBox
    
    
def getRoiBox(orig, roiPts):      
    # determine the top-left and bottom-right points
    roiPts = np.array(roiPts)
    s = roiPts.sum(axis = 1)
    tl = roiPts[np.argmin(s)]
    br = roiPts[np.argmax(s)]
         
    # grab the ROI for the bounding box and convert it
    # to the HSV color space
    roi = orig[tl[1]:br[1], tl[0]:br[0]]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # compute a HSV histogram for the ROI and store the
    # bounding box
    roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
    roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
    roiBox = (tl[0], tl[1], br[0], br[1])
    
    return roiHist, roiBox