import plotly.express as px

# Setting general colors
colors = {
    'bg': 'rgba(0,0,0,0)', # Transparent
    'font': '#767676', # Dark Gray
    'marker': '#800000', # Maroon
    'coverage': 'rgba(128,0,0,0.3)', # Maroon with some transparency
    'default': '#D6D6CE' # Light Gray
}

def empty_map(df, geojsonfile):
    '''
    Sets default choropleth map

    Input:
        - df (pd): Dataframe 
        - geojsonfile: GEOJSON

    Return: Choropleth map
    '''

    df.sort_values("geoid10", inplace=True)
    df.drop_duplicates(subset=['geoid10'])

    trace0 = px.choropleth(
            df, 
            geojson = geojsonfile, 
            locations = 'geoid10', 
            featureidkey = "properties.geoid10", 
            color_discrete_sequence = [colors['default']],
            projection = "gnomonic"
            )
    trace0.update_geos(fitbounds = "locations", visible = False)
    trace0.update_traces(marker_line_color = "white", marker_line_width=0.5)
    trace0.layout.update(
        width = 800, height = 600,
        margin = {"r":0,"t":10,"l":0,"b":0},
        showlegend = False 
        )

    return trace0

def socioeconomic_map(df, geojsonfile):
    '''
    Generates choropleth map for the socioeconomic variable

    Input:
        - df (pd): Dataframe 
        - geojsonfile: GEOJSON

    Return: Choropleth map
    '''
    trace1 = px.choropleth(
            df,
            geojson = geojsonfile, 
            color = "bin_value_bin",
            color_discrete_map={'Q4': '#FFAD05',
                                'Q3': '#FED628',
                                'Q2': '#F1F374',
                                'Q1': '#D6D6CE'},
            labels = {'bin_value_bin': ''},
            locations = 'geoid10', 
            featureidkey = "properties.geoid10", 
            projection = 'gnomonic'
            )
    trace1.update_geos(fitbounds = "locations", visible = False)
    trace1.update_traces(marker_line_color = "white", marker_line_width = 0.5)
    trace1.layout.update(
        legend = dict(y=0.9, x=0.8),
        coloraxis_colorbar = dict(
            thicknessmode = "pixels", thickness = 30, ticks="inside",
            lenmode="pixels", len = 175
            ),
        font_color = colors['font'],
        width = 800, height = 600,
        margin = {"r":0,"t":10,"l":0,"b":0}, 
        showlegend = True
        )
    return trace1

def facilities_map(df, geojsonfile):
    '''
    Generates scatter geo map for the Public Facility

    Input:
        - df (pd): Dataframe 
        - geojsonfile: GEOJSON

    Return: Choropleth map
    '''
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
        paper_bgcolor = colors['bg'], 
        plot_bgcolor = colors['bg'],
        font_color = colors['font'], 
        margin = {"r":0,"t":10,"l":0,"b":0} 
        )

    return trace2

def isochrone_map(df, geojsonfile):
    '''
    Generates isochrone map as a choropleth to trace boundaries

    Input:
        - df (pd): Dataframe 
        - geojsonfile: GEOJSON

    Return: Choropleth map
    '''
    trace3 = px.choropleth(
            df,
            geojson = geojsonfile, 
            locations = 'full_address',
            featureidkey = "properties.full_address", 
            color_discrete_sequence = [colors['bg']], 
            projection = "gnomonic" 
            )
    trace3.update_geos(fitbounds = "locations", visible = False) 
    trace3.update_traces(marker_line_color = 'black', marker_line_width=0.5)
    trace3.layout.update(
        width = 900, height = 350,
        paper_bgcolor = colors['bg'],
        plot_bgcolor = colors['bg'], 
        margin = {"r":0,"t":10,"l":0,"b":0},
        showlegend = False
        )

    return trace3

def histogram(df, variable):
    '''
    Generates histogram for the socioeconomic variable

    Input:
        - df (pd): Dataframe 
        - variable (str): Selected socioeconomic variable

    Return: Histogram
    '''
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