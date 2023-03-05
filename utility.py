import plotly.express as px

# Setting general colors
colors = {
    'bg': 'rgba(0,0,0,0)', # Transparent
    'font': '#767676', # Dark Gray
    'marker': '#800000', # Maroon
    'coverage': 'rgba(128,0,0,0.3)', # Maroon with some transparency
    'default': '#D6D6CE', # Light Gray
}

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
            projection = "gnomonic" # mercator, orthographic, azimuthal equal area, azimuthal equidistant, gnomonic, mollweide
            )
    trace0.update_geos(fitbounds = "locations", visible = False) # Maps shapefile boundary locations from geojson
    trace0.update_traces(marker_line_color = "white", marker_line_width=0.5)
    trace0.layout.update(
        width = 800, height = 600,
        margin = {"r":0,"t":10,"l":0,"b":0},
        showlegend = False 
        )

    return trace0

def socioeconomic_map(df, geojsonfile):
    #------- CHOROPLETH MAP TO DISPLAY SOCIOECONOMIC VARIABLE -------#
    trace1 = px.choropleth(
            df, # Socioeconomic data
            geojson = geojsonfile, # Mapping geoJson
            color = "bin_value_bin",
            #color_continuous_scale = 'Aggrnyl', # Choosing color
            color_discrete_map={'3': '#FFAD05',
                                '2': '#FED628',
                                '1': '#F1F374',
                                '0': '#D6D6CE'},
            labels = {'bin_value_bin': ''},
            locations = 'geoid10', # Identifies locations from geojson
            featureidkey = "properties.geoid10", # Consider pri_neigh as key from geojson dictionary
            projection = 'gnomonic'
            )
    trace1.update_geos(fitbounds = "locations", visible = False) # Maps shapefile boundary locations from geojson
    trace1.update_traces(marker_line_color = "white", marker_line_width = 0.5)
    trace1.layout.update(
        legend = dict(y=0.9, x=0.8),
        coloraxis_colorbar = dict(
            thicknessmode = "pixels", thickness = 30, ticks="inside",
            lenmode="pixels", len = 175
            ),
        font_color = colors['font'],
        width = 800, height = 600,
        margin = {"r":0,"t":10,"l":0,"b":0}, # Sets boundaries of map
        showlegend = True # Show legend
        )
    return trace1

def facilities_map(df, geojsonfile):
    #------- SCATTER MAP FOR PUBLIC SERVICES/PROVISIONS -------#
    trace2 = px.scatter_geo(df,
                            lat = 'latitude', lon = 'longitude', 
                            geojson = geojsonfile,
                            hover_data={'full_address': True, 'coords': False,
                                    'type': False, 'row_number': False, 'isoID': False,
                                    'latitude': False, 'longitude': False
                                    },
                            symbol_sequence = ['circle'],
                            color_discrete_sequence = [colors['marker']],
                            projection = 'gnomonic'
                            )
    trace2.update_traces(marker_line_color = "white", marker_line_width=0.5)
    trace2.layout.update(
        width = 800, height = 600,
        paper_bgcolor = colors['bg'], # Sets transparent background
        plot_bgcolor = colors['bg'], # Sets transparent background
        font_color = colors['font'], # Sets font color
        margin = {"r":0,"t":10,"l":0,"b":0} # Sets boundaries of map
        )

    return trace2

def isochrone_map(df, geojsonfile):

    #------- ISOCHRONE MAP -------#
    trace3 = px.choropleth(
            df, # Socioeconomic data
            geojson = geojsonfile, # Mapping geoJson
            locations = 'full_address',
            featureidkey = "properties.full_address", # Consider pri_neigh as key from geojson dictionary
            color = [i for i in df['full_address']],
            color_discrete_sequence = [colors['coverage'] for i in range(0, len(df['full_address']))],
            projection = "gnomonic" 
            )
    trace3.update_geos(fitbounds = "locations", visible = False) # Maps shapefile boundary locations from geojson
    trace3.update_traces(marker_line_color = 'white', marker_line_width=1.5)
    trace3.layout.update(
        width = 900, height = 350,
        paper_bgcolor = colors['bg'],
        plot_bgcolor = colors['bg'], 
        margin = {"r":0,"t":10,"l":0,"b":0},
        showlegend = False
        )

    return trace3

def histogram(df, variable):
    hist = px.histogram(df, x = variable, 
                        color = "bin_value_bin",
                        color_discrete_map={'3': '#FFAD05',
                                            '2': '#FED628',
                                            '1': '#F1F374',
                                            '0': '#D6D6CE'},
                        labels = {'bin_value_bin': ''}
                        )
    hist.layout.update(
        width = 600, height = 300,
        paper_bgcolor = colors['bg'], 
        plot_bgcolor = colors['bg'], 
        font_color = colors['font'])
    hist.update_yaxes(visible=False)
    hist.update_xaxes(title=None)
    return hist