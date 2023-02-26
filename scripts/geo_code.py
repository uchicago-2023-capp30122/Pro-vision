import googlemaps
import csv
from datetime import datetime
from traveltimepy import Driving, Coordinates, TravelTimeSdk

# hide key
api_key = "AIzaSyABteA2oGa6yJK1u92PAvbKhcpMiiE21w8"
gmaps = googlemaps.Client(key=api_key)
sdk = TravelTimeSdk(
    app_id="f9571a60", api_key="4caa1f5a4b29f582b455df38a1004541", limit_per_host=4
)

#add delay to geocode
def geocode(address):
    geocode_result = gmaps.geocode(address)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    long = geocode_result[0]["geometry"]["location"]["lng"]
    return (lat, long)


def isochrone(coords, address):
    if coords is None:
        coords = geocode(address)
    alat, along = coords
    result = sdk.time_map(
        coordinates=[Coordinates(lat=alat, lng=along)],
        departure_time=datetime.now(),
        transportation=Driving(),
        travel_time=600,
    )
    return result
