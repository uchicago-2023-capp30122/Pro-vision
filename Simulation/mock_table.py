import pandas as pd

lst = ['Humboldt Park',
 'Austin',
 'West Garfield Park',
 'North Lawndale',
 'South Shore',
 'Roseland',
 'West Englewood',
 'Englewood',
 'Greater Grand Crossing',
 'Auburn Gresham']
datatable_dict = {'name': lst, 'height': [0,9,8,7,6,5,4,3,2,1]}
datatable_df = pd.DataFrame.from_dict(datatable_dict)