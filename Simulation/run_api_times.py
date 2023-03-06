import times_matrices
import pandas as pd




prov_centers = pd.read_csv('prov_geoV1.csv', usecols =  \
                            ['ADDRESS', 'coords', 'type'])
com_areas = pd.read_csv('sei_community_bounds.csv', usecols = \
                ['community_area', 'longitude', 'latitude', 'type']) 


times_matrices.get_distances(prov_centers, com_areas)