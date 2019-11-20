from PIL import Image, ImageFile
from simon import SIMON
import io
import os
import base64
import binascii
from grafica import * 
import PIL.Image
import math

ImageFile.LOAD_TRUNCATED_IMAGES = True

def main(): 
    root = Tk()
    ex = Grafica(root)
    
    root.geometry("500x500+300+300")
    #root.mainloop()  

    try: 

        with open("original.bmp") as image:
		 fileContent = image.read()
		 byteArray = bytearray(fileContent)
        # header: primeros 54 bits
	header = fileContent[0:54]
		
	count=54
    # anexo el header a texto payload cifrado	
	cipherContent=header	
	while count < len(fileContent):
	        #Como usamos long a 8 bytes x caracter y 128 de bloques tenemos que iterar para mandarle al cifrador
			payload = fileContent[count:count+16]
			#se cifra solo el payload
#			print (payload)
#			print (len(str(payload)))
#			print ("payload")
			my_simon = SIMON(128, 256, 0x1f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100)
			cipherPayload = my_simon.encrypt(long(payload.encode('hex'), 16))

			res= str("%x" % cipherPayload) #formato para sacar el trail 'L' que agrega el encode('hex') y el '0x'
			if res.__len__()%2 ==1:
			 res="0{}".format(res) #completo con 0 si es impar
			cipherPayload = res
			# join de la cabecera original con los datos encriptados
			cipherContent += binascii.a2b_hex(str(cipherPayload))
			count +=16

        # aca tiene que ir el payload cifrado
        image = PIL.Image.open(io.BytesIO(cipherContent))
        image.save('cipher.bmp')

		

    except Exception as e: print(e)
		
    try:

        with open("cipher.bmp") as image:
		 fileContent = image.read()
		 byteArray = bytearray(fileContent)
        # header: primeros 54 bits
	header = fileContent[0:54]
	count=54
	DescipherContent=header
	while count < len(fileContent):
	        #Como usamos long a 8 bytes x caracter y 128 de bloques tenemos que iterar para mandarle al cifrador
			payload = fileContent[count:count+16]
			#se cifra solo el payload
#			print (payload)
#			print (len(str(payload)))
#			print ("payload Decript")

			my_simon = SIMON(128, 256, 0x1f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100)
			DescipherPayload = my_simon.decrypt(long(payload.encode('hex'), 16))
			res= str("%x" % DescipherPayload) 
			if res.__len__()%2 ==1:
			 res="0{}".format(res)
			DescipherPayload = res
            # print 'hex(DescipherPayload) ' + hex(DescipherPayload)
			#print 'res ' + res
			#print type(DescipherContent)
			#print 'str desc ' + str(DescipherPayload)

			DescipherContent +=  binascii.a2b_hex(str(DescipherPayload))
			#DescipherContent += binascii.a2b_hex(str(DescipherPayload)[32:len(str(DescipherPayload))])
			count +=16

        image = PIL.Image.open(io.BytesIO(DescipherContent))
        image.save('Descipher.bmp')
		

    except Exception as e: print(e)
		

if __name__ == "__main__": 
    main()