import cv2
import numpy as np
from math import inf

box_coordinates = []

# mouse callback function
def draw_rect(event, x, y, flags, param):
    global box_coordinates ,box2_coordinates

    if event == cv2.EVENT_LBUTTONDOWN:
        box_coordinates=[(x, y)] 
        box2_coordinates=[(x-100, y-100)] 

      
    elif event == cv2.EVENT_LBUTTONUP:
        box_coordinates.append((x, y)) 
        box2_coordinates.append((x+100, y+100))
        cv2.rectangle(img, (box_coordinates[0][0], box_coordinates[0][1]), 
        (box_coordinates[1][0], box_coordinates[1][1]), (0, 0, 255), 2)
        cv2.rectangle(img, (box2_coordinates[0][0], box2_coordinates[0][1]), 
        (box2_coordinates[1][0], box2_coordinates[1][1]), (124, 252, 0), 2)
        cv2.imshow("image", img) 


def MSE(bloc1,bloc2):
    N=bloc1.shape[0]
    M=bloc2.shape[1]
    




            
              
	
img = cv2.imread("image072.png")
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rect)  
img2 = cv2.imread("image092.png")
cv2.namedWindow('image')
cv2.rectangle(img2, (box_coordinates[0][0]-100, box_coordinates[0][1]-100), 
        (box_coordinates[1][0]+100, box_coordinates[1][1]+100), (0, 0, 255), 2)


while(True):
	cv2.imshow('image', img)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break
cv2.imshow('image2', img2) 
print(box_coordinates)
cv2.destroyAllWindows()

img1 = cv2.imread('image072.png')
grayImg1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# Cropping an image
bloc1 = grayImg1[box_coordinates[0][1]:box_coordinates[1][1], box_coordinates[0][0]:box_coordinates[1][0]] 
# Display cropped image
cv2.imshow("cropped", bloc1)
cv2.waitKey(0)
