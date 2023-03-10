import cv2
import numpy as np
from math import inf
from matplotlib import pyplot as plt

box_coordinates = []

# Fonction qui calcul
def MSE(bloc1, bloc2):
    block1, block2 = np.array(bloc1), np.array(bloc2)
    return np.square(np.subtract(block1, block2)).mean()


img1 = cv2.imread('image072.png')
img2 = cv2.imread('image092.png')

height = img1.shape[0]
width = img1.shape[1]

grayImg1 = cv2.cvtColor(img1, cv2.COLOR_RGB2YCrCb)[:, :, 0]
grayImg2 = cv2.cvtColor(img2, cv2.COLOR_RGB2YCrCb)[:, :, 0]

for i in range(0, width-1):
    for j in range(0, height-1):
        """bloc1 = grayImg1[i:i, j:j]
        bloc2 = grayImg2[i:i + (i - j), j:j + (i - j)]"""
        cv2.rectangle(img1, (i * 32, j * 32), ((i+1)*32, (j+1) * 32), (0, 0, 255), 2)

img2 = cv2.imread('image092.png')

height = img1.shape[0]
width = img1.shape[1]

for i in range(0, width-1):
    for j in range(0, height-1):
        """bloc1 = grayImg1[i:i, j:j]
        bloc2 = grayImg2[i:i + (i - j), j:j + (i - j)]"""
        cv2.rectangle(img1, (i * 32, j * 32), ((i+1)*32, (j+1) * 32), (0, 0, 255), 2)

cv2.imshow('image', img1)
# cv2.imshow('image', img2)

while True:
    cv2.imshow('image', img1)
    # cv2.imshow('image', img2)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

# cv2.destroyAllWindows()


# deviser en blocs de 32 l'image 1

# deviser en blocs de 32 l'image 2

# researching similarity between every bloc
"""min = inf
for i in range(box_coordinates[0][1] - 100,
               box_coordinates[1][1] + 100 - (box_coordinates[1][1] - box_coordinates[0][1])):
    for j in range(box_coordinates[0][0] - 100,
                   box_coordinates[1][0] + 100 - (box_coordinates[1][0] - box_coordinates[0][0])):
        block2 = grayImg2[i:i + (box_coordinates[1][1] - box_coordinates[0][1]),
                 j:j + (box_coordinates[1][0] - box_coordinates[0][0])]
        loss = MSE(bloc1, block2)
        if loss < min:
            min = loss
            bloc = block2"""

# Display cropped image

"""plt.figure(figsize=(12, 8))
plt.subplot(1, 4, 1)
plt.title('bloc rogné')
plt.imshow(bloc1, cmap='gray')

plt.subplot(1, 4, 2)
plt.title('bloc de recherche')
plt.imshow(bloc2, cmap='gray')

plt.subplot(1, 4, 3)
plt.title('le bloc le plus similaire dans l''image 2')
plt.imshow(bloc, cmap='gray')

plt.show()"""

cv2.waitKey(0)
