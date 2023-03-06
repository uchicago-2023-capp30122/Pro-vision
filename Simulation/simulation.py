'''
Simulation

ANGEL RODRIGUEZ GONZALEZ

Main file for simulation: implements the Network class and the ui_shock function.
'''

import pandas as pd
import geopandas as gpd
from shapely import wkt, geometry
import numpy as np
import networkx as nx
import json
import matplotlib.pyplot as plt
from matplotlib import use
import random
import utils
import copy


class Network(object):
    """
    Class for representing a city as a network, in order to apply Graph Theory
        to it.
    """

    def __init__(self, prov_data, sei_data, *, \
                prov_serv = 'police_stations', \
                sei_ind = 'homicide in community areas'):
        """
        Constructor. Creates the object, by defining its basic attributes,
            notably, the dataframe with attributes for each community area.
        Parameters:
            prov_data: (csv) cleaned data where each row represents a provision
                center
            sei_data: (csv) cleaned data where each row represents a community
                area
            prov_serv: (string) the selected provision service - police stations
                are the default mode
            sei_ind: (string) the selected socioeconomic vulnerability - homicide
                rate is the default mode 
        """

        NUMBER_OF_SEI = 10
        TIMES = 'Dist_from_com_areas_to_prov_centers.json'


        # First. Creates self.prov_centers
        #   Notes on some steps: We need to convert coordinates as strings into 
        #   shapely geometry objects (Points). 
        prov_centers = pd.read_csv(prov_data, usecols = \
                                   ['ADDRESS', 'coords', 'type'])
        prov_centers = prov_centers[prov_centers['type'] == prov_serv]

        prov_centers[['Latitude', 'Longitude']] = prov_centers['coords'].apply(\
            lambda x: pd.Series(str(x).strip('()').split(','))).astype(float)
        prov_centers['coords'] = prov_centers[['Latitude', 'Longitude']].apply(\
            tuple, axis=1)
        prov_centers['coords'] = prov_centers['coords'].apply(\
            switch_tuple_order)
        prov_centers['coords_geo'] = gpd.GeoSeries(prov_centers['coords'].apply(\
            lambda x: geometry.Point(x)))
        
        self.prov_centers = prov_centers.copy(deep = True)


        # Second: Creates self.df
        #   Notes on some steps: 
        #   1) We create two binary variables: 'Tensioned' (for top10 vulnerable
        #       community areas), and 'Prov_within' (for community areas with
        #       a provision centers within its boundaries). For the latter,
        #       we convert coordinates as strings into shapely geometry 
        #       objects (Multipolygon), and then use a helper function based in
        #       GeoPandas.
        #   2) We load a JSON containing the cleaned and formatted output from
        #       the TravelTime API: the time distance from each community area 
        #       to each provision center. That task is generated by the module
        #       times_matrices.py. Convert it to a pandas df
        #   3) We merge the latter to our main df, using names as keys (there is
        #       no risk, since the names in both df come from the same source)
        #       and generate a minimum distance variable
        df = pd.read_csv(sei_data, usecols = \
                        ['community_area', 'GEOID', 'longitude', 'latitude', \
                         'type', 'value', 'boundaries']) 
        df = df[df['type'] == sei_ind]

        df['Tensioned'] = 0
        df.loc[df['value'] >= min(\
            df.nlargest(NUMBER_OF_SEI, 'value')['value']), 'Tensioned'] = 1

        df['geometry'] = df['boundaries'].apply(lambda x: wkt.loads(x))
        df['Prov_within'] = df['geometry'].apply(\
            lambda x: 1 if point_in_area(self.prov_centers['coords_geo'], x) \
                else 0)
        
        f = open(TIMES)
        times_dict = json.load(f)
        times_df = pd.DataFrame.from_dict(times_dict, orient = 'index')
        num_prov_centers = len(times_df.columns)
        times_df['names'] = times_df.index
        
        df = df.merge(times_df, \
            how = 'outer', left_on = 'community_area', right_on = 'names')
        df.drop('names', axis = 1, inplace = True)
        df['Min_dist'] = df[df.columns[-num_prov_centers:]].min(axis = 1).apply(\
            lambda x: round(x/60,3))

        self.df = df.copy(deep = True)
  
        # Third: Creates self.table_statu_quo. This will be called back in the
        #   dashboard
        table_statu_quo = df[df['Tensioned'] == 1]
        table_statu_quo = table_statu_quo.rename(columns = \
            {'community_area': 'Community area', 'Min_dist': 'Min. distance'})
        self.table_statu_quo = table_statu_quo[['Community area', 'Min. distance']]




    def gen_adjacency_graph(self, colors = 'baseline'):
        """
        Generates the graph that models the city of Chicago as a network of 
            community areas, where connected nodes are bordering areas. The value
            of each node indicates whether the community area is near a police 
            station and whether it is tensioned (top10 in homicide rate). 
        Parameters:
            colors: (str) incorporates the user choice in the dashboard
        """

        # First: Opens and cleans the csv with the community areas pairs
        pairs = pd.read_csv('Pairs_vf.csv', sep = '\0') 
        pairs[['Origin', 'Destination']] = pairs['Pairs'].apply(\
            lambda x: pd.Series(str(x).strip('()').split(',')))
        pairs['Pairs'] = pairs[['Origin', 'Destination']].apply(tuple, axis=1)
        
        # Second: Generates the adjacency graph.
        #   Notes on some steps: Uses the adjacency tuples and than adds a
        #       dictionary as attribute for each node, labelling whether the
        #       community area is tensioned or not, and whether it has a provision
        #       center within its boundaries or not.
        G = nx.Graph(pairs['Pairs'])

        attrs = {}
        for _, com in self.df.iterrows():
            label = {'Tensioned': com['Tensioned'], 'Prov_within': com['Prov_within']}
            key = com['community_area']
            attrs[key] = label
        nx.set_node_attributes(G, attrs) # for debugging: nx.get_node_attributes(G, "Tensioned")[<node name>] or G[<node name>]["Tensioned"]


        # Third: Assigns colors to labels and prints the graph
        tens_colors = {0: '#D6D6CE', 1: '#FFAD05'}
        prov_colors = {0: '#D6D6CE', 1: '#FED628'}
        tens_node_colors = []
        prov_node_colors = []
        for node in G.nodes():
            tens_node_colors.append(tens_colors[G.nodes[node]['Tensioned']])
            prov_node_colors.append(prov_colors[G.nodes[node]['Prov_within']])

        use('agg')
        if colors == 'baseline':
            plt.clf()
            pos = nx.spring_layout(G, seed = 225)
            nx.draw(G, pos, node_color = '#D6D6CE', \
                    edgecolors = '#5A5A5A', edge_color = '#5A5A5A')
            plt.savefig('network_baseline.png')
        elif colors == 'Tensioned community area':
            plt.clf()
            pos = nx.spring_layout(G, seed = 225)
            nx.draw(G, pos, node_color = tens_node_colors, \
                    edgecolors = '#5A5A5A', edge_color = '#5A5A5A')
            plt.savefig('network_tens.png')
        elif colors == 'Provision within community area':
            plt.clf()
            pos = nx.spring_layout(G, seed = 225)
            nx.draw(G, pos, node_color = prov_node_colors, \
                    edgecolors = '#5A5A5A', edge_color = '#5A5A5A')
            plt.savefig('network_prov.png')
        # plt.show()   # https://networkx.guide/visualization
                     # https://networkx.org/documentation/stable/reference/drawing.html
        

        # Fourth: Creates self.G. This will be used as base for the graphs with 
        #   shock.
        self.G = copy.deepcopy(G)
        



    def apply_shock_com_areas(self, colors = 'baseline'):
        """
        Generates a random shock in the degree of tension for all the community 
            areas: the assignation of top-tensioned areas is stochastically 
            modified.
        Parameters:
            colors: (str) incorporates the user choice in the dashboard
        """

        # First: Creates self.df_shock_com (shocked version of self.df). Applies
        #   the stochastic shock to the community areas labelled as tensioned
        self.df_shock_com = self.df.copy(deep = True)
        self.df_shock_com['Tensioned_sim'] = 0
        shock_rows = np.random.choice(\
            self.df_shock_com.index, size = 10, replace = False)
        self.df_shock_com.loc[shock_rows, 'Tensioned_sim'] = 1
        # self.df_shock_com['Min_dist_shock'] = self.df_shock_com[[]].apply(min, axis = 1)  # Complete with the missing cols    # Why did I write this??


        # Second: Modifies the graph labels and prints the new graph
        G_shock_com = copy.deepcopy(self.G)

        attrs = {}
        for _, com in self.df_shock_com.iterrows():
            label = {'Tensioned': com['Tensioned_sim'], \
                     'Prov_within': com['Prov_within']}
            key = com['community_area']
            attrs[key] = label

        nx.set_node_attributes(G_shock_com, attrs)

        tens_colors = {0: '#D6D6CE', 1: '#FFAD05'}
        prov_colors = {0: '#D6D6CE', 1: '#FED628'}
        tens_node_colors = []
        prov_node_colors = []
        for node in G_shock_com.nodes():
            tens_node_colors.append(\
                tens_colors[G_shock_com.nodes[node]['Tensioned']])
            prov_node_colors.append(\
                prov_colors[G_shock_com.nodes[node]['Prov_within']])

        use('agg')
        if colors == 'baseline':
            plt.clf()
            pos = nx.spring_layout(G_shock_com, seed = 225)
            nx.draw(G_shock_com, pos, node_color = '#D6D6CE', \
                    edgecolors = '#5A5A5A', edge_color = '#5A5A5A')
            plt.savefig('network_baseline_shock_tens.png')
        elif colors == 'Tensioned community area':
            plt.clf()
            pos = nx.spring_layout(G_shock_com, seed = 225)
            nx.draw(G_shock_com, pos, node_color = tens_node_colors, \
                    edgecolors = '#5A5A5A', edge_color = '#5A5A5A')
            plt.savefig('network_tens_shock_tens.png')
        elif colors == 'Provision within community area':
            plt.clf()
            pos = nx.spring_layout(G_shock_com, seed = 225)
            nx.draw(G_shock_com, pos, node_color = prov_node_colors, \
                    edgecolors = '#5A5A5A', edge_color = '#5A5A5A')
            plt.savefig('network_prov_shock_tens.png')

        # Third: Creates self.table_shock_com (shocked version of 
        #   self.df_statu_quo). This will be called back in the dashboard
        table_shock_com = self.df_shock_com[\
            self.df_shock_com['Tensioned_sim'] == 1]
        table_shock_com = table_shock_com.rename(columns = \
            {'community_area': 'Community area', 'Min_dist': 'Min. distance'})
        self.table_shock_com = table_shock_com[['Community area', 'Min. distance']]




    def apply_shock_prov_centers(self, reduction = 0.25, colors = 'baseline'):
        """
        Generates a random shock in the set of provision centers: the number of
            operating centers is reduced by a factor and the eliminated centers
            are stochastically selected.
        Parameters:
            redution: (float) percentage reduction in the number of provision 
                centers
            colors: (str) incorporates the user choice in the dashboard      
        """

        # First: Creates self.df_shock_prov (shocked version of self.df). Applies
        #   the stochastic shock by reducing the number of provision centers
        self.df_shock_prov = self.df.copy(deep = True)

        prov_centers_all = list(self.df.columns[\
            -(len(self.prov_centers)+1):-1].values)
        prov_centers_shock = random.sample(\
            prov_centers_all, round(len(self.prov_centers)*(1-reduction)))

        self.df_shock_prov['Min_dist_shock'] = self.df_shock_prov[\
            prov_centers_shock].min(axis = 1).apply(lambda x: round(x/60, 3))
        prov_cens_shock_df = self.prov_centers[\
            self.prov_centers['ADDRESS'].isin(prov_centers_shock)] 
        self.df_shock_prov['Prov_within_shock'] = self.df_shock_prov['geometry'].apply(\
            lambda x: 1 if point_in_area(prov_cens_shock_df['coords_geo'], x) else 0)   # (before: point_in_area(prov_cens_shock_df['coords_geo'], x, prov_centers_shock)        


        # Second: Modifies the graph labels and prints the new graph
        G_shock_prov = copy.deepcopy(self.G)

        attrs = {}
        for _, com in self.df_shock_prov.iterrows():
            label = {'Tensioned': com['Tensioned'], 'Prov_within': com['Prov_within_shock']}
            key = com['community_area']
            attrs[key] = label

        nx.set_node_attributes(G_shock_prov, attrs)  

        tens_colors = {0: '#D6D6CE', 1: '#FFAD05'}
        prov_colors = {0: '#D6D6CE', 1: '#FED628'}
        tens_node_colors = []
        prov_node_colors = []
        for node in G_shock_prov.nodes():
            tens_node_colors.append(tens_colors[G_shock_prov.nodes[node]['Tensioned']])
            prov_node_colors.append(prov_colors[G_shock_prov.nodes[node]['Prov_within']])

        use('agg')
        if colors == 'baseline':
            plt.clf()
            pos = nx.spring_layout(G_shock_prov, seed = 225)
            nx.draw(G_shock_prov, pos, node_color = '#D6D6CE', \
                    edgecolors = '#5A5A5A', edge_color = '#5A5A5A')
            plt.savefig('network_baseline_shock_prov.png')
        elif colors == 'Tensioned community area':
            plt.clf()
            pos = nx.spring_layout(G_shock_prov, seed = 225)
            nx.draw(G_shock_prov, pos, node_color = tens_node_colors, \
                    edgecolors = '#5A5A5A', edge_color = '#5A5A5A')
            plt.savefig('network_tens_shock_prov.png')
        elif colors == 'Provision within community area':
            plt.clf()
            pos = nx.spring_layout(G_shock_prov, seed = 225)
            nx.draw(G_shock_prov, pos, node_color = prov_node_colors, \
                    edgecolors = '#5A5A5A', edge_color = '#5A5A5A')
            plt.savefig('network_prov_shock_prov.png')


        # Third: Creates self.table_shock_prov (shocked version of 
        #   self.df_statu_quo). This will be called back in the dashboard
        table_shock_prov = self.df_shock_prov[\
            self.df_shock_prov['Tensioned_sim'] == 1]
        table_shock_prov = table_shock_prov.rename(columns = \
            {'community_area': 'Community area', 'Min_dist': 'Min. distance'})
        self.table_shock_prov = table_shock_prov[['Community area', 'Min. distance']]





def ui_shock(network, shock_source = 'Reset'):
    """
    Channels the user's order on the desired source of shock, by executing the 
        applicable method of the Network class
    Parameters:
        network: (instance of Network) the model
        shock_source: (str) the selection of the user in the interface 
    """

    if shock_source == 'Change in Tensioned Community Areas':
        network.apply_shock_com_areas()
    elif shock_source == 'Reduction in Public Provision':
        network.apply_shock_prov_centers()






############################ For utils.py ######################################


def point_in_area(points, polygon):
    """
    Verifies whether a point in a given set is geographically within an area.
    Parameters:
    Returns
    """

    for p in points:
        if p.within(polygon):
            return True
    return False 



def switch_tuple_order(tup):
    """
    ---
    """
    return (tup[1], tup[0])