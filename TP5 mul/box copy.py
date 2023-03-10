import cv2
import numpy as np
import math

box_coordinates = []

# mouse callback function
def draw_rect(event, x, y, flags, param):
    global box_coordinates 
    if event == cv2.EVENT_LBUTTONDOWN:
        box_coordinates=[(x, y)] 

    elif event == cv2.EVENT_LBUTTONUP:
        box_coordinates.append((x, y)) 
        cv2.rectangle(img, (box_coordinates[0][0], box_coordinates[0][1]), 
        (box_coordinates[1][0], box_coordinates[1][1]), (0, 0, 255), 2)
        cv2.imshow("image", img) 


img = cv2.imread("image072.png")
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rect)

while(True):
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
print(box_coordinates)
cv2.destroyAllWindows()


def MSE(bloc1,bloc2):
    
    M = bloc1.shape[1]
    N = bloc1.shape[0]
    sum = 0
    for x in range(N):
        for y in range(M):
            sum+=math.pow((bloc1[x,y] - bloc2[x,y]),2)
    return sum/(M*N)

img1 = cv2.imread('image072.png')
grayImg1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# Cropping an image
bloc1 = grayImg1[box_coordinates[0][1]:box_coordinates[1][1], box_coordinates[0][0]:box_coordinates[1][0]]
img2 = cv2.imread('image092.png')
grayImg2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
Searchzone = grayImg2[box_coordinates[0][1]-100:box_coordinates[1][1]+100, box_coordinates[0][0]-100:box_coordinates[1][0]+100]
# Display cropped image
cv2.rectangle(img2, (box_coordinates[0][0], box_coordinates[0][1]), 
        (box_coordinates[1][0], box_coordinates[1][1]), (0, 0, 255), 2)
cv2.rectangle(img2, (box_coordinates[0][0]-100, box_coordinates[0][1]-100), 
        (box_coordinates[1][0]+100, box_coordinates[1][1]+100), (0, 255, 0), 2)
cv2.imshow("cropped", bloc1)
cv2.imshow("cropped1", Searchzone)
cv2.waitKey(0)


def findSim(bloc1,Searchzone):
    X = Searchzone.shape[0] 
    Y = Searchzone.shape[1]
    MIN = math.inf
    print(X)
    for y in range(Y-bloc1.shape[1]):
        for x in range(X-bloc1.shape[0]):
            if MSE(bloc1,Searchzone[x:x+bloc1.shape[0],y:y+bloc1.shape[1]]) < MIN:
                MIN = MSE(bloc1,Searchzone[x:x+bloc1.shape[0],y:y+bloc1.shape[1]])
    return MIN

print(findSim(bloc1,Searchzone))

