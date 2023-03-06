import requests
import json
import os
travel_time_key = os.environ.get('TT_API_KEY')

travel_time_id = os.environ.get('TT_API_ID')
URL = 'https://api.traveltimeapp.com/v4/time-map'
def create_request(coords, pkey):
    lat, lng = coords
    data = {
        "departure_searches": [
            {
                "id": pkey,
                "coords": {
                    "lat": lat,
                    "lng": lng
                },
                "transportation": {
                    "type": "driving"
                },
                "departure_time": "2023-03-04T09:00:00Z",
                "travel_time": 600,
                "reachable_postcodes_threshold": 4
            }
        ]
    }
    return data

def get_isochrones(coords, pkey):
    data = create_request(coords, pkey)
    response = requests.post(URL, headers=headers, json=data)
    return response.text

headers = {
    "Content-Type": "application/json",
    "X-Application-Id": '1b17a2b4',
    'Accept': 'application/geo+json',
    "X-Api-Key": '20882cb7789cee2a0adb02cb0c0db4ff',
}

def merge_geojson(dataframe):
    gp_iso = dict(tuple(dataframe.groupby('type')))
    merged_geo = {}
    for prov, prov_df in gp_iso.items():
        merged_geo[prov] = []
        #for geom in prov_df['isochrones']:
        for idx, geom in prov_df['isochrones'].iteritems():
            shape = json.loads(geom)
            shape['features'][0]['properties']['full_address'] = prov_df.loc[idx, 'full_address']
            shape['features'][0]['properties']['coords'] = prov_df.loc[idx, 'coords']
            merged_geo[prov].extend(shape['features'])
    return merged_geo
#FIX THIS
        
# for prov, geoj in merged_geo.items():
#     combined_geoj[prov] = geojson.FeatureCollection(geoj)