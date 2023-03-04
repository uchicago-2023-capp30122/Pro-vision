import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, LineString, Point
import numpy as np
import networkx as nx
import urllib.request, json
from point_in_area import point_in_area
import matplotlib.pyplot as plt
import random



class Network(object):
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
        com_bounds = gpd.read_file(urllib.request.urlopen(com_areas_boundaries))
        com_bounds = com_bounds[['geoid10', 'geometry']]


        prov_centers = pd.read_csv(prov_data, usecols = \
                                   ['ADDRESS', 'coords', 'type'])
        prov_centers = prov_centers[prov_centers['type'] == prov_serv] 
        prov_centers[['Latitude', 'Longitude']] = prov_centers['coords'].apply(\
            lambda x: pd.Series(str(x).strip('()').split(',')))
        prov_centers['coords_geo'] = prov_centers['coords'].apply(\
            lambda x: gpd.GeoSeries(Point(x)))
        self.prov_centers = prov_centers



        df = pd.read_csv(sei_data, usecols = \
                        ['Name', 'GEOID', 'Longitude', 'Latitude', 'indicator', \
                         'value'])    # Confirm with Setu's csv
        df = df[df['indicator'] == sei_ind]
        self.df = df

        df_extended = df
        df_extended['Tensioned'] = 0
        df_extended.loc[df_extended['value'] >= min(\
            df_extended.nlargest(NUMBER_OF_SEI, 'value')['value']), \
            'Tensioned'] = 1
        df_extended = df_extended.merge(\
            com_bounds, how = 'outer', left_on = 'GEOID', right_on = 'geoid10')
        df_extended.drop('geoid10', axis = 1, inplace = True) 
        df_extended['Prov_within'] = df['geometry'].apply(\
            lambda x: 1 if point_in_area(self.prov_centers['coords_geo'], x) else 0)
        
        # Include 1 col for each pol station, to have the distance between this and the com_area
        df_extended['Min_dist'] = df_extended[[]].apply(min, axis = 1)  # Complete with the missing cols
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

        G = nx.Graph()
        # Iterate over the districts and add them as nodes to the graph, with the label
        for _, com in self.df_extended.iterrows():
            if com['Tensioned'] == 1 and com['Prov_within'] == 1:
                G.add_node(com['Name'], tensioned = 1, prov = 1)
            elif com['Tensioned'] == 1 and j['Prov_within'] == 0:
                G.add_node(com['Name'], tensioned = 1, prov = 0)
            elif com['Tensioned'] == 0 and j['Prov_within'] == 1:
                G.add_node(com['Name'], tensioned = 0, prov = 1)
            else:
                G.add_node(com['Name'], tensioned = 0, prov = 0)

        # Iterate over the districts again and check which ones are neighboring.
        #   EXTREMELY EXPENSIVE!! num_iter = (77!/2)-77
        for i, com in self.df_extended.iterrows():
            for j, other_com in self.df_extended.iterrows():
                if i < j and com['geometry'].touches(other_com['geometry']):
                    G.add_edge(com['Name'], other_com['Name'])        

        self.model = G
        
        # Include the savefile as in demo_nx 

        pass



        # Some issues to be solved here:
            # to create the nodes, we can avoid the ugly for loop
            # we have to avoid the nested for loop. Options:
            #   investigate whether another nx method
            #   Setu's new API
            #   clustering using lat 
            #   clustering using the GeoID (worst option)




    def apply_shock_com_areas(self, ):
        """
        Generates a random shock in the degree of tension for all the community 
            areas: the assignation of top-tensioned areas is stochastically 
            modified.
        Parameters:
        Returns        
        """

        self.df_shock_com = self.df_extended
        self.df_shock_com['Tensioned_sim'] = 0
        shock_rows = np.random.choice(\
            self.df_shock_com.index, size = 10, replace = False)
        self.df_shock_com.loc[shock_rows, 'Tensioned_sim'] = 1
        self.df_shock_com['Min_dist_shock'] = self.df_shock_com[[]].apply(min, axis = 1)  # Complete with the missing cols

        # Modify the graph label

        return self.df_shock_com



    def apply_shock_prov_centers(self, reduction = 0.2):
        """
        Generates a random shock in the set of provision centers: the number of
            operating centers is reduced by a factor and the eliminated centers
            are stochastically selected.
        Parameters:
        Returns        
        """

        self.df_shock_prov = self.df_extended
        prov_centers_all = list(self.self.df_extended.columns.values)
        prov_centers_shock = random.sample(prov_centers_all, \
                                           round(len(self.prov_centers)*(1-reduction)))

        self.df_shock_prov['Min_dist_shock'] = self.df_shock_prov[\
            prov_centers_shock].apply(min, axis = 1) 
        # For the node label: self.df_shock_prov['Prov_within_shock'] = 

        # Modify the graph label

        return self.df_shock_prov