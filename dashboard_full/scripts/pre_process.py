import pandas as pd
from .community_data_clean import *
from .centract_data_clean import *
from .geo_api import *
import geojson

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
    "Demographics, minorities (% of residents), 2016-2020",
    "Population (residents), 2015-2019",
]
# Cleaning provision files
def get_clean_prov():
    """
    Returns cleaned data for provisions
    """
    path = "raw_data/provisions"
    list_cols = ["ADDRESS", "CITY", "STATE", "ZIP", "LOCATION"]
    dict_provision = clean_prov(list_cols, path)
    provisions = pd.concat(dict_provision.values())
    provisions = provisions.assign(row_number=range(len(provisions)))
    provisions["row_number"] = provisions["row_number"].astype(str)
    provisions["isoID"] = provisions["type"] + provisions["row_number"]
    return provisions


# pass on provisions to Diego


def get_clean_community_sei():
    """
    Returns cleaned community level Socio-economic indicator data
    """
    path = "raw_data/socioecon"
    dict_sei = clean_sei_com(path)
    sei_cleaned = pd.concat(dict_sei.values())

    return sei_cleaned


def get_clean_centract_sei(indicator_vars):
    """
    Returns clean census-tract level Socio-Economic indicator data
    """
    path_sei = "raw_data/centract/sei_centract.csv"
    path_bounds = "raw_data/Boundaries - Census Tracts - 2010.geojson"
    centract = pre_clean_centract(path_sei, path_bounds)
    wide_centract, bin_vars = bin_centract(centract, path_bounds, indicator_vars)
    final_centract = reshape_data(wide_centract, indicator_vars, bin_vars)
    return final_centract


def isochrone_add():
    """
    Add isochrones to cleaned provision data
    """
    prov_data = get_clean_prov()
    prov_data["isochrones"] = prov_data.apply(
        lambda row: get_isochrones(row["coords"], row["type"]), axis=1
    )
    return prov_data


def isochrone_json():
    """
    convert isochrones to a json file
    """
    combined_geoj = {}
    iso_data = isochrone_add()
    merged_geo = merge_geojson(iso_data)
    for prov, geoj in merged_geo.items():
        combined_geoj[prov] = geojson.FeatureCollection(geoj)
    return combined_geoj
