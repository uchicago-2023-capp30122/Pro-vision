import pandas as pd
import geopandas as gpd
def clean_sei_cen():
    """
    Clean socio-econimic indicator data at the census tract level
    """
    dataframe = pd.read_csv("raw_data/centract/sei_centract.csv")
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
        dataframe[var_name] = pd.qcut(
            dataframe[indicator], q=4, labels=False, duplicates="drop"
        )
        bin_vars.append(var_name)
    # FIX THIS DUPLICATES ISSUE!!!!
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
        value_vars=bin_vars,
        var_name="bins",
        value_name="bin_value",
    )
    binned_data = binned_data.drop(["bins"], axis=1)
    # binned_data.to_csv("data/binned_data_V2.csv")

    cendata = gpd.read_file("raw_data/Boundaries - Census Tracts - 2010.geojson")
    cendata = cendata[["geoid10", "geometry"]]
    cendata.rename(columns={"geoid10": "GEOID"}, inplace=True)
    cendata["GEOID"] = cendata["GEOID"].astype(int)
    cen_geo = pd.merge(binned_data, cendata, on="GEOID")
    # Check if merge has filled data for all rows or jst selected ones
    # cen_geo.to_file('censustractSEI.geojson', driver='GeoJSON')
    cen_geo.to_csv("data/binned_data_V3.csv")
