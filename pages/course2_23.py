
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 13:07:13 2023

@author: u1130196
"""

# Run this app with `python_dbc.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import pandas as pd

dash.register_page(__name__, name='Course 2')

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP])

#read data
df = pd.read_csv('https://raw.githubusercontent.com/RSESEdDev/EdAnalytics/main/progress_esdh_2023.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/RSESEdDev/EdAnalytics/main/logs_ESDH_2023.csv')

fig3 = px.bar(df, x="ID number", y=["1.1 Quiz - What is Data?","1.2 Quiz - Relational Databases","1.3 Quiz - Non-Relational Databases"], title="Data Hub Quiz Activity Completion")
fig4 = px.bar(df2, x="Section", y=["ID"], title="Data Hub Log Test")

dropdown = html.Div(
    [
        dbc.Label("Select Quiz (y-axis)"),
        dcc.Dropdown(
            ["1.1 Quiz - What is Data?", "1.2 Quiz - Relational Databases", "1.3 Quiz - Non-Relational Databases"],
            "1.1 Quiz - What is Data?",
            id="dropdown1",
            multi=True,
            clearable=False
        ),
    ],
    className="mb-4",
)

table = html.Div(
    dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i, "deletable": True} for i in df.columns],
        data=df.to_dict("records"),
        page_size=10,
        editable=True,
        cell_selectable=True,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
        row_selectable="multi",
    ),
    className="dbc-row-selectable",
)


controls = dbc.Card(
    [dropdown],
    body=True,
)
#tabs
tab1 = dbc.Tab([dcc.Graph(id="graph2_chart")], label="Sample Barchart")
tab3 = dbc.Tab([table], label="Barchart Data Table", className="p-4")
tabs = dbc.Card(dbc.Tabs([tab1, tab3]))

#HTML Layouts
layout = dbc.Container(
        [
           html.Div
                (html.H2
                     (children='''Course 2, Sem 1, 2023''',
                      style={'height':'40px',
                               'colour': 'black',
                               'padding-left':'2%',
                               'display':'inline-block'})),
        dbc.Row(
            [
                dbc.Col(
                    [
                        controls,

                    ],
                    width=4,
                ),
                dbc.Col([tabs], width=8),
              ]
           ),

        dbc.Row(
            [
                dbc.Col(html.Div(
                    dcc.Graph(
                id='example-graph3', figure=fig3, className="m-3 border"))),
                
                dbc.Col(html.Div(
                    dcc.Graph(
                id='example-graph4', figure=fig4, className="m-3 border"))),
            ]
        ),
    ],
    fluid=True,
    className="dbc",
)
         
    
@callback(
    Output("graph2_chart","figure"),
    Input("dropdown1", "value"),
    )

def update_barcharts(dropdown1): 
    if dropdown1 is None:
        return {}, {}, []
    
    fig = px.bar(
             df, 
             x="ID number",
             y=dropdown1, 
             title="Data Hub Quiz Activity Completion")
    fig.update_xaxes (type='category')
    return fig  



if __name__ == '__main__':
    app.run_server(debug=True)