from PIL import Image
import numpy as np

# Open an image
image = Image.open('random.jpg')
print (type(image))
image.show()

# Get the size of the image
width, height = image.size
print (f'Width: {width} / Height: {height}')

# Get the mode of the image
mode = image.mode
print (f'This image is: {mode}')

# Access the pixels of the image
pix = image.load()
print (type(pix))
pix_1 = pix[780, 400]
print (pix_1)
print (f'The R value is: {pix_1[0]}.', end=' ')
print (f'The G value is: {pix_1[1]}.', end=' ')
print (f'The B value is: {pix_1[2]}.') 

# ****************************************************** Image Binarization with PIL *******************************************
# Convert an image from RGB to grayscale: L = R * 299/1000 + G * 587/1000 + B * 114/1000

# Open an image
image = Image.open('random.jpg')
image_gray = image.convert(mode='L')
pix_gray = image_gray.load()
print (pix_gray[780, 400])
image_gray.show()

# Method 1: Define a binarization function
def binarize(img, thresh=100):

    width,height=img.size

    # Loop through pixels 
    for x in range(width):
        for y in range(height):

            # If intensity less than threshold, assign white
            if img.getpixel((x,y)) < thresh:
                img.putpixel((x,y),0)
                
            # If intensity greater than threshold, assign black 
            else:
                img.putpixel((x,y),255)
                
    return img

bin_image=binarize(image_gray) 
bin_image.show()
bin_image.save('binary_random1.png')

image2 = Image.open('binary_random1.png').convert('L')
image2_np = np.array(image2).astype(np.uint8)
print (image2_np.shape)
print (np.unique(image2_np))

# Method 2: Using point function
# Convert to bi (white and black) with a threshold of 100
threshold = 127
image_bw = image_gray.point(lambda x: 255 if x > threshold else 0)
image_bw.show()
image_bw.save('binary_random2.png')

image3 = Image.open('binary_random2.png').convert('L')
image3_np = np.array(image3).astype(np.uint8)
print (image3_np.shape)
print (np.unique(image3_np))

# ************************************************* Opencv *******************************************************

import cv2

img_rgb = cv2.imread('random.jpg', cv2.IMREAD_COLOR)
print (type(img_rgb))
print (img_rgb.shape)
print (img_rgb[400, 780, :])

img_gray = cv2.imread('random.jpg', cv2.IMREAD_GRAYSCALE)
print (img_gray.shape)
print (img_gray[400, 780])

threshold = 127
_, img_bw = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)
print (img_bw[400, 780])
print (np.unique(img_bw))
cv2.imshow('binary image', img_bw)
cv2.waitKey(0)

otsu_thresh, img_bw_otsu = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_OTSU)
print (otsu_thresh)
print (img_bw_otsu[400, 780])
print (np.unique(img_bw_otsu))
cv2.imshow('binary image with otsu', img_bw_otsu)
cv2.waitKey(0) 