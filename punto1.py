import csv
import os

from geopy.geocoders import Nominatim
from functools import partial


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
                    print("Descripcion texto: ", dato[5])
                    print("ruta audio: ", dato[6])
                    print("------------------------------------------")       

        
    except IOError: 
        print("No se encontró el archivo")   

    except:
            print("Ocurrio un error inesperado, por favor reintente mas tarde")    

    return datos
            

def obtenerDireccion(datos: list, latitud: float, longitud: float) -> list:  

    #ACA HAY QUE TOMAR LAS COORDENAS DEL ARCHIVO CSV ORIGINAL Y HACER LA CONSULTA CON GEOLOCATOR PARA OBTENER LA DIRECCION,
    #LOCALIDAD, PAIS ETC Y LO GUARDAMOS EN UNA LISTA QUE LUEGO ENVIAREMOS AL ARCHIVO DATOSPROCESADOS.CSV
    # reverse = partial(geolocator.reverse, language="es")
    # print(reverse("52.509669, 13.376294"))
    # geolocator = Nominatim(user_agent="example app")
    # direc_1 = geolocator.geocode("larrea 1230,Buenos Aires, Argentina")
    # direc_1 = direc_1.latitude, direc_1.longitude
    # print(direc_1)#Recoleta
    pass


def obtenerPatente(rutaImagen: str) -> str:
    pass


def convertirVozATexto() -> str:
    pass


def crearCsv(datos: list) -> None:

    try:
        #archivo = open('datosProcesados.csv', 'a')
        
        
        with open('datosProcesados.csv', 'w', newline='', encoding="UTF-8") as archivo_csv:
            csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"', quoting= csv.QUOTE_NONNUMERIC)

            csv_writer.writerow(["Timestamp", "Telefono", "Dirección", "Localidad", "Pais", "Patente", "Descripcion_en_txt",  "Descripcion_del_audio"]) 
            
            for dato in datos:
                timestamp: str = dato[0]
                telefono: str = dato[1]
                
                ubicacion= obtenerDireccion( dato[2], dato[3])

                direccion: str = "ubicacion.direccion ó segun como nos devuelva el dato geopy lo tomamos" 
                localidad:str = ''
                pais: str = ''
                patente: str = ''
                descripcion_en_txt: str = ''
                descripcion_del_audio: str = ''
            
                         
                csv_writer.writerow((timestamp, telefono, direccion, localidad, pais, patente, descripcion_en_txt, descripcion_del_audio))
            
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
crearCsv(lista)
