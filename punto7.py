import matplotlib.pyplot as plt
from datetime import datetime

def generar_diccionario(lista: list) -> dict:
    """
    Pre: Recibe una lista vacia.
    Pos: Devuelve un diccionario con los meses del año como keys y la cantidad de denuncias por mes como value.
    """
    
    meses: list = []
    for i in lista:
        date = datetime.fromtimestamp(int(float(i[0]))) #Transforma el timestamp de Denuncias.csv datetime
        mes = date.strftime("%m") #11 Saca el numero de mes       
        meses.append(mes) # [1,2,5,6,11,11,11,11,11,11] Crea la lista del mes de cada denuncia
 
         
    numero_a_mes = {"01":"Enero", "02":"Febrero", "03":"Marzo", "04":"Abril", "05":"Mayo", "06":"Junio", "07":"Julio", "08":"Agosto", "09":"Septiembre", "10":"Octubre", "11":"Noviembre", "12":"Diciembre"}
    denuncias_por_mes = {"Enero":0,"Febrero":0, "Marzo":0, "Abril":0, "Mayo":0, "Junio":0, "Julio":0, "Agosto":0, "Septiembre":0, "Octubre":0, "Noviembre":0, "Diciembre":0}

    #Conversión de mes numerico a mes Enero, Febrero, etc..
    for i in meses:
        denuncias_por_mes[numero_a_mes[i]] += 1

    return denuncias_por_mes


def addlabels(x,y) -> None:
    """
    Pre: Recibe coordenadas X e Y.
    Pos: Define las coordenadas X e Y en el gráfico.
    """

    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')


def graficar(diccionario: dict) -> None:
    """
    Pre: Recibe el diccionario retornado por la funcion generar_diccionario.
    Pos: Devuelve el gráfico ya terminado con sus respectivos datos; Meses del año en X y Cantidad de denuncias por mes en Y.
    """

    names = list(diccionario.keys())
    values = list(diccionario.values())

    plt.figure(figsize=(12, 5))  # dimensiones del grafico (ancho, alto)
    plt.bar(range(len(diccionario)), values, tick_label=names)#sobre x
    addlabels(range(len(diccionario)), values)
    plt.title("Denuncias por mes")
    plt.xlabel("Meses")
    plt.ylabel("Denuncias")
    plt.show()

