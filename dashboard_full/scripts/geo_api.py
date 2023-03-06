import json
import os
import requests

# Fetching environment variables
travel_time_key = os.environ.get("TT_API_KEY")
travel_time_id = os.environ.get("TT_API_ID")
URL = "https://api.traveltimeapp.com/v4/time-map"


def create_request(coords, pkey):
    """
    Create request for TravelTime API to get isochrones

    Inputs:
    coords: coordinates of provision
    pkey: unique identifier for each provision

    Output:
    a JSON object
    """
    lat, lng = coords
    data = {
        "departure_searches": [
            {
                "id": pkey,
                "coords": {"lat": lat, "lng": lng},
                "transportation": {"type": "driving"},
                "departure_time": "2023-03-04T09:00:00Z",
                "travel_time": 600,
                "reachable_postcodes_threshold": 4,
            }
        ]
    }
    return data


def get_isochrones(coords, pkey):
    """
    Create request and post results of request
    Inputs:
    coords: coordinates of provision
    pkey: unique identifier

    Output:
    text element of request response
    """
    data = create_request(coords, pkey)
    response = requests.post(URL, headers=headers, json=data, timeout=30)
    return response.text


headers = {
    "Content-Type": "application/json",
    "X-Application-Id": "1b17a2b4",
    "Accept": "application/geo+json",
    "X-Api-Key": "20882cb7789cee2a0adb02cb0c0db4ff",
}


def merge_geojson(dataframe):
    """
    Merge geoJSONs corresponding to isochrones of access points to one geoJSON
    per provision category

    Inputs:
    dataframe: pandas dataframe

    Output:
    A dictionary object with provision type as key and merged geoJSON for all
    provisions of that type as values
    """
    gp_iso = dict(tuple(dataframe.groupby("type")))
    merged_geo = {}
    for prov, prov_df in gp_iso.items():
        merged_geo[prov] = []
        for idx, geom in prov_df["isochrones"].iteritems():
            shape = json.loads(geom)
            shape["features"][0]["properties"]["full_address"] = prov_df.loc[
                idx, "full_address"
            ]
            shape["features"][0]["properties"]["coords"] = prov_df.loc[idx, "coords"]
            merged_geo[prov].extend(shape["features"])
    return merged_geo
