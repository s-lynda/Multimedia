import argparse
import os
import pickle
import cv2
import numpy as np

DICTIONARY_SIZE = 256


def compress(input):
    
    img_color=cv2.imread(input,cv2.IMREAD_COLOR)

    img_bw=cv2.imread(input,cv2.IMREAD_GRAYSCALE)

    # we choosed 127 cuz 127*2 = 256 -> au dela de 128 c noir et au dessus c blanc=0

    threshold=127

    _, img_bw1=cv2.threshold(img_bw,threshold, 255, cv2.THRESH_BINARY)
   
    otsu, img_bw_Ot=cv2.threshold(img_bw,threshold, 255, cv2.THRESH_BINARY)

    img= np.array(img_bw_Ot)
    img=img.flatten()
    image=[]

    #code each pixel on 3 caracter
    for i in range(len(img)):
        image.append(str(img[i]).zfill(3))

    input_array=''.join(image)

    global DICTIONARY_SIZE
    dictionary = {}
    result = []
    temp = ""

    for i in range(0, DICTIONARY_SIZE):
        dictionary[str(i).zfill(3)] = i

    # for c in input:
    #     temp2 = temp+str(chr(c))
    #     if temp2 in dictionary.keys():
    #         temp = temp2
    #     else:
    #         result.append(dictionary[temp])
    #         dictionary[temp2] = DICTIONARY_SIZE
    #         DICTIONARY_SIZE+=1
    #         temp = ""+str(chr(c))

    i=0
    while(i< len(input_array)):
        temp2 = temp+str(input_array[i:i+3])
        
        if temp2 in dictionary.keys():
            temp = temp2
        else:
            result.append(dictionary[temp])
            dictionary[temp2] = DICTIONARY_SIZE
            DICTIONARY_SIZE+=1
            temp = ""+str(input_array[i:i+3]) 
            #print(temp)
        i+=3

    if temp != "":
        result.append(dictionary[temp])     
    return result

def decompress(input):
    global DICTIONARY_SIZE
    dictionary = {}
    result = []

    for i in range(0, DICTIONARY_SIZE):
        dictionary[i] = str(i).zfill(3)

    previous = str(input[0]).zfill(3)
    input = input[1:]
    result.append(previous)

    for bit in input:
        aux = ""
        if bit in dictionary.keys():
            aux = dictionary[bit]
        else:
            aux = previous+previous[0:3] 
            #Bit is not in the dictionary
                 # Get the last character printed + the first position of the last character printed
                 #because we must decode bits that are not present in the dictionary, so we have to guess what it represents, for example:
                 #let's say bit 37768 is not in the dictionary, so we get the last character printed, for example it was 'uh'
                 #and we take it 'uh' plus its first position 'u', resulting in 'uhu', which is the representation of bit 37768
                 #the only case where this can happen is if the substring starts and ends with the same character ("uhuhu").
        result.append(aux)
        dictionary[DICTIONARY_SIZE] = previous + aux[0:3]
        DICTIONARY_SIZE+= 1
        previous = aux

        result=''.join(result)
    return result


parser = argparse.ArgumentParser(description = 'Text compressor and decompressor.')
parser.add_argument('action', choices={"compress", "decompress"}, help="Define action to be performed.")
parser.add_argument('-i', action = 'store', dest = 'input', required = True,
                           help = 'Input file.')
parser.add_argument('-o', action = 'store', dest = 'output', required = True,
                           help = 'Output file.')
arguments = parser.parse_args()

ABSOLUTE_PATH = os.getcwd()

if arguments.action == 'compress':
    input = arguments.input
    output = open(ABSOLUTE_PATH+"//"+arguments.output, "wb")

    compressedFile = compress(input)
    pickle.dump(compressedFile, output)
else:
    input = pickle.load(open(ABSOLUTE_PATH+"//"+arguments.input, "rb"))
    output = open(ABSOLUTE_PATH+"//"+arguments.output, "w")
    uncompressedFile = decompress(input)
  