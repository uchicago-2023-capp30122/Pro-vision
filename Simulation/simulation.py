import pandas as pd
import numpy as np
import networkx as nx
from Setu import distance # adjust name


class Graph(object):
    """
    ---
    """

    def __init__(self, prov_data, sei_data, *, \
                prov_serv = 'police_stations', sei_ind = 'Homicide rate'):
        """
        Constructor. Creates the object, by defining its basic attributes,
            notably, the dataframe with attributes for each census.
        """

        NUMBER_OF_SEI = 10

        prov_centers = pd.read_csv(prov_data, usecols = \
                                   ['ADDRESS', 'coords', 'type'])
        prov_centers = prov_centers[prov_centers.type == prov_serv] 
        prov_centers[['Latitude', 'Longitude']] = prov_centers['coords'].apply(\
            lambda x: pd.Series(str(x).strip('()').split(',')))
        self.prov_centers = prov_centers


        df = pd.read_csv(sei_data, usecols = \
                        ['Name', 'GEOID', 'Longitude', 'Latitude', 'indicator', \
                         'value'])    # Confirm with Setu's csv
        df = df[df['indicator'] == sei_ind]
        df['Tensioned'] = df['indicator'].apply(\
            lambda x: 1 if x.nlargest(NUMBER_OF_SEI, 'value') else 0)
        # df['Prov_time'] = see below
        df['Prov_near'] = df['Prov_time'].apply(lambda x: 1 if x <= 10 else 0)
        self.df = df


        
        for c in df:
            min_dist = 10000000
            for p in prov_centers:
                    dist = ()
                    if dist < min_dist:
                        min_dist = dist


        pass


    def gen_dist_matrix(self, ):
        """
        Generates a symmetric matrix where each element is the distance in time
            from census tract i to census tract j.
        Paramters:
        Returns 
        """

        matrix = np.fromfunction(lambda i, j: setu(\
            self.df.iloc[i]['coordinates'], self.df.iloc[j]['coordinates']), (len(self.df), len(self.df)))   # Setu's function
        # In case I found out how to build just an upper triangular matrix
        #       matrix = np.triu(matrix) + np.triu(matrix, k = 1).T

        return pd.DataFrame(matrix, \
                            columns = list(self.df['Name']), \
                            index = list(self.df['Name']))


    def gen_adjac_matrix(self, ):
        """
        Generates the adjacency matrix that models the city of Chicago as a
            network of census tracts, based on their nearness degree (distance in 
            time less than 10 minutes in car from each other).
        Parameters:
        Returns
        """

        return self.gen_dist_matrix().applymap(lambda x: 1 if x <= 10 else 0)


    def gen_graph(self, ):
        """
        Generates the graph that models the city of Chicago as a network of 
            census tracts, where connected nodes are "near" census tracts using
            the adjacency matrix. The value of each node indicates whether the 
            census tract is near a police station and whether it is tensioned
            (top10 in homicide rate). 
        Parameters:
        Returns
        """

        graph = nx.Graph(self.gen_adjac_matrix())

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

