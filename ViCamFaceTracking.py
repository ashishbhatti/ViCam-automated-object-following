'''
Author: Ashish Kumar
Date: December 10, 2023

This file contains the neccessary functions to implement object tracking.
The code implements face tracking.
'''


import cv2
import ObjectDetectionModule as odm
import SerialModule as sm
import numpy as np
import time

# parameters for camera
frameWidth = 640
frameHeight = 480

# uncomment for CSI camera
# flip = 2
# camset = 

cap = cv2.VideoCapture(1)                                    # uncomment for webcam     

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# previous pid errors initially
perrorLR, perrorUD = 0, 0                                    # Left-Right, Up-Down
perrorYR, perrorPR = 0, 0                                    # Yaw-Rate, Pitch-Rate


def findCenter(imgObject, objects):
    '''
    Finds the center of the bounding box with highest area, marks it and
    draws error lines.
    Args:
        imgObject: image read using VideoCapture().read()
        objects: sorted list of properties ([bbox, area]) of all bounding boxes 
    Returns:
        cx: (int) center x coordinate
        cy: (int) center y coordinate
        imgObject: same image with center and error lines drawn
    '''
    cx, cy = -1, -1                                          # if no object found
    if len(objects) != 0:
        x,y,w,h = objects[0][0]                              # bbox with highest area
        cx = x + w //2
        cy = y + h // 2
        cv2.circle(imgObject, (cx,cy), 2, (0,255,0), cv2.FILLED)

        # visually show how far from center
        ih, iw, ic = imgObject.shape
        cv2.line(imgObject, (iw//2, cy), (cx, cy), (0,255,0), 1)    # horizontal line
        cv2.line(imgObject, (cx, ih//2), (cx, cy), (0,255,0), 1)    # vertical line

    return cx, cy, imgObject


def trackObjectAngles(cx, cy, w, h):
    '''
    Tracks a point cx, cy provided. This means it calculates error from
    center lines. Usea PID to compute yaw and pitch angles. Returns the angles
    Args:
        cx: (int) the x-coordinate of point to track
        cy: (int) the y-coordinate of point to follow
        w: (int) width of the frame
        h: (int) height of the frame
    Returns:
        posX: (int) yaw angle 
        posY: (int) pitch angle
    '''
    global perrorLR, perrorUD

    # pid paramaters, only p and d
    kLR = [0.6, 0.1]
    kUD = [0.6, 0.1]

    if cx != -1:

        # left and right
        errorLR = w//2 - cx
        posX = kLR[0]*errorLR + kLR[1]*(errorLR - perrorLR)         # PD control output for yaw
        posX = int(np.interp(posX, [-w//2, w//2], [20, 160]))       # mapping pid control output to servo acceptable answer
        perrorLR = errorLR                                          # update error

        # up and down
        errorUD = h//2 - cy
        posY = kUD[0]*errorUD + kUD[1]*(errorUD - perrorUD)         # PD control output for pitch
        posY = int(np.interp(posY, [-h//2, h//2], [20, 160]))       # mapping pid control output to servo acceptable answer
        perrorUD = errorUD                                          # update error

        # sm.sendData(ser, [posX, posY], 3)
        return posX, posY
    
    else: 
        return None, None


def trackObjectRotationRates(cx, cy, w, h):
    '''
    Tracks a point cx, cy provided. This means it calculates error from
    center lines. Usea PID to compute yaw and pitch roll rates. Returns the rates.
    Args:
        cx: (int) the x-coordinate of point to track
        cy: (int) the y-coordinate of point to follow
        w: (int) width of the frame
        h: (int) height of the frame
    Returns:
        rateX: (int) yaw rate
        rateY: (int) pitch rate
    '''
    global perrorYR, perrorPR

    # pid paramaters, only p and d
    pidY = [0.4, 0.4, 0]
    pidP = [0.4, 0.4, 0]

    if cx != -1:

        # yaw rate
        errorYR = cx - w//2
        speedY = pidY[0]*errorYR + pidY[1]*(errorYR - perrorYR)         # PD control output for yaw rate
        yawRate = int(np.clip(speedY, -100, 100))                       # clipping pid control output between a range
        perrorYR = errorYR                                             # update error

        # pitch rate
        errorPR = cy - h//2
        speedP = pidP[0]*errorPR + pidP[1]*(errorPR - perrorPR)         # PD control output for yaw rate
        pitchRate = int(np.clip(speedP, -100, 100))                       # clipping pid control output between a range
        perrorYR = errorYR

        # sm.sendData(ser, [posX, posY], 3)
        return yawRate, pitchRate
    
    else: 
        return None, None


def mainNoSerial():
    '''
    TESTER FUNCTION: prints angles on console, instead of sending to serial port.
    HOW TO TEST: main in case if we don't want to write to serial.
    '''
    while True:
        success, img = cap.read()
        img = cv2.resize(img, (0,0), None, 0.3,0.3)
    
        # find the objects in image
        imgObject, objects = odm.findObjects(img, faceCascade, 1.08, 10)
        cx, cy, imgObject = findCenter(imgObject, objects)
        
        h,w,c = imgObject.shape
        cv2.line(imgObject, (w//2,0), (w//2,h), (255,0,255),1)
        cv2.line(imgObject, (0, h//2), (w,h//2), (255,0,255),1)
        
        # yawValue, pitchValue = trackObjectAngles(cx, cy, w, h)
        yawValue, pitchValue = trackObjectRotationRates(cx, cy, w, h)
    
        if (yawValue != None):
            print(yawValue, pitchValue, sep=", ")
    
    
        cv2.imshow("Image", imgObject)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("90, 90")
            break


def main():
    '''
    Main in case writing to serial port. Check the serial port number.
    '''
    ser = sm.initConnection('COM3', 9600)                     # cross check the COM port
    while True:
        success, img = cap.read()
        img = cv2.resize(img, (0,0), None, 0.5,0.5)
    
        # find the objects in image
        imgObject, objects = odm.findObjects(img, faceCascade, 1.08, 10)
        cx, cy, imgObject = findCenter(imgObject, objects)
        
        h,w,c = imgObject.shape
        cv2.line(imgObject, (w//2,0), (w//2,h), (255,0,255),1)
        cv2.line(imgObject, (0, h//2), (w,h//2), (255,0,255),1)
        
        yawValue, pitchValue = trackObjectAngles(cx, cy, w, h)
        # yawValue, pitchValue = trackObjectRotationRates(cx, cy, w, h)
    
        if (yawValue != None):
            sm.sendData(ser, [yawValue, pitchValue], 3)
    
    
        cv2.imshow("Image", imgObject)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sm.sendData(ser, [90,90], 3)
            break


if __name__ == "__main__":
    # mainNoSerial()
    main()                                                  # uncomment if sending to serial