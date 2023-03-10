import qrcode
from PIL import Image
import numpy as np
import cv2
import itertools
#from pyzbar.pyzbar import decode
import warnings
import pyqrcode
warnings.filterwarnings("ignore")

def encode(image, file_name='compressed_image.txt', bits=15):

    count_list = []
    count = 0
    prev = None
    fimage = image.flatten()
    size = 2**(bits+1) - 2**bits #32768 = 8000H
    
    for pixel in fimage:
        
        if prev == None:
            prev = pixel 
            count += 1
        else:
            if prev != pixel:
                if count >= 3:
                    count_list.append((size+count, [prev]))
                else:
                    if count_list == []:
                        count_list.append((count, [prev]*count))
                    else: 
                        c, color = count_list[-1]
                        if c > size:
                            count_list.append((count, [prev]*count))
                        else:
                            if c+count <= (2**bits)-1:
                                count_list[-1] = (c+count, color+[prev]*count)
                            else:
                                count_list.append((count, [prev]*count))
                prev = pixel
                count = 1
            else:
                if count < (2**bits)-1:
                    count += 1                    
                else:
                    count_list.append((size+count, [prev]))
                    prev = pixel
                    count = 1

    if count >= 3:
        count_list.append((size+count, [prev]))
    else:
        c, color = count_list[-1]
        if c > size:
            count_list.append((count, [prev]*count))
        else:
            if c+count <= (2**bits)-1:
                count_list[-1] = (c+count, color+[prev]*count)
            else:
                count_list.append((count, [prev]*count))

    # Hexa encoding
    with open(file_name,"w") as file:
        hexa_encoded = "".join(map(lambda x: "{0:04x}".format(x[0])+"".join(map(lambda y: "{0:02x}".format(y), x[1])), count_list))
        """ hexa_encoded = ""
        for count, colors in count_list:
            hexa_encoded += "{0:04x}".format(count)
            for color in colors:
                hexa_encoded += "{0:02x}".format(color) """
        file.write(hexa_encoded)
        file.close()

    # Compression rate
    rate = (1-(len(hexa_encoded)/2)/len(fimage))*100
    
    return hexa_encoded, rate

def decode(height, width, file_name, bits=15):

    # Read the entire code from the file
    with open(file_name, "r") as file:
        code = file.readlines()[0]
        
    # Loop through the code and get the color of the pixels
    size = 2**(bits+1) - 2**bits 
    i = 0
    data = []
    while i < len(code):
        count = code[i:i+4]
        count = int(count, 16)
        i += 4
        if count > size: 
            # Here the color is repeated 3 times or more
            count -= size
            color = code[i:i+2]
            color = int(color, 16)            
            data += [color]*count
            i += 2
        else: 
            # Here each color is repeated less than 3 times
            color_seq = code[i:i+count*2]
            colors = [int(color_seq[idx:idx+2], 16) for idx in range(0, len(color_seq), 2)]
            data += colors
            i += count*2

    image = np.zeros((height, width)).astype(np.uint8)
    for k, (i, j) in enumerate(itertools.product(range(height), range(width))):
        image[i, j] = data[k]

    return image



image1_np = np.array([[0, 1, 0, 1, 0, 1], 
                    [1, 0, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0], 
                    [0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0]])*255

image2_np = np.array([[0, 0, 0, 1, 1, 1], 
                    [1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1],
                    [0, 0, 0, 1, 1, 1], 
                    [1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1]])*255

image3_np = np.array([[0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1], 
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0]])*255

encoded, rate = encode(image1_np, file_name='compressed1.txt', bits=15)
print (f'Compression rate :{rate:.02f}%') # 1- 38/36 = -5.56%
image = decode(height=6, width=6, file_name='compressed1.txt', bits=15)
# This has to be equal to 0
error_rate = np.count_nonzero(image - image1_np)
print (f'Error Rate: {error_rate}') 

encoded, rate = encode(image2_np, file_name='compressed2.txt', bits=15)
print (f'Compression rate :{rate:.02f}%') # 1- 24/36 = 33.33 %
image = decode(height=6, width=6, file_name='compressed2.txt', bits=15)
# This has to be equal to 0
error_rate = np.count_nonzero(image - image2_np)
print (f'Error Rate: {error_rate}') 

encoded, rate = encode(image3_np, file_name='compressed3.txt', bits=15)
print (f'Compression rate :{rate:.02f}%') # 1- 9/36 = 75.00 %
image = decode(height=6, width=6, file_name='compressed3.txt', bits=15)
# This has to be equal to 0
error_rate = np.count_nonzero(image - image3_np)
print (f'Error Rate: {error_rate}')


img_gray = cv2.imread('iglogo.jpeg', cv2.IMREAD_GRAYSCALE)
_, img_bw = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
cv2.imwrite('cig.png', img_bw)
height, width = img_bw.shape # 787x444 = 349428
encoded, rate = encode(img_bw, file_name='ig_compressed.txt', bits=15)
print (f'Compression rate :{rate:.02f}%') # 1- 4292/349428 = 98.77%
image = decode(height, width, file_name='ig_compressed.txt', bits=15)
compressed_image = Image.fromarray(image, mode='L')
compressed_image.show()
compressed_image.save('cig.png')
# This has to be equal to 0
error_rate = np.count_nonzero(image - img_bw)
print (f'Error Rate: {error_rate}') 

img_gray = cv2.imread('fblogo.jpeg', cv2.IMREAD_GRAYSCALE)
_, img_bw = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
cv2.imwrite('cfb.png', img_bw)
height, width = img_bw.shape # 512x480 = 245760
encoded, rate = encode(img_bw, file_name='fb_compressed.txt', bits=15)
print (f'Compression rate :{rate:.02f}%') # 1- 22927/245760 = 90.67%
image = decode(height, width, file_name='fb_compressed.txt', bits=15)
compressed_image = Image.fromarray(image, mode='L')
compressed_image.show()
compressed_image.save('cfb.png')
# This has to be equal to 0
error_rate = np.count_nonzero(image - img_bw)
print (f'Error Rate: {error_rate}')

##################################################################################

with open('fb_compressed.txt') as f:
    lines = f.readlines()
    textCfb = lines[0]
    qr1 = qrcode.make(textCfb)
    qr1.save('FBQRcode.png')
    qr1.show()

with open('ig_compressed.txt') as f:
    lines2 = f.readlines()
    textCig = lines2[0]
    qr2 = qrcode.make(textCig)
    qr2.save('IGQRcode.png')
    qr2.show()

# une fonction qui scan l'image qr code et retourne son résultat
def returnQRcodeResult(imagename):
    img = cv2.imread(imagename)
    detector = cv2.QRCodeDetector()
    val,b,c = detector.detectAndDecode(img)
    return val

    """for result in decode(img):
        print(result.data.decode('utf-8'))
        return result.data.decode('utf-8')"""

# scan du qr et obtention du resultat
imageQR1 = returnQRcodeResult('/Users/rayanpicso/Desktop/MIV/Multimédia/FBQRcode.png')
imageQR2 = returnQRcodeResult('/Users/rayanpicso/Desktop/MIV/Multimédia/IGQRcode.png')

"""img1 = decode(50,50,'fb_compressed.txt')
img1Decompressed = Image.fromarray(img1, mode='L')
img2 = decode(25,25,'ig_compressed.txt')
img2Decompressed = Image.fromarray(img2, mode='L')

img1Decompressed.show()
img2Decompressed.show()"""







