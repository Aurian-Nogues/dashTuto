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

    ########## dropdown menu #########
    dcc.Dropdown(id="slct_disease",
                 options=[
                     {"label": disease, "value": disease}
                      for disease in set(df['Affected by'])],
                 multi=False,
                 value='Varroa_mites',
                 style={'width': "40%"}
                 ),

    ########## output to display ??? #########
    html.Div(id='output_container', children=[]),
    html.Br(),

    ########## graph #########
    dcc.Graph(id='line_chart', figure={})
])

#callback

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='line_chart', component_property='figure')],
    [Input(component_id='slct_disease', component_property='value')]
)

def update_graph(option_selected):

    container = "User chose Affected by: {}".format(option_selected)

    dff = df.copy()
    myStates = ['Texas', 'New Mexico', 'New York']
    dff = dff.loc[dff['State'].isin(myStates)]
    dff=dff[dff['Affected by'] == option_selected]

    fig = px.line(
        data_frame = dff,
        x = 'Year',
        y = 'Pct of Colonies Impacted',
        color = 'State',
        title = '% of bee colonies affected by Varroa_mites',
        template='plotly_dark'
    )

    return container, fig


#------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug = True)