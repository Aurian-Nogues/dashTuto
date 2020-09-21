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


#HTML div that contains the layout of the page and all elements
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

#connect plotly graphs components to dash
#callback use component_id and omponent_property to connect elements
#outputs refers to things where the data goes, here it's the output_container div and my_bee_map frapth
#inputs are what we get in, it's from the slct_year dropdown in that case

@app.callback(
    #do not use list if only one output -> remove external brackets
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)

#under each callback there needs to be a function with each argument connecting to an input
#this argument refers to the component property of the input
#the returns of the function connect to the outputs, they need to be returned in the same order as the outputs are declared in callback

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    # Plotly Graph objects (will be depreciated over time
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )


    return container, fig

#------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug = True)