import csv
import json
import os

from geopy.geocoders import Nominatim
from functools import partial

import requests
from requests.auth import HTTPBasicAuth

from settings import settings
import speech_recognition as sr
r = sr.Recognizer()

APIKEY = settings.APIKEY

#2- Con la información leída del archivo CSV, se pide crear un nuevo archivo CSV que contenga los siguientes campos: (Timestamp,Teléfono, Dirección de la infracción, Localidad, Provincia, patente, descripción texto, descripción audio) 
def leerCSV(archivo: str) -> list:

    try:
        datos:list = []
        with open(archivo, newline='', encoding="UTF-8") as archivo_csv:
                csv_reader = csv.reader(archivo_csv, delimiter=',')
                next(csv_reader) 
                for linea in csv_reader:
                    datos.append(linea)

                for dato in datos:
                    
                    print("fecha y hora de la denuncia: ", dato[0])
                    print("número: ", dato[1])
                    print("Coordenadas latitud: ",dato[2])
                    print("Coordenadas longitud: ", dato[3])
                    print("ruta foto: ", dato[4])
                    print("Texto de wsp: ", dato[5])
                    print("ruta audio: ", dato[6])
                    print("------------------------------------------")       

        
    except IOError: 
        print("No se encontró el archivo")   

    except:
            print("Ocurrio un error inesperado, por favor reintente mas tarde")    

    return datos
            

def obtenerDireccion(datos: list, latitud: float, longitud: float) -> list:  

    url: str ='https://api.opencagedata.com/geocode/v1/geojson?q='
    #Llamada a la api de posicionamiento
    response= requests.request("GET", url+ latitud + '%2C' + longitud + '&key=' + APIKEY + '&pretty=1')
    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))   
    
    dataJson= (response.json()['features'][0])
    data: list = []
    data.append(dataJson['properties']['components']['road'] +', '+ dataJson['properties']['components']['house_number'])
    data.append(dataJson['properties']['components']['suburb'])    
    data.append(dataJson['properties']['components']['city'])
    data.append(dataJson['properties']['components']['country'])     
    
    return data
    


def obtenerPatente(rutaImagen: str) -> str:
    pass


def enviar_rutas_audios(datos:list):
    lista_De_rutas:list = []
    for audio in datos:
        ruta = audio[6]
        lista_De_rutas.append(ruta)
    
    denunciasEnTexto:list = []
    for denuncia in (lista_De_rutas):
        text:str = convertirVozATexto(denuncia)
        denunciasEnTexto.append(text)
    
    return denunciasEnTexto

def convertirVozATexto(ruta_archivo:str) -> str:
  prueba = sr.AudioFile(ruta_archivo)
  with prueba as source:
    audio = r.record(source)
  denuncia = (r.recognize_google(audio,language='es-ES'))
  return denuncia


def crearCsv(datos: list) -> None:

    ubicacion: list = []
    matriz:list = [["Timestamp", "Telefono", "Dirección", "Localidad", "Pais", "Patente", "Descripcion_en_txt",  "Descripcion_del_audio"]]
    for dato in datos:
            lista:list = []
            timestamp: str = dato[0]
            telefono: str = dato[1]
                
            ubicacion= obtenerDireccion(datos, dato[2], dato[3])

            direccion: str = ubicacion[0]
            localidad: str = ubicacion[1] + ', ' +ubicacion[2]
            pais: str = ubicacion[3]
            patente: str = ''
            descripcion_en_txt: str = dato[5]
            descripcion_del_audio: str = ''
            lista.append(timestamp)
            lista.append(telefono)
            lista.append(direccion)
            lista.append(localidad)
            lista.append(pais)
            lista.append(patente)
            lista.append(descripcion_en_txt)
            lista.append(descripcion_del_audio)
            matriz.append(lista)
        
        
    try:
        #archivo = open('datosProcesados.csv', 'a')
        
        with open('datosProcesados.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file, delimiter=',')
            csv_writer.writerows(matriz)
        
        # with open(“alumnos.csv”, 'w', newline='', encoding="UTF-8") as archivo_csv:
                # csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
                # csv_writer.writerow(["Padron", "Nombre", "Apellido"]) #Escribimos el header

                # for padron, nombre_completo in alumnos.items():
                #     nombre, apellido = nombre_completo
                #     csv_writer.writerow((padron, nombre, apellido))

    except IOError: 
        print("No se encontró el archivo")   

    except:
        print("Ocurrio un error inesperado, por favor reintente mas tarde")    
  




lista = leerCSV('Denuncias.csv')
nuevo_csv = crearCsv(lista)

audio_A_texto:list = enviar_rutas_audios(lista)#audios en texto
print(audio_A_texto)

#>>>>>>> 2cc24131f1a57cf6256d78ab3ed01e3d7278a9af
