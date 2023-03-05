from dash import Dash, dcc, html, Input, Output
import utility as ut
import json 
import pandas as pd
import dash_bootstrap_components as dbc
import copy as cp

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

#------- GEOJSON MAP OF THE CITY OF CHICAGO -------#
with open("Boundaries - Census Tracts - 2010.geojson") as gjs:
        chicagoMap = json.load(gjs)

#------- ISOCHRONES' GEOJSON -------#
with open("isochrone_best.json") as js:
        isochroneMaps = json.load(js)

#------- DATA FOR SOCIOECONOMIC VARIABLE -------#
cleanData = pd.read_excel('final_geo_SEI.xlsx', sheet_name = "in", dtype={'GEOID': str, 'Longitude': float, 'Latitude': float, 
                                                            'geometry': str, 'indicator': str, 'value': float,
                                                            'bin_value_bin': str})
cleanData = cleanData.rename(columns={'indicator': 'SocEconVar', 'GEOID': 'geoid10'}) 

#------- DATA TO DISPLAY PUBLIC FACILITIES/PROVISIONS -------#
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
                        dbc.Col(html.Img(src=UChi_logo, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Pro-Vision")),
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

            dcc.Dropdown( # Choose Socioeconomic Variable
                cleanData['SocEconVar'].unique(),
                placeholder = 'Select a Socioeconomic Variable',
                searchable = True,
                id = 'SocEconVar',
                style = {'margin-left': '20px', 'margin-bottom': '30px'}
            ),
            
            dcc.Dropdown( # Choose Public Facility
                cleanData2['type'].unique(),
                placeholder = 'Select a Public Facility',
                searchable = True,
                id = 'ProvisionVar',
                style = {'margin-left': '20px', 'margin-bottom': '30px'}
            ),

            html.H5( # Count number of facilities
                id = 'facility-counter',
                style = {'margin-left': '45px', 'margin-bottom': '10px'}
            ),

            html.Div( # Display map
            id = 'hist'
            )

        ], className="2 columns",
           style = {'width': '40%', 'display': 'inline-block'}),

        html.Div( # Display map
            id = 'map', style={'margin-left': '50px', 'width':'50%', 
                               'display': 'inline-block'},
            className="four columns")
        ], 
        className="row"
    )

])

@app.callback(
    Output(component_id = 'hist', component_property = 'children'),
    Input(component_id = 'SocEconVar', component_property = 'value')
)
def update_figure(SocEconValue):
    if SocEconValue:
        socEconData = cleanData[cleanData['SocEconVar'] == SocEconValue]
        hist = ut.histogram(socEconData, 'value')
        return [dcc.Graph(figure = hist)]

@app.callback(
    Output(component_id = 'facility-counter', component_property = 'children'),
    Input(component_id = 'ProvisionVar', component_property = 'value')
)
def update_counter(ProvisionValue):

    if ProvisionValue:
        global cleanData2
        provisionsData = cleanData2[cleanData2['type'] == ProvisionValue]
        counter = len(provisionsData['type'])
        return f'Number of public facilities: {counter}'
    else:
        return f'Number of public facilities: 0'

@app.callback(
    Output(component_id = 'map', component_property = 'children'),
    Input(component_id = 'SocEconVar', component_property = 'value'),
    Input(component_id = 'ProvisionVar', component_property = 'value')
)
def update_figure(SocEconValue, ProvisionValue):

    global chicagoMap
    global isochroneMaps

    global cleanData
    global cleanData2

    if SocEconValue and ProvisionValue:
        socEconData = cleanData[cleanData['SocEconVar'] == SocEconValue]
        provisionsData = cleanData2[cleanData2['type'] == ProvisionValue]

        trace1 = ut.socioeconomic_map(socEconData, chicagoMap)
        base_map = cp.deepcopy(trace1) # Base map copy to add layers
        trace2 = ut.facilities_map(provisionsData, chicagoMap)
        joined_map = base_map.add_trace(trace2.data[0]) # Overlayed map

        isochroneMap = isochroneMaps[ProvisionValue]
        coverage = ut.isochrone_map(cleanData2, isochroneMap) # Coverage map
        fullMap = joined_map.add_trace(coverage.data[0]) # Overlayed map w/coverage

        return [dcc.Graph(figure = fullMap)]
    
    elif SocEconValue and not ProvisionValue:
        socEconData = cleanData[cleanData['SocEconVar'] == SocEconValue]

        trace1 = ut.socioeconomic_map(socEconData, chicagoMap)

        return [dcc.Graph(figure = trace1)]
    elif ProvisionValue and not SocEconValue:
        provisionsData = cleanData2[cleanData2['type'] == ProvisionValue]

        trace0 = ut.empty_map(cleanData, chicagoMap)
        empty_map = cp.deepcopy(trace0) # Base map copy to add layers
        facilities_map = ut.facilities_map(provisionsData, chicagoMap) # Facilities map
        joined_map = empty_map.add_trace(facilities_map.data[0]) # Overlayed map

        isochroneMap = isochroneMaps[ProvisionValue]
        coverage = ut.isochrone_map(cleanData2, isochroneMap) # Coverage map
        fullMap = joined_map.add_trace(coverage.data[0]) # Overlayed map w/coverage

        return [dcc.Graph(figure = fullMap)]
    else:
        empty_map = ut.empty_map(cleanData, chicagoMap)

        return [dcc.Graph(figure = empty_map)]


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port='8090', debug = False) 