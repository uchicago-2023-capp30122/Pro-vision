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
            color = 'value', # Setting color intensity by the values of HCSNS_2016-2018 (i.e., safety variable)
            color_continuous_scale = 'PuBu', # Choosing color
            locations = 'geoid10', # Identifies locations from geojson
            featureidkey = "properties.geoid10", # Consider pri_neigh as key from geojson dictionary
            width = 800
            )
    trace1.update_geos(fitbounds = "locations", visible = False) # Maps shapefile boundary locations from geojson
    trace1.layout.update(
        margin = {"r":0,"t":0,"l":0,"b":0}, # Sets boundaries of map
        showlegend = True # Show legend
        )
    return trace1

def facilities_map(df, geojsonfile):
    #------- SCATTER MAP FOR PUBLIC SERVICES/PROVISIONS -------#
    trace2 = px.scatter_geo(df,
                            lat = 'latitude', lon = 'longitude', 
                            geojson = geojsonfile,
                            hover_data={'ADDRESS': False, 'CITY': False, 'STATE': False, 
                                   'ZIP': False, 'full_address': True, 'coords': False,
                                    'type': False, 'isochrones': False, 'latitude': False,
                                    'longitude': False
                                    },
                            symbol_sequence = ['star-diamond-open'],
                            color_discrete_sequence = [colors['marker']],
                            width = 800
                            )
    trace2.layout.update(
        paper_bgcolor = colors['bg'], # Sets transparent background
        plot_bgcolor = colors['bg'], # Sets transparent background
        font_color = colors['font'], # Sets font color
        margin = {"r":0,"t":0,"l":0,"b":0} # Sets boundaries of map
        )

    return trace2

def empty_map(df, geojsonfile):

    df.sort_values("geoid10", inplace=True)
    df.drop_duplicates(subset=['geoid10'])

    #------- EMPTY CHOROPLETH MAP -------#
    trace0 = px.choropleth(
            df, # Socioeconomic data
            geojson = geojsonfile, # Mapping geoJson
            locations = 'geoid10', # Identifies locations from geojson
            featureidkey = "properties.geoid10", # Consider pri_neigh as key from geojson dictionary
            color_discrete_sequence = [colors['default']],
            width = 800
            )
    trace0.update_geos(fitbounds = "locations", visible = False) # Maps shapefile boundary locations from geojson
    trace0.layout.update(
        margin = {"r":0,"t":0,"l":0,"b":0},
        showlegend = False # Show legend
        )

    return trace0