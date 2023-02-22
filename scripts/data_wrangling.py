import pandas as pd
fire_stations = pd.read_csv(r'raw_data/Fire_stations.csv')
fire_stations = fire_stations.astype(str)
fire_stations["full_address"] = fire_stations[["ADDRESS", "CITY", "STATE", "ZIP"]].apply(", ".join, axis=1)
fire_stations.drop(
    ["NAME", "ADDRESS", "CITY", "STATE", "ZIP","ENGINE"],
    axis=1,
    inplace=True
)
fire_stations['coords'] = fire_stations['LOCATION'].str.extract(r'\((.*?)\)')
fire_stations.drop("LOCATION", axis=1, inplace=True)
fire_stations.to_csv("data/fire_stations.csv")