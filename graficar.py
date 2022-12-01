import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def graficarMensual(denuncias: list) -> None:
    
    denunciasMes: dict = {'Enero': 0, 'Febrero': 0, 'Marzo': 0,
                          'Abril': 0, 'Mayo': 0, 'Junio': 0,
                          'Julio': 0, 'Agosto':0, 'Septiembre': 0,
                          'Octubre':0, 'Noviembre':0, 'Diciembre': 0}
    #tomar el mes del timestamp
    #dt_object = datetime.fromtimestamp(ts_11).month

    pass

#Definimos una lista con paises como string
paises = ['Estados Unidos', 'España', 'Mexico', 'Rusia', 'Japon']
#Definimos una lista con ventas como entero
ventas = [25, 32, 34, 20, 25]

fig, ax = plt.subplots()
#Colocamos una etiqueta en el eje Y
ax.set_ylabel('Ventas')
#Colocamos una etiqueta en el eje X
ax.set_title('Cantidad de Ventas por Pais')

#Creamos la grafica de barras utilizando 'paises' como eje X y 'ventas' como eje y.
plt.bar(paises, ventas)
plt.savefig('barras_simple.png')
#Finalmente mostramos la grafica con el metodo show()
plt.show()