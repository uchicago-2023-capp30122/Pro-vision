from datetime import datetime
from traveltimepy import Driving,Coordinates, TravelTimeSdk
from geo_code import *
#make api id and key private before pushing
sdk = TravelTimeSdk(app_id='f9571a60', api_key='4caa1f5a4b29f582b455df38a1004541', limit_per_host=4)
def isochrone(directory):
    iso_dict ={}
    for cat,addresses in directory.items():
        iso_dict[cat]=[]
        for address in addresses:
            add,alat,along = address
            result = sdk.time_map(
                coordinates = [Coordinates(lat = alat, lng = along)],
                departure_time=datetime.now(),
                transportation=Driving(),
                travel_time = 900
            )
            iso_dict[cat].append((add,result))
    return iso_dict
