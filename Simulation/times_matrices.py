from datetime import datetime
import pandas as pd
from traveltimepy import Location, Coordinates, Property, TravelTimeSdk, Driving
import json


def get_distances(prov_data, sei_data, *, \
    dep_time = datetime.now(),
    lim_time = 14400):
    """
    Uses TravelTime API to get the distances from each community area to each
    provision center.
    Parameters:
    Returns
    """

    APP_ID = '9548a652'
    APP_KEY = '7b839b683b5832a21b5becacce8b1698'

    sdk = TravelTimeSdk(app_id = APP_ID, api_key = APP_KEY)


    prov_centers_df = inputs_for_locations(prov_data, sei_data)['prov_centers']
    com_areas_df = inputs_for_locations(prov_data, sei_data)['com_areas']

    com_areas = com_areas_df.to_dict(orient = 'records')
    prov_cens = prov_centers_df.to_dict(orient = 'records')
    locations_com = []
    locations_com_traveltime = []
    for com in com_areas:
        com['id'] = com.pop('community_area')
        com['coords'] = {'lat': com['latitude'], 'lng': com['longitude']}
        del com['latitude']
        del com['longitude']
        del com['type']
        locations_com.append(com)
        locations_com_traveltime.append(\
            Location(id = com['id'], \
            coords = Coordinates(\
                lat = com['coords']['lat'], lng = com['coords']['lng'])))
    locations_prov = []
    locations_prov_traveltime = []
    for prov in prov_cens:
        prov['id'] = prov.pop('ADDRESS')
        prov['coords'] = {'lat': prov['Latitude'], 'lng': prov['Longitude']}
        del prov['type']
        locations_prov.append(prov)
        locations_prov_traveltime.append(\
            Location(id = prov['id'], \
            coords = Coordinates(\
                lat = prov['coords']['lat'], lng = prov['coords']['lng'])))
    

    times_dict = {}
    for com in locations_com:
        key = com['id']
        times_dict[key] = sdk.time_filter(\
            locations = locations_com_traveltime + locations_prov_traveltime, \
            search_ids = {com['id']: [prov['id'] for prov in locations_prov]}, \
            departure_time = dep_time, \
            travel_time = lim_time, \
            transportation = Driving(), \
            properties = [Property.TRAVEL_TIME], \
        )


    times_list = []
    for _, com in times_dict.items():
        for output_com in com:
            times_list.append(dict(output_com))


    times_clean = {}
    for com in times_list:
        com_key = com['search_id']
        dummy_dic = {}
        for prov in com['locations']:
            prov_dic = dict(prov)
            prov_key = prov_dic['id']
            i = dict(prov_dic['properties'][0])
            time = i['travel_time']
            dummy_dic[prov_key] = time
        times_clean[com_key] = dummy_dic


    with open('Dist_from_com_areas_to_prov_centers.json', 'w') as outfile:
        json.dump(times_clean, outfile)
    




def inputs_for_locations(prov_centers, com_areas, *, \
                         prov_serv = 'police_stations', sei_ind = 'homicide in community areas'):
    """
    ---
    """

    prov_centers = prov_centers[prov_centers['type'] == prov_serv] 
    prov_centers[['Latitude', 'Longitude']] = prov_centers['coords'].apply(\
        lambda x: pd.Series(str(x).strip('()').split(','))).astype(float)


    com_areas = com_areas[com_areas['type'] == sei_ind]

    return {'prov_centers': prov_centers, 'com_areas': com_areas}
