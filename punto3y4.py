from math import radians, cos, sin, asin, sqrt

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Formula del semiverseno: Calcula la distancia en kilometros entre 2 puntos de la tierra
    """
    # convertir grados a radianes
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radio de la tierra en km
    return c * r

def cercano_al_estadio(latitud1: float, longitud1: float, latitud2: float, longitud2: float) -> bool:
    """
    Devuelve True si la distancia del auto al estadio es menor a 1km
    """
    distancia: float = haversine(latitud1, longitud1, latitud2, longitud2)
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