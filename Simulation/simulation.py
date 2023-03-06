import pandas as pd
import geopandas as gpd
from shapely import wkt, geometry
import numpy as np
import networkx as nx
import urllib.request, json
import matplotlib.pyplot as plt
from matplotlib import use
import random
import utils
import copy


class Network(object):
    """
    ---
    """

    def __init__(self, prov_data, sei_data, com_areas_boundaries, distances, *, \
                prov_serv = 'police_stations', sei_ind = 'homicide in community areas'):
        """
        Constructor. Creates the object, by defining its basic attributes,
            notably, the dataframe with attributes for each community area.
        """

        NUMBER_OF_SEI = 10

        prov_centers = pd.read_csv(prov_data, usecols = \
                                   ['ADDRESS', 'coords', 'type'])
        prov_centers = prov_centers[prov_centers['type'] == prov_serv] 
        prov_centers[['Latitude', 'Longitude']] = prov_centers['coords'].apply(\
            lambda x: pd.Series(str(x).strip('()').split(','))).astype(float)
        prov_centers['coords'] = prov_centers[['Latitude', 'Longitude']].apply(tuple, axis=1)
        prov_centers['coords'] = prov_centers['coords'].apply(utils.switch_tuple_order)    # Bug: doesn't read utils.py
        prov_centers['coords_geo'] = gpd.GeoSeries(prov_centers['coords'].apply(\
            lambda x: geometry.Point(x)))
        self.prov_centers = prov_centers.copy(deep = True)


        # com_bounds = gpd.read_file(urllib.request.urlopen(com_areas_boundaries))
        # com_bounds = com_bounds[['geoid10', 'geometry']]
        df = pd.read_csv(sei_data, usecols = \
                        ['community_area', 'GEOID', 'longitude', 'latitude', 'type', \
                         'value', 'boundaries']) 
        df = df[df['type'] == sei_ind]

        df['Tensioned'] = 0
        df.loc[df['value'] >= min(\
            df.nlargest(NUMBER_OF_SEI, 'value')['value']), \
            'Tensioned'] = 1

        df['geometry'] = df['boundaries'].apply(lambda x: wkt.loads(x))
        df['Prov_within'] = df['geometry'].apply(\
            lambda x: 1 if utils.point_in_area(self.prov_centers['coords_geo'], x) else 0)     # Bug: doesn't read utils.py
        

        # Open JSON
        f = open('Times_from_com_areas_to_prov_centers.json')
        times_dict = json.load(f)
        times_df = pd.DataFrame.from_dict(times_dict, orient = 'index')
        num_prov_centers = len(times_df)
        times_df['names'] = times_df.index
        
        # Merge with df
        df = df.merge(\
            times_df, how = 'outer', left_on = 'community_area', right_on = 'names')
        df.drop('names', axis = 1, inplace = True)

        df['Min_dist'] = df[df.columns[-num_prov_centers:]].apply(min, axis = 1)  # ALTERNATIVE: df['Min_dist'] = df[[]].min(axis = 1)
        self.df = df.copy(deep = True)
  
        table_statu_quo = df[df['Tensioned'] == 1]
        self.table_statu_quo = table_statu_quo[['community_area', 'Min_dist']]




    def gen_adjacency_graph(self, ):
        """
        Generates the graph that models the city of Chicago as a network of 
            community areas, where connected nodes are bordering areas. The value
            of each node indicates whether the community area is near a police 
            station and whether it is tensioned (top10 in homicide rate). 
        Parameters:
        Returns
        """

        
        list_of_neighbours = list(output_from_API_as_df[['src_MyCode', 'nbr_MyCode']].itertuples(index = False, name = None))
            # The output of this is a list of tuples, where each tuple is a pair of neighbours
        

        G = nx.Graph(list_of_neighbours)
            # The output of this is the adjacency graph: nodes and edges.
            # Alternative: 1- Create void graph, 2- Graph.add_nodes_from(df['Name'], **attr)
        

        attrs = {}   # This can be done without a for loop
        for _, com in self.df.iterrows():
            label = {'Tensioned': com['Tensioned'], 'Prov_within': com['Prov_within']}
            key = com['Name']
            attrs[key] = label

        nx.set_node_attributes(G, attrs)    

        # for debugging: nx.get_node_attributes(G, "Tensioned")[<node name>]
        # idem: https://networkx.guide/functions/attributes/basics/

        self.G = copy.deepcopy(G)
        
        use('agg')
        pos = nx.spring_layout(G, seed=225)  # Seed for reproducible layout
        nx.draw(G, pos)
        plt.show()   # https://networkx.guide/visualization
                     # https://networkx.org/documentation/stable/reference/drawing.html

        plt.savefig('network.png')

        pass



    def apply_shock_com_areas(self, ):
        """
        Generates a random shock in the degree of tension for all the community 
            areas: the assignation of top-tensioned areas is stochastically 
            modified.
        Parameters:
        Returns        
        """

        self.df_shock_com = self.df.copy(deep = True)
        self.df_shock_com['Tensioned_sim'] = 0
        shock_rows = np.random.choice(\
            self.df_shock_com.index, size = 10, replace = False)
        self.df_shock_com.loc[shock_rows, 'Tensioned_sim'] = 1
        self.df_shock_com['Min_dist_shock'] = self.df_shock_com[[]].apply(min, axis = 1)  # Complete with the missing cols


        # Modifies the graph label
        G_shock_com = copy.deepcopy(self.G)
        attrs = {}   # Probably to a helper function (if we maintain the for loop)
        for _, com in self.df_shock_com.iterrows():
            label = {'Tensioned': com['Tensioned_sim'], 'Prov_within': com['Prov_within']}
            key = com['Name']
            attrs[key] = label

        nx.set_node_attributes(G_shock_com, attrs)

        use('agg')
        pos = nx.spring_layout(G_shock_com, seed=225)  # Seed for reproducible layout
        nx.draw(G_shock_com, pos)
        plt.show()

        plt.savefig('network_shock_com.png')


        table_shock_com = self.df_shock_com[self.df_shock_com['Tensioned_sim'] == 1]
        self.table_shock_com = table_shock_com[['Name', 'Min_dist_shock']]

        # return {'df': self.df_shock_com, 'graph': G_shock_com}



    def apply_shock_prov_centers(self, reduction = 0.2):
        """
        Generates a random shock in the set of provision centers: the number of
            operating centers is reduced by a factor and the eliminated centers
            are stochastically selected.
        Parameters:
        Returns        
        """

        self.df_shock_prov = self.df.copy(deep = True)
        prov_centers_all = list(self.df.columns.values)  # Warning: not all cols, only the prov
        prov_centers_shock = random.sample(prov_centers_all, \
                                           round(len(self.prov_centers)*(1-reduction)))

        self.df_shock_prov['Min_dist_shock'] = self.df_shock_prov[\
            prov_centers_shock].apply(min, axis = 1)
        prov_cens_shock_df = self.prov_centers[self.prov_centers['Name'] == prov_centers_shock]  # 'Name' doesnot exist, wait for API output 
        self.df_shock_prov['Prov_within_shock'] = self.df_shock_prov['geometry'].apply(\
            lambda x: 1 if utils.point_in_area(prov_cens_shock_df['coords_geo'], x, prov_centers_shock) else 0)        


        # Modifies the graph label
        G_shock_prov = copy.deepcopy(self.G)
        attrs = {}   # Probably to a helper function (if we maintain the for loop)
        for _, com in self.df_shock_prov.iterrows():
            label = {'Tensioned': com['Tensioned'], 'Prov_within': com['Prov_within_shock']}
            key = com['Name']
            attrs[key] = label

        nx.set_node_attributes(G_shock_prov, attrs)  

        use('agg')
        pos = nx.spring_layout(G_shock_prov, seed=225)  # Seed for reproducible layout
        nx.draw(G_shock_prov, pos)
        plt.show()

        plt.savefig('network_shock_prov.png')


        table_shock_prov = self.df_shock_prov[self.df_shock_prov['Tensioned'] == 1]
        self.table_shock_prov = table_shock_prov[['Name', 'Min_dist_shock']]


        # return {'df': self.df_shock_prov, 'graph': G_shock_prov}





def ui_shock(network, shock_source = 'Reset'):
    """
    ---
    """

    if shock_source == 'Change in Tensioned Community Areas':
        network.apply_shock_com_areas()
    elif shock_source == 'Reduction in Public Provision':
        network.apply_shock_prov_centers()
