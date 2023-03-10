import cv2
import numpy as np
from math import inf

from matplotlib import pyplot as plt

box_coordinates = []


def MSE(bloc1, bloc2):
    block1, block2 = np.array(bloc1), np.array(bloc2)
    return np.square(np.subtract(block1, block2)).mean()


img1 = cv2.imread('images/image072.png')
img2 = cv2.imread('images/image092.png')

grayImg1 = cv2.cvtColor(img1, cv2.COLOR_RGB2YCrCb)[:, :, 0]
grayImg2 = cv2.cvtColor(img2, cv2.COLOR_RGB2YCrCb)[:, :, 0]

height = grayImg1.shape[0]
width = grayImg2.shape[1]

boxSize = 16
boxSize2 = 23
"""for i in range(0, width):
    for j in range(0, height):

        blocRouge = grayImg1[i:i + ((j + 1) * boxSize - j * boxSize),
                    j:j + ((i + 1) * boxSize - i * boxSize)]
        for i2 in range(j * boxSize - 7,
                        (j + 1) * boxSize + 7 - ((j + 1) * boxSize - j * boxSize)):
            for j2 in range(i * boxSize - 7,
                            (i + 1) * boxSize + 7 - ((i + 1) * boxSize - i * boxSize)):

                blocVert = grayImg2[i2:i2 + (j * boxSize - j * boxSize),
                           j2:j2 + ((i2 + 1) * boxSize - (j2 + 1) * boxSize)]

                loss = MSE(blocRouge, blocVert)
                if loss > 50:
                    cv2.rectangle(img1, (i * boxSize, j * boxSize), ((i + 1) * boxSize, (j + 1) * boxSize), (0, 0, 255),
                                  2)
                    cv2.rectangle(img2, (i * boxSize2, j * boxSize2), ((i + 1) * boxSize2, (j + 1) * boxSize2),
                                  (0, 255, 0), 2)"""

greens = []
reds = []
for i in range(0, height - boxSize, boxSize):  # colonne
    for j in range(0, width - boxSize, boxSize):  # ligne
        blocRouge = grayImg1[i:i + boxSize, j:j + boxSize]
        min1 = inf
        for i1 in range(max(0, i - 7), min(i + 7, height - boxSize)):
            for j1 in range(max(0, j - 7), min(j + 7, width - boxSize)):
                blocVert = grayImg2[i1:i1 + boxSize, j1:j1 + boxSize]

                loss = MSE(blocRouge, blocVert)
                if loss < min1:
                    min1 = loss
                    x1 = i1
                    x2 = j1

        if min1 > 50:
            # print(min1)
            greens.append((x2, x1))
            reds.append((i, j))

for i in range(len(greens)):
    cv2.rectangle(img2, (greens[i][0], greens[i][1]),
                  (greens[i][0] + boxSize, greens[i][1] + boxSize), (0, 255, 0), 2)

for i in range(len(reds)):
    cv2.rectangle(img1, (reds[i][0], reds[i][1]),
                  (reds[i][0] + boxSize, reds[i][1] + boxSize), (0, 0, 255), 2)

cv2.imshow('image1', img1)
cv2.imshow('image2', img2)

"""while True:
    cv2.imshow('image1', img1)
    cv2.imshow('image2', img2)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break"""

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
