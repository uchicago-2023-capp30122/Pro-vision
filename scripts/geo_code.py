import googlemaps
import time
from datetime import datetime
from traveltimepy import Driving, Coordinates, TravelTimeSdk
from geojson import Polygon
from geojson import Feature
alt_id = '1b17a2b4'
alt_key = '20882cb7789cee2a0adb02cb0c0db4ff'
# hide key
api_key = "AIzaSyABteA2oGa6yJK1u92PAvbKhcpMiiE21w8"
gmaps = googlemaps.Client(key=api_key)
sdk = TravelTimeSdk(
    # app_id="f9571a60", api_key="4caa1f5a4b29f582b455df38a1004541", limit_per_host=4
    app_id= alt_id, api_key= alt_key, limit_per_host=4
)

def geocode(address):
    time.sleep(1)
    geocode_result = gmaps.geocode(address)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    long = geocode_result[0]["geometry"]["location"]["lng"]
    return (lat, long)

def fetch_isochrone(coords, address):
    time.sleep(1)
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

def isochrone_geometry(coords, address):
    response = fetch_isochrone(coords, address)
    geoms = []
    for res in response:
        shapes = res.shapes
        for shape in shapes:
            coords = shape.shell
            feature = Feature(geometry=Polygon([[(coord.lng, coord.lat) for coord in coords]]))
            geoms.append(feature)
    return geoms

