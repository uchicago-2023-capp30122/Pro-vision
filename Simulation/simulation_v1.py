import pandas as pd
import numpy as np
import networkx as nx


def create_graph(prov_serv, socioecon_vulner, n):
    """
    ---
    """

    return nx.Graph(process_data(prov_serv, socioecon_vulner, n)['array'])


def process_data(prov_data, prov_serv, sei_data, sei_ind, n):
    """
    ---
    """
    provision = pd.read_csv(prov_data, usecols = ['coords', 'type'])
    provision = provision[provision.type == prov_serv] 
    provision[['Latitude', 'Longitude']] = provision['coords'].apply(lambda x: pd.Series(str(x).strip('()').split(',')))

    tension = pd.read_csv(sei_data, usecols = ['Longitude', 'Latitude', 'indicator', 'value'])
    tension = tension[tension.indicator == sei_ind].nlargest(n, 'value')

    # Gen adjacency array (helper function)
    rows_tension = []
    rows_provision = []
    for i in range(len(provision.index) + n):
        if i < n:
            rows_tension.append(0)
            rows_provision.append(1)
        else:
            rows_tension.append(1)
            rows_provision.append(0)
    
    array = []
    for _ in range(n):
        array.append(rows_tension)
    for _ in range(len(provision.index)):
        array.append(rows_tension)


    # Gen indices of distances (helper function)



    output = {}
    output['array'] = np.array(array)