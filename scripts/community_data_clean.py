import os
import pandas as pd


def clean_prov_csv(pd_df, col_list, category):
    """
    Cleans pandas dataframes for data on provisions
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
    dataframe.drop(col_list, axis=1, inplace=True)
    dataframe["type"] = category
    dataframe["type"] = dataframe["type"].astype("category")
    return dataframe


def clean_prov(list_cols, path):
    """
    Cleans all csvs in a folder and manipulates them to a desired format
    Input:
    list_cols : list of columns relevent to the analysis (location attributes)
    path: path of folder containing files for different provisions
    Output: dictionary with provision type as key and dataframe of cleaned data
    for those provisions as values
    """
    dict_prov = {}
    for filename in os.listdir(path):
        new_path = path + "/" + filename
        dataframe = pd.read_csv(new_path)
        cat = filename.split(".")[0].lower()
        clean_data = clean_prov_csv(dataframe, list_cols, cat)
        dict_prov[cat] = clean_data
        new_path = path
    return dict_prov


def clean_sei_csv(pd_df, category):
    """
    Cleans a pandas dataframe containing data on socio economic indicators at
    the community level

    Input:
    pd_df: pandas dataframe containing community level information on a socio-
    economic indicator
    category: Name (breif description) of the socio economic indicator that
    pd_df relates to
    """
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


def clean_sei_com(path):
    """
    Clean all socio-economic indicator data csvs at the community level in
    a folder

    Input:
    path: path of folder containing socio-economic data csvs
    Output:
    dicitionary of socio-economic indicators with the indicator as the key and
    community level data on that indicator in a pandas dataframe as the value.
    """
    dict_sei = {}
    for filename in os.listdir(path):
        new_path = path + "/" + filename
        dataframe = pd.read_csv(new_path)
        cat = filename.split(".")[0].lower()
        clean_data = clean_sei_csv(dataframe, cat)
        dict_sei[cat] = clean_data
        new_path = path
    return dict_sei
