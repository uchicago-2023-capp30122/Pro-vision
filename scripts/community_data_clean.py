import pandas as pd
import geopandas as gpd
import os


def clean_prov_csv(pd_df, col_list, category):
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


def clean_sei_csv(pd_df, category):
    dataframe = pd_df.astype(str)
    dataframe = dataframe.iloc[:, range(1, 4)]
    dataframe = dataframe.drop(dataframe.index[0], axis=0)
    dataframe.rename(
        columns={dataframe.columns[0]: "community_area", dataframe.columns[2]: "value"},
        inplace=True,
    )
    dataframe["type"] = category
    dataframe["type"] = dataframe["type"].astype("category")
    return dataframe


def clean_prov():
    dict_prov = {}
    list_cols = ["ADDRESS", "CITY", "STATE", "ZIP", "LOCATION"]
    path = "raw_data/provisions"
    for filename in os.listdir(path):
        new_path = path + "/" + filename
        dataframe = pd.read_csv(new_path)
        cat = filename.split(".")[0].lower()
        clean_data = clean_prov_csv(dataframe, list_cols, cat)
        dict_prov[cat] = clean_data
        new_path = path
    return dict_prov


def clean_sei_com():
    """
    Clean socio-economic indicator data at the community level
    """
    dict_sei = {}
    path = "raw_data/socioecon"
    for filename in os.listdir(path):
        new_path = path + "/" + filename
        dataframe = pd.read_csv(new_path)
        cat = filename.split(".")[0].lower()
        clean_data = clean_sei_csv(dataframe, cat)
        dict_sei[cat] = clean_data
        new_path = path
    return dict_sei

dict_provision = clean_prov()
provisions = pd.concat(dict_provision.values())
provisions.to_csv("data/clean_prov/prov_1.csv")
dict_indicators = clean_sei_com()
indicators = pd.concat(dict_indicators.values())
indicators.to_csv("data/clean_sei/sei_4.csv")
