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




def binFileToImg(binaryFile):
    w, h = 120,120

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

def compress(input):
    global DICTIONARY_SIZE
    dictionary = {
        0: '000',
        255: '001'
    }
    result = []
    temp = ""

    for i in range(0, DICTIONARY_SIZE):
        dictionary[str(chr(i))] = i

    for c in input:
        temp2 = temp + str(chr(c))
        if temp2 in dictionary.keys():
            temp = temp2
        else:
            result.append(dictionary[temp])
            dictionary[temp2] = DICTIONARY_SIZE
            DICTIONARY_SIZE += 1
            temp = "" + str(chr(c))

    if temp != "":
        result.append(dictionary[temp])

    return result


def decompress(input):
    global DICTIONARY_SIZE
    dictionary = {
        '000': 0,
        '001': 255
    }
    result = []

    for i in range(0, DICTIONARY_SIZE):
        dictionary[i] = str(chr(i))

    previous = chr(input[0])
    input = input[1:]
    result.append(previous)

    for bit in input:
        aux = ""
        if bit in dictionary.keys():
            aux = dictionary[bit]
        else:
            aux = previous + previous[0]
            # Bit is not in the dictionary
            # Get the last character printed + the first position of the last character printed
            # because we must decode bits that are not present in the dictionary, so we have to guess what it represents, for example:
            # let's say bit 37768 is not in the dictionary, so we get the last character printed, for example it was 'uh'
            # and we take it 'uh' plus its first position 'u', resulting in 'uhu', which is the representation of bit 37768
            # the only case where this can happen is if the substring starts and ends with the same character ("uhuhu").
        result.append(aux)
        dictionary[DICTIONARY_SIZE] = previous + aux[0]
        DICTIONARY_SIZE += 1
        previous = aux

    return result


################### MAIN #########################

image1_np = np.array([[0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0]])*255

writeArray(image1_np)

image2_np = np.array([[0, 0, 0.5, 1, 1, 1],
                    [1, 1, 1, 0, 0, 0.5],
                    [0.5, 0, 0, 1, 1, 1],
                    [0, 0, 0.5, 1, 1, 1],
                    [1, 1, 1, 0, 0, 0.5],
                    [0, 0, 0.5, 1, 1, 1]])*255

#convertir l'image str puis stocker le str dans un fichier.txt
#imageFile, fileTxt = convertImgToStr('paint.jpeg', 'image1.txt')
#imageFile1, fileTxt1 = convertImgToStr('eyeman.jpeg', 'image2.txt')

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
else:
    input = pickle.load(open(ABSOLUTE_PATH + "//" + arguments.input, "rb"))
    output = open(ABSOLUTE_PATH + "//" + arguments.output, "w")

    uncompressedFile = decompress(input)
    for l in uncompressedFile:
        output.write(l)
    output.close()

# convertir le dossier .bin généré a une image

#binFileToImg('binary_image1.bin')
#binFileToImg('binary_image2.bin')
