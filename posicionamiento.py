from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="example app")
direc_1 = geolocator.geocode("larrea 1230,Buenos Aires, Argentina")
direc_1 = direc_1.latitude, direc_1.longitude
print(direc_1)#Recoleta
direc_2 = geolocator.geocode("Talcahuano 932,Buenos Aires, Argentina")
direc_2 = direc_2.latitude, direc_2.longitude
print(direc_2)#Tribunales
direc_3 = geolocator.geocode("Beruti 2857,Buenos Aires, Argentina")
direc_3 = direc_3.latitude, direc_3.longitude
print(direc_3)#Recoleta
direc_4 = geolocator.geocode("Juana Manso 1636,Buenos Aires, Argentina")
direc_4 = direc_4.latitude, direc_4.longitude
print(direc_4)#Puerto Madero
direc_5 = geolocator.geocode("lavalle 2666,ciudad autonoma de Buenos Aires, Argentina")
direc_5 = direc_5.latitude, direc_5.longitude
print(direc_5)#Balvanera
direc_6 = geolocator.geocode(" Av. Cabildo 4029,ciudad autonoma de Buenos Aires, Argentina")
direc_6 = direc_6.latitude, direc_6.longitude
print(direc_6)#Saavedra
direc_7 = geolocator.geocode(" Ernesto A. Bavio 3164,ciudad autonoma de Buenos Aires, Argentina")
direc_7 = direc_7.latitude, direc_7.longitude
print(direc_7)#River
direc_8 = geolocator.geocode(" Ernesto A. Bavio 2977,ciudad autonoma de Buenos Aires, Argentina")
direc_8 = direc_8.latitude, direc_8.longitude
print(direc_8)#River
direc_9 = geolocator.geocode("Rafael Hernandez 2939,ciudad autonoma de Buenos Aires, Argentina")
direc_9 = direc_9.latitude, direc_9.longitude
print(direc_9)#River
direc_10 = geolocator.geocode("Brandsen 1420,ciudad autonoma de Buenos Aires, Argentina")
direc_10 = direc_10.latitude, direc_10.longitude
print(direc_10)#Boca
direc_11 = geolocator.geocode("Pinzón 1101,ciudad autonoma de Buenos Aires, Argentina")
direc_11 = direc_11.latitude, direc_11.longitude
print(direc_11)#Boca
