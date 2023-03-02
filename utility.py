import plotly.express as px
import numpy as np
import copy as cp
import plotly.graph_objects as go

# Setting general colors
colors = { 
    'bg': 'rgba(0,0,0,0)',
    'font': '#767676',
    'marker': ' #800000',
    'default': '#D6D6CE'
}

def socioeconomic_map(df, geojsonfile):
    #------- CHOROPLETH MAP TO DISPLAY SOCIOECONOMIC VARIABLE -------#
    trace1 = px.choropleth(
            df, # Socioeconomic data
            geojson = geojsonfile, # Mapping geoJson
            color = 'Value', # Setting color intensity by the values of HCSNS_2016-2018 (i.e., safety variable)
            color_continuous_scale = 'PuBu', # Choosing color
            locations = 'Community Area', # Identifies locations from geojson
            featureidkey = "properties.pri_neigh", # Consider pri_neigh as key from geojson dictionary
            labels = {'Label'} # Labelling socioeconomic variable
            )
    trace1.update_geos(fitbounds = "locations", visible = False) # Maps shapefile boundary locations from geojson
    trace1.layout.update(
        margin = {"r":20,"t":20,"l":20,"b":20}, # Sets boundaries of map
        showlegend = True # Show legend
        )
    return trace1

def facilities_map(df, geojsonfile):
    #------- SCATTER MAP FOR PUBLIC SERVICES/PROVISIONS -------#
    trace2 = px.scatter_geo(df,
                            lat = 'latitude', lon = 'longitud', 
                            geojson = geojsonfile,
                            hover_data={'Provision': False, 'longitud': False, 
                                        'latitude': False, 'ADDRESS': True, 
                                        'ZIP': True},
                            symbol_sequence = ['star-diamond-open'],
                            color_discrete_sequence = [colors['marker']]
                            )
    trace2.layout.update(
        paper_bgcolor = colors['bg'], # Sets transparent background
        plot_bgcolor = colors['bg'], # Sets transparent background
        font_color = colors['font'], # Sets font color
        margin = {"r":20,"t":20,"l":20,"b":20} # Sets boundaries of map
        )

    return trace2

def empty_map(df, geojsonfile):

    df.sort_values("GEOID", inplace=True)
    df.drop_duplicates(subset="GEOID", keep=False, inplace=True)

    #------- EMPTY CHOROPLETH MAP -------#
    trace0 = px.choropleth(
            df, # Socioeconomic data
            geojson = geojsonfile, # Mapping geoJson
            locations = 'Community Area', # Identifies locations from geojson
            featureidkey = "properties.pri_neigh", # Consider pri_neigh as key from geojson dictionary
            color_discrete_sequence = [colors['default']],
            height = 800
            )
    trace0.update_geos(fitbounds = "locations", visible = False) # Maps shapefile boundary locations from geojson
    trace0.layout.update(
        showlegend = False # Show legend
        )

    return trace0