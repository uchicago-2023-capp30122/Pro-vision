


def build_requests(Graph, *, \
    departure_time = datetime.now(),
    travel_time = 600,
    transportation = 'driving',
    properties = 'travel_time'):
    """
    Generates the parameters for the two needed TravelTime requests.
    Parameters:
    Returns
    """


    # Com area to com area

    locations_to_comareas = Graph.df.to_dict(orient = 'records')
    for com in locations_to_comareas:
        com['id'] = com.pop('Name')
        com['coords'] = {'lat': com['Latitude'], 'lng': com['Longitude']}
        del com['GEOID']
        del com['Latitude']
        del com['Longitude']
        del com['indicator']
        del com['value']


    # It is better to have all in 1
    search_ids_to_comareas = []
    


    # Com area to police station

    locations_to_provcen = Graph.prov_centers.to_dict(orient = 'records')
    search_ids_to_provcen = []
