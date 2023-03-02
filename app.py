# These are the packages. You may need to pip install some of them.
# These should be included in the virtual environment
from dash import Dash, dcc, html, Input, Output
import utility as ut
import urllib.request, json 
import plotly.express as px 
import pandas as pd
import dash_bootstrap_components as dbc
import requests
import copy as cp

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

#------- DATA FOR SOCIOECONOMIC VARIABLE -------#
# Importing from direct link
data = requests.get("https://uchicago.box.com/shared/static/1i3rrpl2t8yvz9z25nrc7rzwauopkd34.xlsx").content
# Reading file to pandas
cleanedData = pd.read_excel(data, sheet_name = "in", dtype={'GEOID': str, 'Longitude': float, 'Latitude': float, 
                                                            'geometry': str, 'indicator': str, 'value': float,
                                                            'bin_value_bin': str})
cleanedData = cleanedData.rename(columns={'indicator': 'SocEconVar', 'GEOID': 'geoid10'}) 

#------- GEOJSON TO DISPLAY SOCIOECONOMIC VARIABLE -------#
# Importing the city of chicago geojson community level map
with urllib.request.urlopen("https://uchicago.box.com/shared/static/piwa29gvoz137t73nyxoogsntqhilune.geojson") as url:
        chicagoMap = json.load(url)

#------- DATA TO DISPLAY PUBLIC SERVICES/PROVISIONS -------#
# Importing from direct link
raw_data2 = requests.get("https://uchicago.box.com/shared/static/lvznfe58bg4o5g7nhqfxt8lbn0e4hyba.xlsx").content
# Reading file to pandas
cleanedData2 = pd.read_excel(raw_data2, sheet_name = "in", 
                             dtype={'ADDRESS': str, 'CITY': str, 'STATE': str, 
                                   'ZIP': str, 'full_address': str, 'coords': tuple,
                                    'type': str, 'isochrones': str
                                    })
cleanedData2[['latitude', 'longitude']] = cleanedData2['coords'].apply(\
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
                style={"textDecoration": "none", 'font-family': 'Times New Roman'},
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

    html.H5('''
        Visualize the time-distance coverage of public facilities/services over 
        socioeconomic data to identify vulnerabilities in the City of Chicago.
        ''', style = {'font-family': 'Gotham', 'margin' : '50px'}), # Main description
    
    html.Div([
    
        html.Div([
            dcc.Dropdown(
                cleanedData['SocEconVar'].unique(),
                placeholder = 'Select a Socioeconomic Variable',
                searchable = False,
                id = 'SocEconVar',
                style = {'margin-left': '20px', 'margin-bottom': '30px'}
            ),
            
            dcc.Dropdown(
                cleanedData2['type'].unique(),
                placeholder = 'Select a Public Facility',
                searchable = False,
                id = 'ProvisionVar',
                style = {'margin-left': '20px'}
            )
        ], className="2 columns",
           style = {'width': '40%', 'display': 'inline-block'}),

        html.Div(
            id = 'map', style={'margin-left': '50px', 'width':'50%', 'display': 'inline-block'},
            className="four columns"),
        ], 
        className="row"
    )

])


@app.callback(
    Output(component_id = 'map', component_property = 'children'),
    Input(component_id = 'SocEconVar', component_property = 'value'),
    Input(component_id = 'ProvisionVar', component_property = 'value')
)
def update_figure(SocEconValue, ProvisionValue):

    global cleanedData
    global cleanedData2
    global chicagoMap

    socEconData = cleanedData[cleanedData['SocEconVar'] == SocEconValue]
    provisionsData = cleanedData2[cleanedData2['type'] == ProvisionValue]

    if SocEconValue and ProvisionValue:
        trace1 = ut.socioeconomic_map(socEconData, chicagoMap)
        base_map = cp.deepcopy(trace1) # Base map copy to add layers
        trace2 = ut.facilities_map(provisionsData, chicagoMap)
        joined_map = base_map.add_trace(trace2.data[0]) # Overlayed map
        return [dcc.Graph(figure = joined_map)]
    elif SocEconValue and not ProvisionValue:
        base_map = ut.socioeconomic_map(socEconData, chicagoMap)
        return [dcc.Graph(figure = base_map)]
    elif ProvisionValue and not SocEconValue:
        trace1 = ut.empty_map(cleanedData, chicagoMap)
        empty_map = cp.deepcopy(trace1) # Base map copy to add layers
        facilities_map = ut.facilities_map(provisionsData, chicagoMap)
        joined_map = empty_map.add_trace(facilities_map.data[0]) # Overlayed map
        return [dcc.Graph(figure = joined_map)]
    else:
        empty_map = ut.empty_map(cleanedData, chicagoMap)
        return [dcc.Graph(figure = empty_map)]


# Runs app from terminal with "python3 app.py". Once you run the map, you can exit with 'ctrl + c'
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port='8090', debug = False) # If there is a port error you can change it to '8080'