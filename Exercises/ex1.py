#use plotly express to plot a bar chart
#X-axis is the state
#Y axis is the % of bee colonies

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
    html.H1('% of bee colonies affected by Varroa mites', style = {'text-align': 'center'}),

    ########## dropdown menu #########
    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018}],
                 multi=False,
                 value=2015,
                 style={'width': "40%"}
                 ),

    ########## output to display ??? #########
    html.Div(id='output_container', children=[]),
    html.Br(),

    ########## graph #########
    dcc.Graph(id='my_bee_map', figure={})
])

#callback

@app.callback(
    #do not use list if only one output -> remove external brackets
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):

    container = "The year chosen by user was: {}".format(option_slctd)
    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

     # Plotly Express

    fig = px.bar(
    data_frame = dff, 
    x = 'State', 
    y= 'Pct of Colonies Impacted',
    color = 'Pct of Colonies Impacted',
    color_continuous_scale=px.colors.sequential.YlOrRd,
    title = '% of bee colonies affected by Varroa_mites',
    template='plotly_dark'
)


    return container, fig



#------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug = True)