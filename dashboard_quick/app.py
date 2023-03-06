from dash import Dash, dcc, html, Input, Output 
import utility as ut # Graph functions
import json
import pandas as pd 
import dash_bootstrap_components as dbc # Template
import copy as cp

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

#------- GEOJSON CENSUS TACTS OF THE CITY OF CHICAGO -------#
with open("Boundaries - Census Tracts - 2010.geojson") as gjs:
        chicagoMap = json.load(gjs)

#------- MERGED/APPENDED ISOCHRONES' GEOJSON -------#
with open("iso_coords.geojson") as js:
        isochroneMaps = json.load(js)

#------- DATA FOR SOCIOECONOMIC VARIABLE -------#
# cleanData = pd.read_excel('final_geo_SEI.xlsx', sheet_name = "in", 
#                           dtype={'GEOID': str, 'Longitude': float, 'Latitude': float, 
#                                  'geometry': str, 'indicator': str, 'value': float,
#                                  'bin_value_bin': str})
cleanData = pd.read_csv('geo_sei_labeled.csv', 
                          dtype={'GEOID': str, 'Longitude': float, 'Latitude': float, 
                                 'geometry': str, 'indicator': str, 'value': float,
                                 'bin_value_bin': str})
cleanData = cleanData.rename(columns={'indicator': 'SocEconVar', 'GEOID': 'geoid10'}) 

#------- DATA FOR PUBLIC FACILITIES/PROVISIONS -------#
cleanData2 = pd.read_csv('prov_isoID.csv')
cleanData2[['latitude', 'longitude']] = cleanData2['coords'].apply(\
            lambda x: pd.Series(str(x).strip('()').split(',')))

#------- NAVIGATION BAR -------#
UChi_logo = "https://www.lib.uchicago.edu/static/base/images/unvlogo-white.png"
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=UChi_logo, height="30px")), # Logo
                        dbc.Col(dbc.NavbarBrand("Pro-Vision")), # Team name
                    ],
                    align="center",
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
        ]
    ),
    color = "#800000",
    dark = True,
)

#------- DASHBOARD STRUCTURE -------#
app.layout = html.Div(children = [
    navbar, # Navigation bar

    html.Div([]), # Space
    
    html.Div([
    
        html.Div([
     
            html.H5( # Main description
            '''
            Visualize the time-distance coverage of public facilities over 
            socioeconomic data to identify vulnerabilities in the City of Chicago.
            ''', style = {'margin' : '50px', 'margin-bottom': '30px'}
            ),

            dcc.Dropdown( # Socioeconomic Variable Menu
                cleanData['SocEconVar'].unique(),
                placeholder = 'Select a Socioeconomic Variable',
                searchable = True,
                id = 'SocEconVar',
                style = {'margin-left': '20px', 'margin-bottom': '30px'}
            ),
            
            dcc.Dropdown( # Public Facility Menu
                cleanData2['type'].unique(),
                placeholder = 'Select a Public Facility',
                searchable = True,
                id = 'ProvisionVar',
                style = {'margin-left': '20px', 'margin-bottom': '30px'}
            ),

            html.H5( # Facility counter
                id = 'facility-counter',
                style = {'margin-left': '45px', 'margin-bottom': '10px'}
            ),

            html.Div( # Display histogram
            id = 'hist'
            )

        ],
           style = {'width': '40%', 'display': 'inline-block'}),

        html.Div( # Display map
            id = 'map', style={'margin-left': '50px', 'width':'50%', 
                               'display': 'inline-block'},
            className="four columns")
        ], 
        className="row"
    )

])

@app.callback( # Callback histogram
    Output(component_id = 'hist', component_property = 'children'),
    Input(component_id = 'SocEconVar', component_property = 'value')
)
def update_figure(SocEconValue):
    '''
    Generates histogram plot for socioeconomic variable

    Input:
        - SocEconValue (str): Value selected from the Socioeconomic Variable Dropdown Menu

    Return: Histogram
    '''
    if SocEconValue:
        socEconData = cleanData[cleanData['SocEconVar'] == SocEconValue]
        hist = ut.histogram(socEconData, 'value')
        return [dcc.Graph(figure = hist)]

@app.callback( # Callback facility counter
    Output(component_id = 'facility-counter', component_property = 'children'),
    Input(component_id = 'ProvisionVar', component_property = 'value')
)
def update_counter(ProvisionValue):
    '''
    Generates a facility counter 

    Input:
        - ProvisionValue (str): Value selected from the Facility dropdown menu

    Return (str): Counter
    '''
    if ProvisionValue:
        global cleanData2
        provisionsData = cleanData2[cleanData2['type'] == ProvisionValue]
        counter = len(provisionsData['type'])
        return f'Number of public facilities: {counter}'
    else:
        return f'Number of public facilities: 0'

@app.callback( # Generate complete overlayed map
    Output(component_id = 'map', component_property = 'children'),
    Input(component_id = 'SocEconVar', component_property = 'value'),
    Input(component_id = 'ProvisionVar', component_property = 'value')
)
def update_figure(SocEconValue, ProvisionValue):
    '''
    Display the GEOJSON map of chicago with socioeconomic data, public facility data
        and coverage data (Isochrone GEOJSON)

    Input:
        - SocEconValue (str): Value selected from the Socioeconomic dropdown menu 
        - ProvisionValue (str): Value selected from the Facility dropdown menu

    Return: Geo Choropleth and/or Geo Scatter Graph with or without isochrones
    '''

    global chicagoMap # Chicago Map GEOJSON
    global isochroneMaps # isochrones' GEOJSONs

    global cleanData # Cleaned Socioeconomic data
    global cleanData2 # Cleaned Public Facilities data

    if SocEconValue and ProvisionValue:
        socEconData = cleanData[cleanData['SocEconVar'] == SocEconValue] 
        provisionsData = cleanData2[cleanData2['type'] == ProvisionValue]

        trace1 = ut.socioeconomic_map(socEconData, chicagoMap) # Load socioeconomic map
        base_map = cp.deepcopy(trace1) # Set socioeconomic map as base map
        trace2 = ut.facilities_map(provisionsData, chicagoMap) # Load facilities map
        joined_map = base_map.add_trace(trace2.data[0]) # Overlay facilities to socioeconomic map

        isochroneMap = isochroneMaps[ProvisionValue] # Filter GEOJSON file by facility
        coverage = ut.isochrone_map(provisionsData, isochroneMap) # Load isochrone map
        fullMap = joined_map.add_trace(coverage.data[0]) # Overlayed isochrone map to the others

        return [dcc.Graph(figure = fullMap)]
    
    elif SocEconValue and not ProvisionValue:
        socEconData = cleanData[cleanData['SocEconVar'] == SocEconValue]
        trace1 = ut.socioeconomic_map(socEconData, chicagoMap) # Load socioeconomic map

        return [dcc.Graph(figure = trace1)]
    
    elif ProvisionValue and not SocEconValue:
        provisionsData = cleanData2[cleanData2['type'] == ProvisionValue]

        trace0 = ut.empty_map(cleanData, chicagoMap) # Load empty map
        empty_map = cp.deepcopy(trace0) # Copy base map to overlay
        facilities_map = ut.facilities_map(provisionsData, chicagoMap) # Load facilities map
        joined_map = empty_map.add_trace(facilities_map.data[0]) # Overlay facilities to empty map

        isochroneMap = isochroneMaps[ProvisionValue] # Filter GEOJSON file by facility
        coverage = ut.isochrone_map(provisionsData, isochroneMap) # Load isochrone map
        fullMap = joined_map.add_trace(coverage.data[0]) # Overlayed isochrone map to the others

        return [dcc.Graph(figure = fullMap)]
    else:
        empty_map = ut.empty_map(cleanData, chicagoMap) # Set empty map

        return [dcc.Graph(figure = empty_map)]


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port='4444', debug = False) 