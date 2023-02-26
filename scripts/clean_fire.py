import pandas as pd
from geo_code import *
import geopandas as gpd

fire_stations = pd.read_csv(r"raw_data/Fire_Stations.csv")
fire_stations = fire_stations.astype(str)
fire_stations["full_address"] = fire_stations[
    ["ADDRESS", "CITY", "STATE", "ZIP"]
].apply(", ".join, axis=1)
fire_stations.drop(
    ["NAME", "ADDRESS", "CITY", "STATE", "ZIP", "ENGINE"], axis=1, inplace=True
)
fire_stations["coords"] = fire_stations["LOCATION"].str.extract(r"\((.*?)\)")
fire_stations["coords"] = fire_stations["coords"].apply(
    lambda x: tuple(map(float, x.split(",")))
)
fire_stations.drop("LOCATION", axis=1, inplace=True)
fire_stations["isochrone"] = fire_stations.apply(
    lambda row: geo_code.isochrone(row["coords"], row["full_address"]), axis=1
)
gdf = gpd.GeoDataFrame(fire_stations, geometry="isochrone")
gdf.to_file("data/output.geojson", driver="GeoJSON")