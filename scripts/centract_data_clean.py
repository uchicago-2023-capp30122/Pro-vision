import pandas as pd
import geopandas as gpd

def pre_clean_centract(path_sei, path_bounds):
    '''
    Makes cosmetic changes to socio economic indicator data and census tract
    boundary data
    '''
    dataframe = pd.read_csv(path_sei)
    dataframe = dataframe.drop(["Layer", "Name"], axis=1)
    cendata = gpd.read_file(path_bounds)
    cendata = cendata[["geoid10", "geometry"]]
    cendata.rename(columns={"geoid10": "GEOID"}, inplace=True)
    cendata["GEOID"] = cendata["GEOID"].astype(int)
    dataframe["Demographics, minorities (% of residents), 2016-2020"] = 100
    dataframe["Demographics, minorities (% of residents), 2016-2020"] = (
        dataframe["Demographics, minorities (% of residents), 2016-2020"]
        - dataframe["Demographics, Non-Hispanic White (% of residents), 2016-2020"]
    )
    dataframe = dataframe.drop(
        ["Demographics, Non-Hispanic White (% of residents), 2016-2020"], axis=1
    )
    return dataframe

def bin_centract(dataframe, path_bounds, indicator_vars):
    '''
    Creates bins for values pertaining to socio-economic indicators for
    census tracts
    '''
    cendata = gpd.read_file(path_bounds)
    bin_vars = []
    for indicator in indicator_vars:
        var_name = "bin_" + indicator
        #UPDATE LABELS HEREEEEE!!!!
        dataframe[var_name] = pd.qcut(
            dataframe[indicator], q=4, labels=False, duplicates="drop"
        )
        bin_vars.append(var_name)
    dataframe_shape = pd.merge(dataframe, cendata, on="GEOID")
    return dataframe_shape, bin_vars

def reshape_data(merged_data, indicator_vars, bin_vars):
    '''
    takes merged data of census tract level socio economic indicators and
    boundaries and reshapes it to make it filterable
    '''
    df_melt = pd.melt(
        merged_data,
        id_vars=["GEOID", "Longitude", "Latitude", "geometry"],
        value_vars=indicator_vars,
        var_name="indicator",
        value_name="value",
    )
    binned_melt = pd.melt(
        merged_data,
        id_vars=["GEOID"],
        value_vars=bin_vars,
        var_name="bins",
        value_name="bin_value",
    )
    binned_melt = binned_melt.add_suffix("_bin")
    df_binned = pd.concat([df_melt, binned_melt], axis=1)
    df_binned = df_binned.drop(["GEOID_bin", "bins_bin"], axis=1)
    return df_binned
