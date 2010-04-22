#!/usr/bin/python
"""
This program is demonstration for face and object detection using haar-like features.
The program finds faces in a camera image or video stream and displays a red box around them.

Original C implementation by:  ?
Python implementation by: Roman Stanchak, James Bowman
"""
import sys
from opencv import cv
from optparse import OptionParser

# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned 
# for accurate yet slow object detection. For a faster operation on real video 
# images the settings are: 
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
# min_size=<minimum possible face size

min_size = (20, 20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0
cascadeDefault = "./haarcascade_frontalface_alt.xml"

def detectFaces(img):
    # load the adaboost model
    cascade = cv.Load(cascadeDefault)
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
			       cv.Round (img.height / image_scale)), 8, 1)

    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

    if(cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
#        print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        faceList = []
        if faces:
            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the 
                # bounding box of each face and convert it to two CvPoints
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                # adding a rectangle for testing only
                cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
                faceList= faceList + [(pt1, pt2)]
            
        return faceList    
    
def recognizeFaces(image, faces):
    
    faceLabels = []
    for ((x1,y1),(x2,y2)) in faces:
        faceLabels += [((x1,y1),(x2,y2),"Chuck")]
        
    return faceLabels
        
if __name__ == '__main__':

    input_name = "Chuck1.jpg"

    cv.NamedWindow("result", 1)

    image = cv.LoadImage(input_name, 1)
    faces = detectFaces(image) #, cascade)
    faceLabels = recognizeFaces(image,faces)
    print faceLabels
    cv.ShowImage("result", image)
    cv.WaitKey(0)
    
    cv.DestroyWindow("result")
