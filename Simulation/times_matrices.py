from datetime import datetime

from traveltimepy import Location, Coordinates, PublicTransport, Property, FullRange, TravelTimeSdk


def get_distances(Network, *, \
    dep_time = datetime.now(),
    lim_time = 600,
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


    com_areas = Network.df.to_dict(orient = 'records')
    prov_cens = Network.prov_centers.to_dict(orient = 'records')
    locations_com = []
    locations_com_traveltime = []
    for com in com_areas:
        com['id'] = com.pop('Name')
        com['coords'] = {'lat': com['Latitude'], 'lng': com['Longitude']}
        del com['GEOID']
        del com['Latitude']
        del com['Longitude']
        del com['indicator']
        del com['value']
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
    for com in locations_prov:
        key = com['id']
        times[key] = sdk.time_filter(\
            locations = locations_com_traveltime + locations_prov_traveltime, \
            search_ids = {com['id']: [prov['id'] for prov in locations_prov]}, \
            departure_time = dep_time, \
            travel_time = lim_time, \
            transportation = PublicTransport(type = mode), \
            properties = [Property.TRAVEL_TIME], \
            full_range = FullRange(enabled = False) \
        )

    return times   # recall: this is a dictionary, where each com_area name is the key and the value is the list of TravelTime objects with the time dist from this com_area to all police stations 
