import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (f'C:\\Users\\Agustin\\AppData\\Local\\Tesseract-OCR\\tesseract.exe')

def validar_patente(data: str) -> bool:

    patente_validada:bool = False
    contador:int = 0
    if len(data) == 9:
        data_lista = data.split("")
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
        numeric = "0123456789" 
        alpha_lista = alpha.split("")
        numeric_lista = numeric.split("")
        for i in data_lista[0]:
            if i in alpha_lista:
                contador += 1
        for j in data_lista[1]: 
            if j is numeric:
                contador += 1
        for k in data_lista[2]:
            if k in alpha_lista:
                contador += 1

        if contador == 7:
            patente_validada = True 

    return patente_validada

def plot_image(img, grayscale=True, iterations=0):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#Este pasa la foto a blanco y negro   me fije en el git del tipo que vimos y tiene esto
    gray = cv2.blur(gray,(3,3))#le pone el efecto blur 
    canny = cv2.Canny(gray,150,200)#Este es para pasarlo todo a blanco y negro completamente 
    canny = cv2.dilate(canny,None,iterations=2)#Aca esta el problema, texto, cambia el grosor algunas funcionan con 1 y otras con 2 y 3
    cnts,_ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img,cnts,-1,(0,255,0),2)

    for c in cnts:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
        epsilon = 0.09*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        if len(approx)==4 and area > 2000:
            # print('area=', area)
            cv2.drawContours(img,[c],0,(0,255,0),2)
            license_ratio = float(w)/h
            if license_ratio > 1.4:
                placa = gray[y:y+h,x:x+w]
                placa = cv2.resize(placa, None, fx=5, fy=5)
                sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                sharpen = cv2.filter2D(placa, -1, sharpen_kernel)
                thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_OTSU)[1] 
                data = pytesseract.image_to_string(thresh, config='--psm 6')#Aca hay otro problema, pasa lo mismo con iteration pero esta vez con el config
                print(data_lista)                
                # cv2.imshow('Placa', placa)
                # cv2.imshow('thresh', thresh)
                # cv2.imshow('sharpen', sharpen)

    cv2.imshow('Image', img)
    # cv2.imshow('Canny', canny)
    cv2.moveWindow('Image',45,10)
    cv2.waitKey(0)

def main():

    img = cv2.imread(f"C:\\Users\\Agustin\\Desktop\\Tp2Algoritmos1\\Imagenes_autos\\003.png")
    plot_image(img, False)

main()