#use plotly express to create a line chart
# X axis is the year
#Y axis is the % of bee colonies
#colour should represent states -> Texas, New Mexico, New York
#dropdown options should be the list of things affecting the bees


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go

import os
import pandas as pd

app = dash.Dash(__name__)

#------------------------------------------------------------------------
# Import and clean data

path = os.path.join('..','Data','intro_bees.csv')
df = pd.read_csv(path)
df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
#print(df[:5])

#------------------------------------------------------------------------
# app layout

app.layout = html.Div([

    ########## title #########
    html.H1('% of bee colonies affected', style = {'text-align': 'center'}),

    ########## disease selection drowdown menu #########
    html.Div([
        dcc.Dropdown(id="slct_disease",
                    options=[
                        {"label": disease, "value": disease}
                        for disease in set(df['Affected by'])],
                    multi=False,
                    value='Varroa_mites'
                    ),

        ########## Display selected disease #########
        html.Div(id='disease_container', children=[])], 
        style={'width': '48%', 'display': 'inline-block'}),

    html.Br(),

    ########## graph #########
    dcc.Graph(id='line_chart', figure={}),

    ########## state selection ##################
    html.Br(),

    html.Div([
  
    dcc.Dropdown(id="slct_state",
                options=[
                    {"label": state, "value": state}
                    for state in set(df['State'])],
                multi=True,
                value=['Texas', 'New Mexico', 'New York'],
                style={'width': "90%",'float': 'left'}
                )],

    style={'width': '48%', 'display': 'inline-block'})

])

#callback

@app.callback(
    [Output(component_id='disease_container', component_property='children'),
     Output(component_id='line_chart', component_property='figure')],
    [Input(component_id='slct_disease', component_property='value'),
    Input(component_id='slct_state', component_property='value') ]
)

def update_graph(disease_selected, state_selected):

    disease_container = "User chose Affected by: {}".format(disease_selected)

    dff = df.copy()
    if type(state_selected) is list:
        dff = dff.loc[dff['State'].isin(state_selected)]
    else:
        dff = dff.loc[dff['State'] == state_selected]

    dff=dff[dff['Affected by'] == disease_selected]

    if type(state_selected) is list:
        fig = px.line(
        data_frame = dff,
        x = 'Year',
        y = 'Pct of Colonies Impacted',
        color = 'State',
        title = '% of bee colonies affected by {}'.format(disease_selected),
        template='plotly_dark'
    )
    else:
        fig = px.line(
        data_frame = dff,
        x = 'Year',
        y = 'Pct of Colonies Impacted',
        title = '% of bee colonies affected by {}'.format(disease_selected),
        template='plotly_dark'
    )



    return disease_container , fig


#------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug = True)