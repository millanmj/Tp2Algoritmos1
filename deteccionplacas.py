
#https://github.com/UB-Mannheim/tesseract/wiki
import cv2
#from PIL import Image
import numpy as np
#import matplotlib.pyplot as plt
import pytesseract
# from darkflow.net.build import TFNet

from settings import settings

#Importaciones para la api plate recognizer
import requests
from pprint import pprint
import json
PATH :str = settings.PATH_PYS 
APIKEY:str = settings.PLATE_APIKEY

pytesseract.pytesseract.tesseract_cmd = (f'{PATH}')



def validar_patente(data: str) -> bool:
    """
    Pre: Recibe la patente sin validar, para verificar si coincide con la estructura de una patente Argentina actual
    Pos: Devuelve un bool que demuestra si la patente coincide o no
    """
    
    patente_validada:bool = False
    contador:int = 0
    if len(data) == 10: #len(data) longitud de la patente
        data_lista = data.split() # [AB, 123, CD]
        alpha = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z" 
        numeric = "0 1 2 3 4 5 6 7 8 9" 
        alpha_lista = alpha.split() #Genera una lista con los datos de alpha
        numeric_lista = numeric.split()
        for i in data_lista[0]:
            if i in alpha_lista:
                contador += 1
        for j in data_lista[1]: 
            if j in numeric_lista:
                contador += 1
        for k in data_lista[2]:
            if k in alpha_lista:
                contador += 1

        if contador == 7:
            patente_validada = True

    # if patente_validada == True:
    #     print(data)
        
    return patente_validada


def consultaApiPatente(ruta_foto: str) -> str:
    """
    Pre: Recibe la la direccion en donde se encuentra la foto si el método de reconocer_patente no funciona
    Pos: Devuelve la patente despues de pasar por el metodo de la API
    """

   #Enviamos la consulta a la API
    with open(ruta_foto, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=['ar']),  # Optional , config=json.dumps(dict(region="strict"))
            files=dict(upload=fp), headers={'Authorization': f'Token {APIKEY}'})
            
    #pprint(response.json())
   

    patente= (response.json()['results'][0]['plate']).upper()
    patente = patente[0:2]+' '+patente[2:5]+' '+patente[5:7] # ab123cd --> AB 123 CD

    return patente
   

def reconocer_patente(ruta_foto: str) -> str:
    """
    Pre: Recibe la direccion en donde se encuentra la foto
    Pos: Devuelve la patente
    """
    
    img = cv2.imread(ruta_foto) #img recibe la foto
    #grayscale = False
    patente_validada:bool = False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Pasa la imagen a blanco y negro
    gray = cv2.blur(gray,(3,3)) # Suaviza la imagen
    canny = cv2.Canny(gray,150,200) # Deja la imagen en blanco y negro sin ningun tono de gris
    
    valor_iteracion: int = 1
    while((valor_iteracion < 6) and (patente_validada == False)):
    #####################################################
        canny = cv2.dilate(canny,None,iterations = valor_iteracion) #Define el grosor del contorno
        cnts,_ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # Buscando los contornos
        # cv2.drawContours(img,cnts,-1,(0,255,0),2) #Sirve para testear y ver los contornos definidos en color verde

        for c in cnts:
            area = cv2.contourArea(c)
            x,y,w,h = cv2.boundingRect(c)
            epsilon = 0.09*cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,epsilon,True)
            if len(approx)==4 and area > 2000: #4 son los vertices, 2000 es el area que se define para filtrar la patente
                # print('area=', area)
                cv2.drawContours(img,[c],0,(0,255,0),2)
                license_ratio = float(w)/h
                if license_ratio > 1.4:
                    placa = gray[y:y+h,x:x+w] # Paso la imagen de la placa a blanco y negro
                    placa = cv2.resize(placa, None, fx=5, fy=5)
                    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                    sharpen = cv2.filter2D(placa, -1, sharpen_kernel)
                    thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_OTSU)[1] # Deja la imagen en blanco y negro sin ningun tono de gris

                    data = pytesseract.image_to_string(thresh, config='--psm 6')        
                    configuracion = 7
                    patente_validada = validar_patente(data)

                    while ((patente_validada == False) and (configuracion < 14)):
                        # print('valor de configuracion: ',configuracion)
                        data = pytesseract.image_to_string(thresh, config=f'--psm {configuracion}')
                        patente_validada = validar_patente(data)#aca me inidica si es true
                        configuracion += 1
        # print('valor de iteración:',valorDeIteracion)
        valor_iteracion += 1
        
    
    if (patente_validada == False):
        data = consultaApiPatente(ruta_foto)
    else:
        data = data.replace("\n", "")       
    
    return data 


              # cv2.imshow('Placa', placa)
                # cv2.imshow('thresh', thresh)
                # cv2.imshow('sharpen', sharpen)

    # cv2.imshow('Image', img)
    # # cv2.imshow('Canny', canny)
    # cv2.moveWindow('Image',45,10)
    # cv2.waitKey(0)

