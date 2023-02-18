from dash import Dash, dcc, html, Input, Output
import urllib.request, json 
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import requests

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

colors = {
    'background': '#111111',
    'text': '#000000'
}

app.layout = html.Div([
    html.H1('Pro-Vision'),
    html.H3('''
        Visualize the travel time-distance of public facilities/services on 
        socioeconomic data to identify vulnerabilities in the City of Chicago.
        '''),
    html.P("Select a socioeconomic indicator:"),
    dcc.RadioItems(
        id='socInd', 
        options=["Income per Capita", "Neighborhood Safety", "Inequality"],
        value="Neighborhood Safety",
        inline=True
    ),
    dcc.Graph(id="socInd")
])

@app.callback(
    Output("graph", "figure"), 
    Input("Neighborhood Safety", "value"))
def display_choropleth(   ):
    raw_data = requests.get("https://uchicago.box.com/shared/static/mxv5z4eommsiaydm9rru69gj5avygxto.xlsx").content
    data = pd.read_csv(raw_data, sheet_name = "Community Areas", dtype={'Layer': str, 'Name': str, 'GEOID': int, 
                                                                      'HCSNS_2016-2018': str})
    data['HCSNS_2016-2018'] = data['HCSNS_2016-2018'].str.replace(',','')
    data['HCSNS_2016-2018'] = pd.to_numeric(data['HCSNS_2016-2018'], downcast='int')
    cleanedData = data.rename(columns={'Name': 'pri_neigh'})
    # df = px.data.election() 
    with urllib.request.urlopen("https://data.cityofchicago.org/api/geospatial/bbvz-uum9?method=export&format=GeoJSON") as url:
        chicagoMap = json.load(url)
    # geojson = px.data.election_geojson()
    fig = px.choropleth(
        cleanedData, geojson=chicagoMap, color='HCSNS_2016-2018',
        locations="pri_neigh", featureidkey="properties.pri_neigh",
        range_color=[924, 80076], labels={'unemp':'Number of people whom reported to feel safe'})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port='8090', debug=True)