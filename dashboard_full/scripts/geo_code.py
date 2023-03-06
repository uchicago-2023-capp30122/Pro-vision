import os
import time
from datetime import datetime
import googlemaps
from traveltimepy import Driving, Coordinates, TravelTimeSdk
from geojson import Polygon, Feature

alt_id = os.environ.get("TT_API_ID")
alt_key = os.environ.get("TT_API_KEY")
api_key = os.environ.get("GKEY")
gmaps = googlemaps.Client(key=api_key)
sdk = TravelTimeSdk(app_id=alt_id, api_key=alt_key, limit_per_host=4)


def geocode(address):
    """
    Map an address(string) to its coordinates

    Inputs:
    address: string value

    Returns:
    tuple of coordinates
    """
    time.sleep(1)
    geocode_result = gmaps.geocode(address)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    long = geocode_result[0]["geometry"]["location"]["lng"]
    return (lat, long)


def fetch_isochrone(coords, address):
    """
    Use the traveltimepy SDK to fetch isochrone geometry for a set of coordinates
    or address

    Inputs:
    coords: coordinates of provisions
    address: address of provisions

    Output:
    A list of TravelTime objects
    """
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
    """
    extract the isochrone geometry from SDK response

    Inputs:
    coords: coordinates of provisions
    address: address of provisions

    Output:
    list of geoJSON features
    """
    response = fetch_isochrone(coords, address)
    geoms = []
    for res in response:
        shapes = res.shapes
        for shape in shapes:
            coords = shape.shell
            feature = Feature(
                geometry=Polygon([[(coord.lng, coord.lat) for coord in coords]])
            )
            geoms.append(feature)
    return geoms
