import argparse
import itertools
import os
import pickle

import cv2
# module importés:
import numpy as np
import PIL
from PIL import Image
import base64

DICTIONARY_SIZE = 256


# used functions:

def binFileToImg(binaryFile):
    w, h = 120, 120

    with open('binary_image1.bin', mode='rb') as f:
        d = np.fromfile(f, dtype=np.uint8, count=w * h).reshape(h, w)

        image = Image.fromarray(d)

    if binaryFile == 'binary_image1.bin':
        image.save('image1.png')
    else:
        image.save('image2.png')

    image.show()


def convertImgToArray2(image):
    img_data = PIL.Image.open(image)
    img_arr2 = np.array(img_data)
    return img_arr2


def convertImgToStr(imageFile, text_file):
    with open(imageFile, "rb") as img2str:
        converted_string = base64.b64encode(img2str.read())

    with open(text_file, "wb") as file:
        file.write(converted_string)

    return imageFile, text_file


def writeArray(array):
    with open('image1.txt', "w") as file:
        merged = list(itertools.chain.from_iterable(array))
        string = "".join(str(s) for s in merged)
        file.write(string)


# comp and decomp functions

def compress(input):
    pxImg = cv2.imread(input, cv2.IMREAD_COLOR)
    imgGray = cv2.imread(input, cv2.IMREAD_GRAYSCALE)
    threshold = 127
    _, img_bw = cv2.threshold(imgGray, threshold, 255, cv2.THRESH_BINARY)
    o_thresh, img_otsu = cv2.threshold(imgGray, threshold, 255, cv2.THRESH_BINARY)
    
    img = np.array(img_otsu)
    img = img.flatten()
    img1 = []

    for i in range(len(img)):
        img1.append(str(img[i]).zfill(3))

    # la chaine
    inp = ''.join(img1)

    global DICTIONARY_SIZE
    dictionary = {}
    result = []
    temp = ""

    for i in range(0, DICTIONARY_SIZE):
        dictionary[str(i).zfill(3)] = i
    # initializer le i
    i = 0

    # lire la chaine
    while i < len(inp):
        temp2 = temp + str(chr(i))
        if temp2 in dictionary.keys():
            temp = temp2
        else:
            result.append(dictionary[temp])
            dictionary[temp2] = DICTIONARY_SIZE
            DICTIONARY_SIZE += 1
            temp = "" + str(inp[i + i + 3])
        # avancer en 3
        i = i + 3
    if temp != "":
        result.append(dictionary[temp])

    return img, result


def decompress(input):
    global DICTIONARY_SIZE
    dictionary = {}
    result = []

    for i in range(0, DICTIONARY_SIZE):
        # lire en 3
        dictionary[i] = str(i).zfill(3)

    # ajouter en 3
    previous = str(input[0]).zfill(3)
    input = input[1:]
    result.append(previous)

    for bit in input:
        aux = ""
        if bit in dictionary.keys():
            aux = dictionary[bit]
        else:
            aux = previous + previous[0:3]
        result.append(aux)
        print(result)
        dictionary[DICTIONARY_SIZE] = previous + aux[0]
        DICTIONARY_SIZE += 1
        previous = aux

    result = ''.join(result)

    return result


################### MAIN #########################

image1_np = np.array([[0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0]]) * 255

image2_np = np.array([[0, 0, 0.5, 1, 1, 1],
                      [1, 1, 1, 0, 0, 0.5],
                      [0.5, 0, 0, 1, 1, 1],
                      [0, 0, 0.5, 1, 1, 1],
                      [1, 1, 1, 0, 0, 0.5],
                      [0, 0, 0.5, 1, 1, 1]]) * 255

# convertir l'image str puis stocker le str dans un fichier.txt
imageFile, fileTxt = convertImgToStr('paint.jpeg', 'image1.txt')
# imageFile1, fileTxt1 = convertImgToStr('eyeman.jpeg', 'image2.txt')

parser = argparse.ArgumentParser(description='Text compressor and decompressor.')
parser.add_argument('action', choices={"compress", "decompress"}, help="Define action to be performed.")
parser.add_argument('-i', action='store', dest='input', required=True,
                    help='Input file.')
parser.add_argument('-o', action='store', dest='output', required=True,
                    help='Output file.')
arguments = parser.parse_args()

ABSOLUTE_PATH = os.getcwd()

# compression / decompression du fichier


if arguments.action == 'compress':

    input = open(ABSOLUTE_PATH + "//" + arguments.input, "rb").read()
    output = open(ABSOLUTE_PATH + "//" + arguments.output, "wb")

    compressedFile = compress(input)
    pickle.dump(compressedFile, output)

    with open('binary_image1.bin', 'rb') as bin:
        for i in bin:
            binCode = binCode + i
        with open('binary_image1.bin', 'w') as txt:
            txt.write(binCode)
else:
    input = pickle.load(open(ABSOLUTE_PATH + "//" + arguments.input, "rb"))
    output = open(ABSOLUTE_PATH + "//" + arguments.output, "w")

    uncompressedFile = decompress(input)
    for l in uncompressedFile:
        output.write(l)
    output.close()

# convertir le dossier .bin généré a une image
# imageFile1, fileTxt1 = convertImgToStr('eyeman.jpeg', 'binary_image1.bin')

binFileToImg('binary_image1.bin')
# binFileToImg('binary_image2.bin')
