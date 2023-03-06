import geopandas as gpd
import pandas as pd
import re
isochrones = pd.read_csv("data/clean_prov/prov_geoV1.csv")
pattern_coords = r'Coordinates\(lat=(-?[\d\.]+), lng=(-?[\d\.]+)\)' #extracts coords
pattern_shell = r'(?<=shell=).+ ' 

def find_shells(str):
    match = re.findall(pattern_shell,str)
    return match
def find_coords(lst):
    coords =[]
    for item in lst:
        match = re.findall(pattern_shell,item)
        coords.append(match)
    return coords




