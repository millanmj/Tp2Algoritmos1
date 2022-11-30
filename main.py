#pip install python-dotenv (instalen esto para poder usar la apikey)

import csv
import os

from datetime import datetime
from geopy.geocoders import Nominatim
from functools import partial

import requests
from requests.auth import HTTPBasicAuth

from settings import settings
import speech_recognition as sr

import webbrowser
import cv2

from deteccionplacas import reconocer_patente

from punto3y4 import boca
from punto3y4 import river
from punto3y4 import pertenece_al_cuadrante

APIKEY = settings.APIKEY


#FUNCION PARA BORRAR
def cls() -> None:
    command = 'clear'

    if os.name in ('nt', 'dos'):
        command = 'cls'

    os.system(command)

def menu()-> int:
    opciones: list[str] = [
        '1- Procesar archivo de denuncias',
        '2- Listar todas las infracciones dentro del centro de la ciudad',   
        '3- Listar los autos infraccionados con pedido de captura',
        '4- Listar autos infraccionados cercanos a los estadios',
        '5- Consultar infracciones por patente',
        '6- Mostrar estadisticas de denuncias',
        '7- Ingrese 0 para salir'
    ]
    
    print('\n GESTOR DE DENUNCIAS \n')

    for item in opciones:
        print(item)
    opcion: int = int(input("\n Ingrese una opción:  ->  "))
    return opcion


def leerCSV(archivo: str) -> list:

    try:
        datos:list = []
        with open(archivo, newline='', encoding="UTF-8") as archivo_csv:
                csv_reader = csv.reader(archivo_csv, delimiter=',')
                next(csv_reader) 
                for linea in csv_reader:
                    datos.append(linea)
        
    except IOError: 
        print("No se encontró el archivo")   

    except:
        print("Ocurrio un error inesperado, por favor reintente mas tarde")    

    return datos


def leerTxt(archivo: str) -> list:
    autosRobados: list = []
    try: 
        with open(archivo, 'r') as robados:
            for auto in robados:               
                autosRobados.append(auto.strip('\n'))
        
    except IOError: 
        print("No se encontró el archivo")   

    except:
        print("Ocurrio un error inesperado, por favor reintente mas tarde") 
    
    
    return autosRobados


def imprimirCsv(datos: list) -> None:

    for dato in datos:                    
        print("fecha y hora de la denuncia: ", dato[0])
        print("número: ", dato[1])
        print("Coordenadas latitud: ",dato[2])
        print("Coordenadas longitud: ", dato[3])
        print("ruta foto: ", dato[4])
        print("Texto de wsp: ", dato[5])
        print("ruta audio: ", dato[6])
        print("------------------------------------------")  


def crearCsv(datos: list) -> None:
    audios : list = []
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

        patente: str = str(reconocer_patente(dato[4]))

        descripcion_en_txt: str = dato[5]
        descripcion_del_audio: str = convertirVozATexto(dato[6])

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
        with open('datosProcesados.csv', 'w', newline='', encoding="UTF-8") as archivo_csv:
            csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
            csv_writer.writerows(matriz)
    
    except IOError: 
        print("No se encontró el archivo")   
    except:
        print("Ocurrio un error inesperado, por favor reintente mas tarde")    


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
    



def convertirVozATexto(ruta_archivo:str) -> str:
    r = sr.Recognizer()
    prueba = sr.AudioFile(ruta_archivo)
    with prueba as source:
        audio = r.record(source)
    denuncia = (r.recognize_google(audio,language='es-ES'))
    return denuncia


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

def verSiPerteneceAlRangoDeCoordenadas(denuncias: str, datosprocesados: str):

    autosCoordenadas: list = []
    autosCoordenadas = leerCSV(denuncias)
    autosCercanos: list = []
    autosCercanos = leerCSV(datosprocesados)

    print("\nAutos dentro de la ciudad: \n")
    
    for dato in autosCoordenadas:
        for i in autosCercanos:
            patente: str = i[5]
        latitud = float(dato[2])
        longitud = float(dato[3])
        pertenece_al_cuadrante(latitud, longitud)
        if pertenece_al_cuadrante(latitud, longitud) == True:
            print(f"Patente: {patente}\nCoordenadas: {latitud} , {longitud}")

def verSiEsCercanoALosEstadios(denuncias: str, datosprocesados: str):

    autosCoordenadas: list = []
    autosCoordenadas = leerCSV(denuncias)
    autosCercanos: list = []
    autosCercanos = leerCSV(datosprocesados)

    print("\nAutos cercanos al estadio de Boca: \n")
    
    for dato in autosCoordenadas:
        for i in autosCercanos:
            patente: str = i[5]
        latitud = float(dato[2])
        longitud = float(dato[3])
        boca(latitud, longitud)
        if boca(latitud, longitud) == True:
            print(f"Patente: {patente}\nCoordenadas: {latitud} , {longitud}")

    print("\nAutos cercanos al estadio de River: \n")

    for dato in autosCoordenadas:
        for i in autosCercanos:
            patente: str = i[5]
        latitud = float(dato[2])
        longitud = float(dato[3])
        river(latitud, longitud)
        if boca(latitud, longitud) == True:
            print(f"Patente: {patente}\nCoordenadas: {latitud} , {longitud}")

def verSiEsRobado(listaDeRobados:list, denuncias: str) -> None:
    
    
    autosRobados: list = []
    formulario_robados:dict = {}
    autosDenunciados: list = []
    autosDenunciados = leerCSV(denuncias)
    
    #print(autosDenunciados)
    for auto in autosDenunciados:
        formulario_robados[auto[5]] = [auto[0], auto[2],auto[3]]
    
    print("\n LISTA DE VEHICULOS ROBADOS CON DENUNCIA DE INFRACCIÓN \n")

    for n in listaDeRobados:
      for key,value in formulario_robados.items():
        if n == key:
            print("----------------------------------------------")         
            print("Patente: {}".format(key))
            print("Ubicación del vehículo: {}".format(value[1]))
            print("Localidad: {}".format(value[2]))
            fecha = datetime.fromtimestamp(float(value[0]))#pasar de timestamp a fecha
            print("Fecha y hora de la denuncia: {}".format(fecha))           
            print("----------------------------------------------")
            autosRobados.append([value[1],value[2],fecha,key])


def consultarPatente(archivo1: str, archivo2: str) -> None:

    consulta: dict = {'timestamp': '', 'latitud':'' , 'longitud': '', 'patente': '', 'rutaImagen':''}
    denuncias: list = []
    datosProcesados: list = []

    patente: str = input('Ingrese la patente que desea consultar: ')
    consulta['patente'] = patente
    
    #FALTA VALIDAR SI LA PATENTE SE ENCUENTRA EN EL CSV, SINO DEBEMOS MOSTRAR UN MENSAJE BONITO

    #Hay que obtener la latitud, la longitud, y la ruta de la imagen
    denuncias= leerCSV(archivo1)

    #hay que obtener la patente
    datosProcesados= leerCSV(archivo2)
    
    for dato in datosProcesados:
        if (dato[5] == patente):
            consulta['patente'] = dato[5]
            consulta['timestamp'] = dato[0]                       
    
    for dato in denuncias:
        if (consulta['timestamp'] == dato[0]):
            consulta['latitud'] = dato[2]
            consulta['longitud'] = dato[3]
            consulta['rutaImagen'] = dato[4]

    #Abrimos la ubicación en el navegador
    webbrowser.open('https://maps.google.com/?q='+ consulta['latitud'] +','+ consulta['longitud'], new=2, autoraise=True)

    imagen = cv2.imread(consulta['rutaImagen']) 
    cv2.imshow('Patente consultada',imagen)
    cv2.waitKey(0)

    #cv2.destroyAllWindows()
        
    print('esta la consulta', consulta)


def main() -> None:

    lista: list =[]
    robados: list = []
    lista = leerCSV('Denuncias.csv')   
   
    #imprimirCsv(lista) 
    #nuevo_csv = crearCsv(lista)


    opcion: int= 1

    while(opcion!= 0):
        opcion= menu()

        if (opcion == 1):
            print('1- Procesar archivo de denuncias')
            lista = leerCSV('Denuncias.csv') 
            print('Aguarde por favor, su archivo esta siendo procesado')
            crearCsv(lista)
            print('Su archivo de denuncias ha sido procesado correctamente')   

        elif (opcion == 2):     
            print('2- Listar todas las infracciones dentro del centro de la ciudad') 
            verSiPerteneceAlRangoDeCoordenadas('Denuncias.csv', 'datosProcesados.csv')   

        elif (opcion == 3):
            print('3- Listar los autos infraccionados con pedido de captura')
            robados = leerTxt('robados.txt') #lista
            verSiEsRobado(robados, 'datosprocesados.csv')

        elif (opcion == 4):
            print('4- Listar autos infraccionados cercanos a los estadios')
            verSiEsCercanoALosEstadios('Denuncias.csv', 'datosProcesados.csv')

        elif (opcion == 5):
            print('5- Consultar infracciones por patente')
            consultarPatente('denuncias.csv', 'datosProcesados.csv')

        elif (opcion == 6):
            print('6- Mostrar estadisticas de denuncias')
        
        else: exit()
   
    # print(robados)

        
         
        
        
        
        

main()

