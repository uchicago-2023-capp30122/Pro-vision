import pandas as pd


def clean_csv(pd_df, col_list, category):
    """
    Cleans pandas dataframes
    Input:
    pd_df: pandas dataframe
    col_list: list of relevant columns (should contain Address components)
    Output: cleaned pandas dataframe
    """
    dataframe = pd_df.astype(str)
    dataframe = dataframe[col_list]
    dataframe["full_address"] = dataframe[["ADDRESS", "CITY", "STATE", "ZIP"]].apply(
        ", ".join, axis=1
    )
    dataframe["coords"] = dataframe["LOCATION"].str.extract(r"\((.*?)\)")
    dataframe["coords"] = dataframe["coords"].apply(
        lambda x: tuple(map(float, x.split(",")))
    )
    dataframe.drop("LOCATION", axis=1, inplace=True)
    dataframe["type"] = category
    dataframe["type"] = dataframe["type"].astype("category")
    return dataframe


fire_stations = pd.read_csv(r"raw_data/Fire_Stations.csv")
warming_centers = pd.read_csv(r"raw_data/Warming_Centers.csv")
neighbor_clinics = pd.read_csv(r"raw_data/Neighborhood_Health_Clinics_-_Historical.csv")
police_stations = pd.read_csv(r"raw_data/Police_Stations.csv")
list_cols = ["ADDRESS", "CITY", "STATE", "ZIP", "LOCATION"]
fire_clean = clean_csv(fire_stations, list_cols, "fire_station")
warm_clean = clean_csv(warming_centers, list_cols, "warming_center")
clinics_clean = clean_csv(
    neighbor_clinics,
    list_cols,
    "neighborhood_clinic",
)
police_clean = clean_csv(police_stations, list_cols, "police_station")
provisions = pd.concat([fire_clean, warm_clean, clinics_clean, police_clean], axis=0)
provisions.to_csv("data/provisions.csv")
