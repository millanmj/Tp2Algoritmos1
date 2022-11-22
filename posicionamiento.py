from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="example app")
v = geolocator.geocode("larrea 1230,Buenos Aires, Argentina")
print(v.latitude, v.longitude)
