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


def clean_sei_cen():
    """
    Clean socio-econimic indicator data at the census tract level
    """
    dataframe = pd.read_csv(
        "raw_data/centract/sei_centract.csv"
    )
    dataframe = dataframe.drop(["Layer", "Name"], axis=1)
    indicator_vars = [
        "Uninsured rate (% of residents), 2015-2019",
        "Homicide (crimes), 2017-2021",
        "Major crime (crimes), 2016-2020",
        "Violent crime (crimes), 2016-2020",
        "Eviction rate (% of renter-occupied households), 2018",
        "Severely rent-burdened (% of renter-occupied housing units), 2015-2019",
        "Traffic crashes (number of crashes), 2021",
        "High school graduation rate (% of residents), 2015-2019",
        "College graduation rate (% of residents), 2015-2019",
        "Unemployment rate (%), 2015-2019",
        "Median household income, 2015-2019",
        "Per capita income, 2015-2019",
        "Poverty rate (% of residents), 2015-2019",
        "Demographics, Non-Hispanic White (% of residents), 2016-2020",
        "Population (residents), 2015-2019",
    ]
    bin_vars = []
    for indicator in indicator_vars:
        var_name = "bin" + indicator
        dataframe[var_name] = pd.qcut(dataframe[indicator], q=4, labels=False, duplicates= 'drop')
        bin_vars.append(var_name)
#FIX THIS DUPLICATES ISSUE!!!!
    df_melt = pd.melt(
        dataframe,
        id_vars=["GEOID", "Longitude", "Latitude"] + bin_vars,
        value_vars=indicator_vars,
        var_name="indicator",
        value_name="value",
    )

    binned_data = pd.melt(
        df_melt,
        id_vars=["GEOID", "Longitude", "Latitude", "indicator", "value"],
        value_vars = bin_vars,
        var_name="bins",
        value_name="bin_value",
    )

    binned_data.to_csv("data/binned_data_V1.csv")
    # df_melt["bin"] = 0
    # for var in indicator_vars:
    #     filtered_df = df_melt[df_melt["indicator"] == var]
    #     filtered_df["bin"] = pd.qcut(filtered_df["value"], q=4, labels=False)
    #     df_melt.set_index("GEOID", inplace=True)
    #     df_melt.update(filtered_df.set_index("GEOID"))
    #     df_melt.reset_index()
merged_df = pd.merge(df1, df2, on='id')

dict_provision = clean_prov()
provisions = pd.concat(dict_provision.values())
provisions.to_csv("data/clean_prov/prov_1.csv")
dict_indicators = clean_sei_com()
indicators = pd.concat(dict_indicators.values())
indicators.to_csv("data/clean_sei/sei_4.csv")
