
import math
import numpy as np

def cosi(x,u,n=8):
    k=2*x+1
    cosinus=math.cos((k*u*np.pi)/(2*n))
    return cosinus 



image=[
[140 ,144 ,147 ,140 ,140 ,155 ,179 ,175],
[144 ,152 ,140 ,147 ,140 ,148 ,167 ,179],
[152 ,155 ,136 ,167 ,163 ,162 ,152 ,172],
[168 ,145 ,156 ,160 ,152 ,155 ,136 ,160],
[162 ,148 ,156 ,148 ,140 ,136 ,147 ,162],
[147 ,167 ,140 ,155 ,155 ,140 ,136 ,162],
[136 ,156 ,123 ,167 ,162 ,144 ,140 ,147],
[148 ,155 ,136 ,155 ,152 ,147 ,147 ,136]
]


def alpha(u):
    if u == 0:
        return 1/math.sqrt(2)
    else:
        return 1

def DC(u,v,img):
    sum = 0
    N = len(img)
    M = len(img[0])
    for x in range(N):
        for y in range(M):
            sum = sum + img[x][y]*cosi(x,u,N)*cosi(y,v,M)
    
    result=2*math.sqrt(1/(N*M))*alpha(u)*alpha(v)*sum
    return  result

def DCT(img):
    dct = []
    N = len(img)
    M = len(img[0])
    for u in range(N):
        liste=[]
        for v in range(M):
            liste.append(DC(u,v,img))

        dct.append(liste)
    return dct


def inv(x,y, dct):
    n = len(dct)
    M = len(dct[0])
    sum = 0

    for u in range(n):
        for v in range(M):
            sum = sum + alpha(u)*alpha(v)*dct[u][v]*cosi(x,u,n)*cosi(y,v,M)

    result=2*math.sqrt(1/(n*M))*sum
    return result

def inv_dct(dct):
    img = []
    n = len(dct)
    M = len(dct[0])

    for u in range(n):
        temp=[]
        for v in range(M):
            temp.append(inv(u,v,dct))

        img.append(temp)

    return img


print('***************** Image **************')
print(image)
print('\n\n')
print('***************** DCT***************')
print(DCT(image))

print('\n\n')

print('***************** DCT inverse***************')
print(inv_dct(DCT(image)))

print('\n\n')

# ---------------------------------------
