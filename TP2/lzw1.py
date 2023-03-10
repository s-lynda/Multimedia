#Import modules
import argparse
import itertools
import os
import pickle
import numpy as np
import PIL
from PIL import Image
import base64

DICTIONARY_SIZE = 256

   

# Convert an image to string in a bianry file
def convertImgToStr(imageFile, txt_file):
    with open(imageFile, "rb") as img2str:
        converted_string = base64.b64encode(img2str.read())
    
    #print(converted_string)
    with open(txt_file, "wb") as file:
        file.write(converted_string)

    return imageFile, txt_file

def convertStrtoImg(txt_file,imagename):
    
    file = open(txt_file, 'rb')
    byte=file.read()
    file.close()
    decodeit = open(imagename, 'wb')
    decodeit.write(base64.b64decode((byte)))
    decodeit.close()

    return imagename


def compress(input):
    global DICTIONARY_SIZE
    # dictionary = {
    #     0: '000',
    #     255: '001'
    # }
    dictionary=dict((chr(i), i) for i in range(DICTIONARY_SIZE))
    result = []
    temp = ""

    for i in range(0, DICTIONARY_SIZE):
        dictionary[str(chr(i))] = i

    for c in input:
        temp2 = temp +str(chr(c))
        if temp2 in dictionary.keys():
            temp = temp2
        else:
            result.append(dictionary[temp])
            dictionary[temp2] = DICTIONARY_SIZE
            DICTIONARY_SIZE += 1
            temp = "" +str(chr(c))

    if temp != "":
        result.append(dictionary[temp])
    
    #print(result)
    return result


def decompress(input):
    global DICTIONARY_SIZE
    # dictionary = {
    #     '000': 0,
    #     '001': 255
    # }
    dictionary=dict((i, chr(i)) for i in range(DICTIONARY_SIZE))
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



#convertir l'image str puis stocker le str dans un fichier.txt
#imageFile, filetxt = convertImgToStr('paint.jpeg', 'compressed.bin')
#imageFile, filetxt = ImgtoText('paint.jpeg', 'image1.txt')

#original_image=convertStrtoImg('binary_image.bin','paint1.jpeg')

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

original_image=convertStrtoImg('binary_image.bin','paint1.jpeg')
