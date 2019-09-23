#!/usr/bin/env python
# coding: utf-8

import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

# load the image, clone it for output, and then convert it to grayscale
img = cv2.imread(args["image"])
output = img.copy()
output2 = img.copy()

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# detect circles in the image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100, param1=50,param2=60,minRadius=150,maxRadius=170)
radius = circles[0][0][2]

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    circle = cv2.circle(gray,(i[0],i[1]),i[2],(0, 255, 0),5)
    # draw the center of the circle
    cv2.circle(gray,(i[0],i[1]),2,(0, 255, 0),10)
#plt.imshow(gray)
cv2.line(gray,(i[0],i[1]),(math.ceil(i[0]+radius),i[1]),(0,255,0),5)
#plt.imshow(gray)


mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

rect = (80, 80, 350, 350)


cv2.grabCut(img,mask,rect,bgdModel,fgdModel,3,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]
img[img > 0] = 255 
#plt.imshow(img)


#inner contour

gray3 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_, threshold = cv2.threshold(gray3, 250, 255, cv2.THRESH_BINARY)
_, contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 65000.0:
        print(area)
        cnt_array = cnt
        approx = cv2.approxPolyDP(cnt, 0.002*cv2.arcLength(cnt, True), True)
        cnts = cv2.drawContours(output, [approx], 0, (255, 0, 0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1]        
        hull = cv2.convexHull(cnt)
        #hull = cv2.convexHull(cnt,returnPoints = False)
        #defects = cv2.convexityDefects(cnt,hull)
        #cv2.drawContours(output, [hull], 0, (0, 0, 255), 1) 
        
#plt.imshow(output)

rect = cv2.minAreaRect(cnt_array)
box = cv2.boxPoints(rect)
box = np.int0(box)
im = cv2.drawContours(img,[box],0,(0,0,255),2)
#plt.imshow(im)

angle = rect[2]

if abs(angle) < 20:
	angle = -90 + angle


b = box[2]+box[3]
c1 = math.ceil(b[0]/2)
c2 = math.ceil(b[1]/2)


circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    circle = cv2.circle(output2,(i[0],i[1]),i[2],(255, 0, 0),5)
    # draw the center of the circle
    cv2.circle(output2,(i[0],i[1]),2,(255, 0, 0),10)

cv2.line(output2,(i[0],i[1]),(math.ceil(i[0]+radius),i[1]),(255, 0, 0),5)	
#cv2.line(output2,(i[0],i[1]),(c1, c2),(0,255,0),5)
plt.imshow(output2)
plt.xticks([]), plt.yticks([]) 
plt.show()
file1 = open("output.txt", "w")
file1.write("The rotation angle of an image called " + str(args["image"]) + " is " + str(angle))
file1.close()







