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
from deteccionplacas import validar_patente

from punto3y4 import *
from punto7 import *


APIKEY = settings.APIKEY


#FUNCION PARA BORRAR (es para borrar)
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
        '6- Mostrar grafico de denuncias por mes',
        '7- Ingrese 0 para salir'
    ]
    
    print('\n GESTOR DE DENUNCIAS \n')

    for item in opciones:
        print(item)
    opcion: int = int(input("\n Ingrese una opción:  ->  "))
    return opcion


def leerCSV(archivo: str) -> list:

    """
    Pre: Recibe del archivo csv a leer.
    Pos: Retorna una lista con los datos del archivo pasado.
    """
    
    try:
        datos:list = []
        with open(archivo, newline='', encoding="UTF-8") as archivo_csv:
                csv_reader = csv.reader(archivo_csv, delimiter=',')
                next(csv_reader) 
                for linea in csv_reader:
                    datos.append(linea)
        
    except IOError: 
        print("procesando archivo....")   

    except:
        print("Ocurrio un error inesperado, por favor reintente mas tarde")    

    return datos


def leerTxt(archivo: str) -> list:
    """
    Pre: Recibe la ruta de un archivo txt a leer.
    Pos: Retorna una lista con los elementos del archivo txt.
    """
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
    """
    Pre: Recibe una lista que se creó a partir de denuncias.csv
    Pos: Imprime de forma clara los datos de dicha lista.
    """
    for dato in datos:                    
        print("fecha y hora de la denuncia: ", dato[0])
        print("número: ", dato[1])
        print("Coordenadas latitud: ",dato[2])
        print("Coordenadas longitud: ", dato[3])
        print("ruta foto: ", dato[4])
        print("Texto de wsp: ", dato[5])
        print("ruta audio: ", dato[6])
        print("------------------------------------------")  


def compararDenuncia( timestamp: str, archivoProcesados: str) -> bool:
    """
    Pre: Recibe el timestamp del archivo de denuncias y la ruta de datosProcesados.
    Pos: Devuelve un booleano positivo en caso de que exista el registro.
    """
    iguales: bool = False

    try:
        datosProcesados = leerCSV(archivoProcesados)
       
        for fila in datosProcesados:           
            if (str(timestamp) == str(fila[0])):              
                iguales = True

    except FileNotFoundError:
        print('Archivo Datos Procesados no existente')
    
    return iguales

   
def procesarDenuncia(dato: list) -> list:
    """
    Pre: Recibe una lista con los datos de denuncias.csv
    Pos: Retorna una lista con los datos procesados.
    """
    lista:list = []
    timestamp: str = dato[0]
    telefono: str = dato[1]    
            
    ubicacion= obtenerDireccion(dato[2], dato[3])#consulta la api

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

    return lista


def crearCsv(datos: list) -> None:
    """
    Pre: Recibe una lista con los datos de denuncias.csv
    Pos: Crea el csv pedido en el punto 2.
    """
    matriz: list = []
    nuevasDenuncias: list = []
    matriz:list = [["Timestamp", "Telefono", "Dirección", "Localidad", "Pais", "Patente", "Descripcion_en_txt",  "Descripcion_del_audio"]]
    
    denunciados =leerCSV('datosProcesados.csv')

    for denuncia in denunciados:
        matriz.append(denuncia)

    #Verifico si existe el archivos en datos procesados  
    for dato in datos: 
        existeDenuncia = compararDenuncia(dato[0], 'datosProcesados.csv')

        if(existeDenuncia == False ):
            nuevasDenuncias.append(procesarDenuncia(dato))
    
    for fila in nuevasDenuncias:
        matriz.append(fila)

    try: 
        with open('datosProcesados.csv', 'w', newline='', encoding="UTF-8") as archivo_csv:
            csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"', quoting= csv.QUOTE_NONNUMERIC)      
            csv_writer.writerows(matriz)
    
    except IOError: 
        
        print("No se encontró el archivo")   
    except:
        print("Ocurrio un error inesperado, por favor reintente mas tarde")    


def obtenerDireccion(latitud: float, longitud: float) -> list:  
    """
    Pre: Recibe los datos de latitud y longitud de una dirección correspondiente a una infracción.
    Pos: Retorna una lista con el barrio, la ciudad y el país correspondiente a la infracción.
    """
    url: str ='https://api.opencagedata.com/geocode/v1/geojson?q='
    #Llamada a la api de posicionamiento
    response= requests.request("GET", url+ latitud + '%2C' + longitud + '&key=' + APIKEY + '&pretty=1')
       
    dataJson= (response.json()['features'][0])
    data: list = []
    data.append(dataJson['properties']['components']['road'] +', '+ dataJson['properties']['components']['house_number'])
    data.append(dataJson['properties']['components']['suburb']) #barrio   
    data.append(dataJson['properties']['components']['city'])
    data.append(dataJson['properties']['components']['country'])     
    
    return data
    

def convertirVozATexto(ruta_archivo:str) -> str:
    """
    Pre: Recibe la ruta de los audios con denuncias.
    Pos: Retorna un string que es resultado de transformar el audio a texto.
    """
    r = sr.Recognizer()
    prueba = sr.AudioFile(ruta_archivo)
    with prueba as source:
        audio = r.record(source)
    denuncia = (r.recognize_google(audio,language='es-ES'))
    return denuncia

def verSiPerteneceAlRangoDeCoordenadas(denuncias: str, datosprocesados: str) -> None:
    """
    Pre: Recibe dos rutas a archivos con extensión csv.
    Pos: Muestra en pantalla que autos están con infracciones dentro del cuadrante solicitado.
    """
    autosCoordenadas: list = []
    autosCoordenadas = leerCSV(denuncias)
    autosCercanos: list = []
    autosCercanos = leerCSV(datosprocesados)

    print("\nAutos dentro de la ciudad: \n")
    
    for index, dato in enumerate(autosCoordenadas):
        patente: str = autosCercanos[index][5]            
        latitud = float(dato[2])
        longitud = float(dato[3])
        pertenece_al_cuadrante(latitud, longitud)
        if pertenece_al_cuadrante(latitud, longitud) == True:
            print(f"Patente: {patente}\nCoordenadas: {latitud} , {longitud}")

    volver_a_menu: str = input("Presione ENTER para volver al menu")


def verSiEsCercanoALosEstadios(denuncias: str, datosprocesados: str) -> None:
    """    
    Pre: Recibe dos rutas a archivos con extensión csv.
    Pos: Muestra en pantalla que autos están con infracciones a menos de 1km de los estadios de River y Boca.
    """
    autosCoordenadas: list = []
    autosCoordenadas = leerCSV(denuncias)
    autosCercanos: list = []
    autosCercanos = leerCSV(datosprocesados)
    boca: tuple = (-34.635614, -58.364669)
    river: tuple = (-34.545290, -58.449740)

    print("\nAutos cercanos al estadio de Boca: \n")
    
    for index, dato in enumerate(autosCoordenadas):
        patente: str = autosCercanos[index][5]
        latitud = float(dato[2])
        longitud = float(dato[3])
        if cercano_al_estadio(boca[0], boca[1], latitud, longitud) == True:
            print(f"Patente: {patente}\nCoordenadas: {latitud} , {longitud}")

    print("\nAutos cercanos al estadio de River: \n")

    for index, dato in enumerate(autosCoordenadas):
        patente: str = autosCercanos[index][5]        
        latitud = float(dato[2])
        longitud = float(dato[3])
        if cercano_al_estadio(river[0], river[1], latitud, longitud) == True:
            print(f"Patente: {patente}\nCoordenadas: {latitud} , {longitud}")

    volver_a_menu: str = input("Presione ENTER para volver al menu")


def verSiEsRobado(listaDeRobados:list, datosProcesados: str) -> None:
    """
    Pre: Recibe una lista con patentes que pertenecen a autos con pedido de captura y una ruta a un archivo con extensión csv.
    Pos: Muestra en pantalla fecha, hora de la denuncia y ubicación del auto.
    """
    
    autosRobados: list = []
    formulario_robados:dict = {}
    autosDenunciados: list = []
    autosDenunciados = leerCSV(datosProcesados)


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

    volver_a_menu: str = input("Presione ENTER para volver al menu")
    


def consultarPatente(archivo1: str, archivo2: str) -> None:
    """
    Pre: Recibe dos rutas a archivos con extensión csv.
    Pos: Muestra en pantalla la foto del auto y la ubicación en un mapa.
    """
    consulta: dict = {'timestamp': '', 'latitud':'' , 'longitud': '', 'patente': '', 'rutaImagen':''}
    denuncias: list = []
    datosProcesados: list = []

    patente: str = str(input('Ingrese la patente que desea consultar de la siguiente manera AB 000 CD: '))  
    patente_valida: bool = bool(validar_patente(patente+' ')) # El espacio (+' ') se agrego como solucion a un inconveniente al ingresar la patente

    while((patente_valida != True) and (patente != "N")):        
        patente: str = str(input('Patente invalida, por favor reingrese la patente con el formato AB 000 CD, N para salir: ')).upper()

    denuncias= leerCSV(archivo1)

    #hay que obtener la patente
    datosProcesados= leerCSV(archivo2)
    
    patentes: list = []

    for dato in datosProcesados:    
        patentes.append(dato[5])

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

    if patente not in patentes:   
        print('No se encontra ninguna denuncia')
    else:
        print('Esta es la patente consultada:\n', consulta)


def main() -> None:

    lista: list =[]
    robados: list = []
    lista = leerCSV('Denuncias.csv')   

    opcion: int= 1
    
    while(opcion!= 0):
        
        opcion= menu()

        if (opcion == 1):
            print('1- Procesar archivo de denuncias')
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
            variable:str = input('Desea continuar? S/N: ').upper()
            while variable == "S":
                consultarPatente('denuncias.csv', 'datosProcesados.csv')
                variable = input('Desea continuar? S/N: ').upper()

        elif (opcion == 6):
            print('6- Mostrar grafico de denuncias por mes')
            diccionario: dict = generar_diccionario(lista)
            graficar(diccionario)

        else: exit()


main()

