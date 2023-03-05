
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
    
    use('agg')
    pos = nx.spring_layout(G, seed=225)  # Seed for reproducible layout
    nx.draw(G, pos)
    plt.show()

    plt.savefig('network.png')

    pass






        # Some issues to be solved here:
            # to create the nodes, we can avoid the ugly for loop
            # we have to avoid the nested for loop. Options:
            #   investigate whether another nx method
            #   Setu's new API
            #   clustering using lat 
            #   clustering using the GeoID (worst option)
            # Possibly interesing methods:
            #   nx.add_edges_from()
            #   adjacency matrix
            #   nx.from_pandas_dataframe()


