from datetime import datetime

from traveltimepy import Location, Coordinates, PublicTransport, Property, FullRange, TravelTimeSdk, Driving


def get_distances(origins_df, destinations_df, *, \
    dep_time = datetime.now(),
    lim_time = 14400,
    mode = 'driving'):
    """
    Uses TravelTime API to get the distances from each community area to each
    provision center.
    Parameters:
    Returns
    """

    APP_ID = '9548a652'
    APP_KEY = '7b839b683b5832a21b5becacce8b1698'

    sdk = TravelTimeSdk(app_id = APP_ID, api_key = APP_KEY)


    com_areas = origins_df.to_dict(orient = 'records')
    prov_cens = destinations_df.to_dict(orient = 'records')
    locations_com = []
    locations_com_traveltime = []
    for com in com_areas:
        com['id'] = com.pop('community_area')
        com['coords'] = {'lat': com['latitude'], 'lng': com['longitude']}
        del com['GEOID']
        del com['latitude']
        del com['longitude']
        del com['type']
        del com['value']
        del com['boundaries']
        del com['Tensioned']
        del com['geometry']
        del com['Prov_within']
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
        del prov['Latitude']
        del prov['Longitude']
        del prov['coords_geo']
        locations_prov.append(prov)
        locations_prov_traveltime.append(\
            Location(id = prov['id'], \
            coords = Coordinates(\
                lat = prov['coords']['lat'], lng = prov['coords']['lng'])))
    

    times = {}
    for com in locations_com:
        key = com['id']
        times[key] = sdk.time_filter(\
            locations = locations_com_traveltime + locations_prov_traveltime, \
            search_ids = {com['id']: [prov['id'] for prov in locations_prov]}, \
            departure_time = dep_time, \
            travel_time = lim_time, \
            transportation = Driving(), \
            properties = [Property.TRAVEL_TIME], \
        )

    for com, result in times.items():



    # return times   # recall: this is a dictionary, where each com_area name is the key and the value is the list of TravelTime objects with the time dist from this com_area to all police stations 
