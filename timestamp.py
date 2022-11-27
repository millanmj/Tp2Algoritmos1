from datetime import datetime
def mostrar_timestamp (fecha) -> None:
    print(("timestamp is: ",fecha))

#CREACIÓN DE REGISTROS DE TIEMPO PARA DENUNCIAS

def main():
    fecha_1 = datetime(2022,11,5,15,23,20)
    ts_1 = datetime.timestamp(fecha_1)
    denuncia1 = mostrar_timestamp(ts_1)

    fecha_2 = datetime(2022,11,7,14,33,20)
    ts_2 = datetime.timestamp(fecha_2)
    denuncia2 = mostrar_timestamp(ts_2)

    fecha_3 = datetime(2022,11,20,21,23,20)
    ts_3 = datetime.timestamp(fecha_3)
    denuncia3 = mostrar_timestamp(ts_3)

    fecha_4 = datetime(2022,11,22,16,40,10)
    ts_4 = datetime.timestamp(fecha_4)
    denuncia4 = mostrar_timestamp(ts_4)

    fecha_5 = datetime(2022,11,5,22,23,20)
    ts_5 = datetime.timestamp(fecha_5)
    denuncia5 = mostrar_timestamp(ts_5)

    fecha_6 = datetime(2022,11,23,22,45,20)
    ts_6 = datetime.timestamp(fecha_6)
    denuncia6 = mostrar_timestamp(ts_6)

    fecha_7 = datetime(2022,11,27,9,23,20)
    ts_7 = datetime.timestamp(fecha_7)
    denuncia7 = mostrar_timestamp(ts_7)
    
    fecha_8 = datetime(2022,11,15,12,23,20)
    ts_8 = datetime.timestamp(fecha_8)
    denuncia8 = mostrar_timestamp(ts_8)
    
    fecha_9 = datetime(2022,11,12,23,23,20)
    ts_9 = datetime.timestamp(fecha_9)
    denuncia9 = mostrar_timestamp(ts_9)
    
    fecha_10 = datetime(2022,11,11,14,23,20)
    ts_10 = datetime.timestamp(fecha_10)
    denuncia10 = mostrar_timestamp(ts_10)

    fecha_11 = datetime(2022,11,12,20,54,10)
    ts_11 = datetime.timestamp(fecha_11)
    denuncia11 = mostrar_timestamp(ts_11)


    






main()