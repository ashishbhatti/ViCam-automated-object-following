'''
Author: Ashish Kumar
Date: December 09, 2023

Object detection module: Defines Object Detection function using Haar Cascades
Haar Cascades refer to the application of the Viola Jones method in a cascade structure.
The cascade is a series of classifiers and at each stage, the image region is tested
against a specific classifier. If a region passes a stage, it moves on to the next,
increasing the likelihood that the region contains the object of interest.
The cascaded structure helps in quickly discarding background regions and focusing 
computational resources on potential object regions.
'''

import cv2

def findObjects(img, objectCascade, scaleFactor = 1.1, minNeighbors = 4):
    '''
    Finds objects using the haarcascade file
    Args:
        img: Image in which the objects needs to be found
        objectCascade: Object Cascade created with Cascade Classifier
        scaleFactor: how much the image size is reduced at each image scale
        minNeighbors: how many neighbors each rectangle should have to accept as valid
    Return:
        imgObject: image with the rectangles drawn 
        objectsOut: sorted list of all bounding boxs and their areaa 
    '''
    imgObject = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                  # optional
    
    # find objects in image
    # image, scale factor, min neighbors (changing these speed-accuracy tradeoff)
    objects = objectCascade.detectMultiScale(imgGray, scaleFactor, minNeighbors)
    # list to store bounding box and area, to later find the biggest
    objectsOut = []                                                                  

    # drawing bounding box over faces
    for (x,y,w,h) in objects:
        cv2.rectangle(imgObject, (x,y), (x+w, y+h), (255,0,255), 2)
        objectsOut.append([[x,y,w,h], w*h])

    objectsOut = sorted(objectsOut, key = lambda x:x[1], reverse = True)

    return imgObject, objectsOut


def main():
    img = cv2.imread("test.jpg")
    img = cv2.resize(img, None, fx=0.5, fy=0.5)
    
    # import the file which has information of detection, here face cascade but can by anything
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    imgObject, objects = findObjects(img, faceCascade)
    
    cv2.imshow("Output",imgObject)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()