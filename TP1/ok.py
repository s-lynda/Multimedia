#import itertools

def decode(height,width,filename="compressed.txt",bits=15):
    with open(filename,"r") as file:
        hexa_code= file.readlines()[0]
        data=[]
        size=2 **(bits+1)-2**bits
        i=0
        #count c la taille de la séquence
        while i<len(hexa_code):
            #Récupérer les 4 premiers 
            count=hexa_code[i:i+4]
            count=int(count,16) # function int -> convertit n'importe quel nombre en hexa
            i+=4
            if count>size: # cas d'une sequence de couleurs qui se repète
                count-=size
                color=hexa_code[i:i+2]
                color=int(color,16)
                data+=[color]*count
                i+=1
            else:#count <=size
                color_seq=hexa_code[i:i+count*2] #lire apr 2 car it's a char
                colors=[int(color_seq[idx:idx+2],16) for idx in range(0,len(color_seq))] #couleur contient 2 char
                data+=colors
                #img=np.reshape(hexa_code,(height,width))
                img=np.reshape(data,(height,width))
                #soit using reshape of the numpy library or we gonna create it 
                #reshape's concept
                #image=np.zeros(height,width)
                #enumerate return tuple (index, elt) # enumerate(itertools.itertools.product)
                #function np.count_nonzero(img_bw,img_decomp)
                # for idx, (i,j) in range(height),range(width):  


    return img