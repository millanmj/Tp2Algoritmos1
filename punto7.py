import matplotlib.pyplot as plt
from datetime import datetime

def generar_diccionario(lista):
    meses = []
    for i in lista:
        date = datetime.fromtimestamp(int(float(i[0])))
        mes = date.strftime("%m")
        meses.append(mes)

    numero_a_mes = {"1":"Enero", "2":"Febrero", "3":"Marzo", "4":"Abril", "5":"Mayo", "6":"Junio", "7":"Julio", "8":"Agosto", "9":"Septiembre", "10":"Octubre", "11":"Noviembre", "12":"Diciembre"}
    denuncias_por_mes = {"Enero":0,"Febrero":0, "Marzo":0, "Abril":0, "Mayo":0, "Junio":0, "Julio":0, "Agosto":0, "Septiembre":0, "Octubre":0, "Noviembre":0, "Diciembre":0}

    for i in meses:
        denuncias_por_mes[numero_a_mes[i]] += 1

    return denuncias_por_mes

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

def graficar(diccionario):
    names = list(diccionario.keys())
    values = list(diccionario.values())

    plt.figure(figsize=(12, 5))  # dimensiones del grafico (ancho, alto)
    plt.bar(range(len(diccionario)), values, tick_label=names)
    addlabels(range(len(diccionario)), values)
    plt.title("Denuncias por mes")
    plt.xlabel("Meses")
    plt.ylabel("Denuncias")
    plt.show()
