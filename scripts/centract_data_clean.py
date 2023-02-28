import pandas as pd
import geopandas as gpd
dataframe = pd.read_csv("raw_data/centract/sei_centract.csv")
dataframe = dataframe.drop(["Layer", "Name"], axis=1)
cendata = gpd.read_file("raw_data/Boundaries - Census Tracts - 2010.geojson")
cendata = cendata[["geoid10", "geometry"]]
cendata.rename(columns={"geoid10": "GEOID"}, inplace=True)
cendata["GEOID"] = cendata["GEOID"].astype(int)
dataframe["Demographics, minorities (% of residents), 2016-2020"] = 100
dataframe["Demographics, minorities (% of residents), 2016-2020"] = \
dataframe["Demographics, minorities (% of residents), 2016-2020"] - \
    dataframe["Demographics, Non-Hispanic White (% of residents), 2016-2020"]
dataframe = dataframe.drop(["Demographics, Non-Hispanic White (% of residents), 2016-2020"], axis=1)
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
    "Population (residents), 2015-2019"
    ]
bin_vars = []
for indicator in indicator_vars:
    var_name = "bin_" + indicator
    dataframe[var_name] = pd.qcut(
        dataframe[indicator], q=4, labels=False, duplicates="drop"
    )
    bin_vars.append(var_name)
    # FIX THIS DUPLICATES ISSUE!!!!

dataframe_shape = pd.merge(dataframe, cendata, on = 'GEOID')
df_melt = pd.melt(
    dataframe_shape,
    #id_vars=["GEOID", "Longitude", "Latitude"] + bin_vars,
    id_vars=["GEOID", "Longitude", "Latitude","geometry"],
    value_vars=indicator_vars,
    var_name="indicator",
    value_name="value",
)


binned_melt = pd.melt(
    dataframe_shape,
    id_vars=["GEOID"],
    value_vars=bin_vars,
    var_name="bins",
    value_name="bin_value",
)
binned_melt = binned_melt.add_suffix('_bin')
df_binned = pd.concat([df_melt, binned_melt], axis=1)
df_binned['flag'] = False
df_binned['flag']= df_binned['GEOID'] != df_binned['GEOID_bin']
df_binned = df_binned.drop(['GEOID_bin', 'bins_bin', 'flag'], axis=1)
df_binned.to_csv('data/binned_sei/final_geo_SEI.csv')

