from PIL import Image, ImageFile
from simon import SIMON
import io
import os
import base64

def main(): 
    try: 
        #necesito abrir dos veces para recuperar el image.size del archivo original
        with Image.open("original.bmp") as image:
         width, height = image.size

        with open("original.bmp") as image:
         fileContent = image.read()
         byteArray = bytearray(fileContent)
        
        # header: primeros 54 bits
        header = fileContent[0:54]
        payload = fileContent[54:len(fileContent)]
        
        #se cifra solo el payload
        #my_simon = SIMON(128, 256, 0x1f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100)
        #cipherPayload = my_simon.encrypt(int(payload.encode('hex'), 16))
        
        # join de la cabecera original con los datos encriptados
        #cipherContent = header + cipherPayload  
        
        # prueba: si guardo como imagen la cabecera + el payload la imagen bien esta bien formada
        cipherContent = header + payload 

        # este .save() funciona con el header pero le cambia el color a la imagen
        #cipher = Image.frombytes('RGB', (width, height), cipherContent).split()
        #cipher = Image.merge('RGB', cipher)
        #cipher = cipher.transpose(Image.FLIP_TOP_BOTTOM)
        #cipher.save('cipher.bmp')

        # aca tiene que ir el payload cifrado
        image = Image.open(io.BytesIO(cipherContent))
        image.save('cipher.bmp')

        # imagen descifrada a partir del cipher
        
    except IOError: 
        print 'IOError'

if __name__ == "__main__": 
    main()