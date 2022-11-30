from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="example app")
direc_1 = geolocator.geocode("Tucuman 1330, Buenos Aires, Argentina")
direc_1 = direc_1.latitude, direc_1.longitude
print(direc_1)#Recoleta