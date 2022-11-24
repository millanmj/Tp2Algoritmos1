import csv
datos:list = []

with open("Denuncias.csv", newline='', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter=',')
        next(csv_reader) 
        for linea in csv_reader:
            datos.append(linea)



for n in datos:
    #print("denuncia número {}".format(list(n+1)))
    print("timestamp: ", n[0])
    print("número: ", n[1])
    print("Coordenadas latitud: ",n[2])
    print("Coordenadas longitud: ", n[3])
    print("ruta foto: ", n[4])
    print("Descripcion texto: ", n[5])
    print("ruta audio: ", n[6])
    print("------------------------------------------")