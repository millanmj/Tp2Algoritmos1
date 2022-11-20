import csv

datos: list = []

with open("csvRead.csv", newline='', encoding="UTF-8") as archivo_csv:
    csv_reader = csv.reader(archivo_csv, delimiter=',')
	#next(csv_reader) #Evitamos leer el header
    for row in csv_reader:
        datos.append(row)
print(datos)