import pandas as pd
import geopandas as gpd
import numpy as np
import networkx as nx
from point_in_area import point_in_area
from Setu import distance # adjust name



class Graph(object):
    """
    ---
    """

    def __init__(self, prov_data, sei_data, com_areas_boundaries, *, \
                prov_serv = 'police_stations', sei_ind = 'Homicide rate'):
        """
        Constructor. Creates the object, by defining its basic attributes,
            notably, the dataframe with attributes for each community area.
        """

        NUMBER_OF_SEI = 10



        prov_centers = pd.read_csv(prov_data, usecols = \
                                   ['ADDRESS', 'coords', 'type'])
        prov_centers = prov_centers[prov_centers.type == prov_serv] 
        prov_centers[['Latitude', 'Longitude']] = prov_centers['coords'].apply(\
            lambda x: pd.Series(str(x).strip('()').split(',')))
        self.prov_centers = prov_centers

        # Create geoseries for provision_centers
        #   Actually, better include the GeoSeries of Points as a new col. Vid infra doubt...




        df = pd.read_csv(sei_data, usecols = \
                        ['Name', 'GEOID', 'Longitude', 'Latitude', 'indicator', \
                         'value'])    # Confirm with Setu's csv
        df = df[df['indicator'] == sei_ind]
        self.df = df

        com_areas = open(com_areas_boundaries)
        self.com_areas = gpd.read_file(com_areas)  # This should be included in df_extended as a col. Possible to include GeoSeries in DataFrame?


        df_extended = df
        df_extended['Tensioned'] = df_extended['indicator'].apply(\
            lambda x: 1 if x.nlargest(NUMBER_OF_SEI, 'value') else 0)
        df_extended['Prov_within'] = df['Boundaries'].apply(lambda x: 1 if point_in_area(<prov_centers_GeoSeries>, x) else 0)
        self.df_extended = df_extended


    
        pass



    def gen_adjacency_graph(self, ):
        """
        Generates the graph that models the city of Chicago as a network of 
            community areas, where connected nodes are bordering areas. The value
            of each node indicates whether the community area is near a police 
            station and whether it is tensioned (top10 in homicide rate). 
        Parameters:
        Returns
        """

        graph = nx.Graph()
        # Iterate over the districts and add them as nodes to the graph
        for i, _ in self.com_areas.iterrows():
            G.add_node(i)

        # Iterate over the districts again and check which ones are neighboring
        for i, com in self.com_areas.iterrows():
            for j, other_com in self.com_areas.iterrows():
                if i == j:
                    continue
                if com.geometry.touches(other_com.geometry):
                    G.add_edge(i, j)        
        # Include labels

        pass


    def apply_shock(self, ):
        """
        Creates a diagonal matrix for modelling either a negative shock in the 
            amount of provision or a change in tensionned census tracts. Each 
            element of the diagonal incorporates the value of the shock for each
            census tract. Applies the shock by multiplying the adjacency matrix
            to this shock matrix.
            the shock by  
        Parameters:
        Returns        
        """

