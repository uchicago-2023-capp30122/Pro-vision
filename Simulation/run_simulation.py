'''
Simulation - run

ANGEL RODRIGUEZ GONZALEZ

Executes some functions in simulation.py to create a model and prints&saves results.
'''

import simulation

########## CREATE INSTANCE ##########

n = simulation.Network('prov_geoV1.csv','sei_community_bounds.csv')
print(' . \n . \n .\n This is the distance of the real most tensioned community areas to the nearest police station \n ------------------------ ')
print(n.table_statu_quo)



########## GENERATE GRAPH ##########

n.gen_adjacency_graph()
print('------------------------\n You can print the graphs from the terminal \n . \n . \n .')



########## APPLY SHOCK 1: CHANGE IN TENSIONED AREAS ##########

n.apply_shock_com_areas()
print('This is the distance of the simulated most tensioned community areas to the nearest police station, after a stochastic change in tensioned areas \n ------------------------')
print(n.table_shock_com)
print('------------------------\n You can print the graphs from the terminal  \n . \n . \n .')



########## APPLY SHOCK 2: CHANGE IN POLICE STATIONS ##########

n.apply_shock_prov_centers()
print('This is the distance of the real most tensioned community areas to the nearest police station, after a stochastic reduction in the number of police stations  \n ------------------------')
print(n.table_shock_prov)
print('------------------------\n You can print the graphs from the terminal  \n . \n . \n .')