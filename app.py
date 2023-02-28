# These are the packages. You may need to pip install some of them.
# These should be included in the virtual environment
from dash import Dash, dcc, html, Input, Output
import urllib.request, json 
import plotly.express as px 
import pandas as pd
import dash_bootstrap_components as dbc
# import numpy as np
import requests
# import openpyxl
import copy as cp
# from plotly.subplots import make_subplots

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.config.suppress_callback_exceptions = True

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

# Setting general colors
colors = { 
    'bg': 'rgba(0,0,0,0)',
    'font': ' #767676'
}

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
        Visualize the travel time-distance of public facilities/services on 
        socioeconomic data to identify vulnerabilities in the City of Chicago.
        ''', style = {'font-family': 'Gotham', 'margin' : '50px'}), # Main description
    html.Div([
            dcc.Dropdown(
                cleanedData['SocEconVar'].unique(),
                placeholder = 'Select a Socioeconomic Variable',
                searchable = False,
                id = 'SocEconVar'
            )], style = {'width': '48%', 'display': 'inline-block'}),
    html.Div([
            dcc.Dropdown(
                cleanedData2['Provision'].unique(),
                placeholder = 'Select a Public Facility',
                searchable = False,
                id = 'ProvisionVar'
            )], style = {'width': '48%', 'display': 'inline-block'}),
    html.Div(id = 'map') # Displaying joined map
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

    #------- CHOROPLETH MAP TO DISPLAY SOCIOECONOMIC VARIABLE -------#
    trace1 = px.choropleth(
            socEconData, # Socioeconomic data
            geojson = chicagoMap, # Community Level Geojson
            color = 'Value', # Setting color intensity by the values of HCSNS_2016-2018 (i.e., safety variable)
            color_continuous_scale = 'PuBu', # Choosing color
            locations = 'Community Area', # Identifies locations from geojson
            featureidkey = "properties.pri_neigh", # Consider pri_neigh as key from geojson dictionary
            labels = 'Label', # Labelling socioeconomic variable
            )
    trace1.update_geos(fitbounds = "locations", visible = False) # Maps shapefile boundary locations from geojson
    trace1.layout.update(
        margin = {"r":20,"t":20,"l":20,"b":20}, # Sets boundaries of map
        showlegend = True # Show legend
        )

    base_map = cp.deepcopy(trace1) # Creating a base map to add layers

    #------- SCATTER MAP FOR PUBLIC SERVICES/PROVISIONS -------#
    trace2 = px.scatter_geo(provisionsData, lat = 'latitude', lon = 'longitud', 
                            hover_data={'Provision': False, 'longitud': False, 
                                        'latitude': False, 'ADDRESS': True, 
                                        'ZIP': True})
    trace2.layout.update(
        paper_bgcolor = colors['bg'], # Sets transparent background
        plot_bgcolor = colors['bg'], # Sets transparent background
        font_color = colors['font'], # Sets font color
        margin = {"r":20,"t":20,"l":20,"b":20} # Sets boundaries of map
        )

    #------- FULL MAP WITH JOINED TRACES -------#
    joined_map = base_map.add_trace(trace2.data[0])

    return [dcc.Graph(figure = joined_map)]

# Runs app from terminal with "python3 app.py". Once you run the map, you can exit with 'ctrl + c'
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port='8080', debug = False) # If there is a port error you can change it to '8080'