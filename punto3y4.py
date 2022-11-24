from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def boca(latitud: float, longitud: float) -> bool:
    """
    Devuelve True si la distancia del punto a la cancha de Boca es menor a 1km
    """
    distancia: float = haversine(-34.635614, -58.364669, latitud, longitud)
    if distancia < 1.0:
        return True
    else:
        return False

def river(latitud: float, longitud: float) -> bool:
    """
    Devuelve True si la distancia del punto a la cancha de River es menor a 1km
    """
    distancia: float = haversine(-34.545290, -58.449740, latitud, longitud)
    if distancia < 1.0:
        return True
    else:
        return False

def pertenece_al_cuadrante(latitud: float, longitud: float) -> bool:
    """
    Devuelve True si la coordenada se encuentra en el cuadrante
    """
    norte: float = -34.599609 # Cordoba
    sur: float = -34.609226 # Rivadavia
    este: float = -58.370162 # Alem
    oeste: float = -58.392951 # Callao

    if latitud < norte and latitud > sur:
        if longitud < este and longitud > oeste:
            return True
    return False

# test
# print(pertenece_al_cuadrante(-34.585642, -58.439767))
# print(pertenece_al_cuadrante(-34.607064, -58.381523))
# print(boca(-34.548316, -58.455670))
# print(boca(-34.633035, -58.358510))
# print(river(-34.548316, -58.455670))
# print(river(-34.633035, -58.358510))