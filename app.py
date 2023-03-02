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
raw_data = requests.get("https://uchicago.box.com/shared/static/ooyygpkhml7vd6p170e3tgl303cfkkek.xlsx").content
# Reading file to pandas
cleanedData = pd.read_excel(raw_data, sheet_name = "Community areas", dtype={'Layer': str, 'Name': str, 'GEOID': int, 
                                                                      'SocEconVar': str, 'Value': str, 'Quintiles': int,
                                                                      'Label': str})
cleanedData = cleanedData.rename(columns={'Name': 'Community Area'}) 
# Getting rid of commas in the variable Value
cleanedData['Value'] = cleanedData['Value'].str.replace(',','')
# Parsing Value to numeric
cleanedData['Value'] = pd.to_numeric(cleanedData['Value'], downcast='float')

#------- GEOJSON TO DISPLAY SOCIOECONOMIC VARIABLE -------#
# Importing the city of chicago geojson community level map
with urllib.request.urlopen("https://uchicago.box.com/shared/static/0hyrwzbja479o01f0ke99b418zvsudjr.geojson") as url:
        chicagoMap = json.load(url)

#------- DATA TO DISPLAY PUBLIC SERVICES/PROVISIONS -------#
# Importing from direct link
raw_data2 = requests.get("https://uchicago.box.com/shared/static/tuq2cw0d18e6wsa4mixvos1g1lp5z3yp.xlsx").content
# Reading file to pandas
cleanedData2 = pd.read_excel(raw_data2, sheet_name = "Police_Stations_-_Map", 
                            dtype={'Provision': str, 'ADDRESS': str, 'ZIP': str, 
                                    'latitude': float, 'longitud': float})

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
            dcc.Dropdown(
                cleanedData['SocEconVar'].unique(),
                placeholder = 'Select a Socioeconomic Variable',
                searchable = False,
                id = 'SocEconVar'
            )], style = {'width': '30%', 'margin-left': '100px',
                         'margin-right': '50px', 'display': 'inline-block'}),
    html.Div([
            dcc.Dropdown(
                cleanedData2['Provision'].unique(),
                placeholder = 'Select a Public Facility',
                searchable = False,
                id = 'ProvisionVar'
            )],
            style = {'width': '30%', 'display': 'inline-block'}),
    html.Div(id = 'map', 
             style={"height": 1500, 'display': 'inline-block'}) # Displaying joined map
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
    provisionsData = cleanedData2[cleanedData2['Provision'] == ProvisionValue]

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