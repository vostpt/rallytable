# -*- coding: utf-8 -*-

# Import libraries 

import pandas as pd 
import io
import requests
import plotly.express as px 

# Import csv file from URL 

url="https://bot-api.vost.pt/rally-pt/rallyptdata.csv"
s=requests.get(url).content

# Convert csv file 

df=pd.read_csv(io.StringIO(s.decode('utf-8')))

# Plot mapbox map with dataframe variables

# Table generation starts here 
# Import libraries to generate table

import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html

# Generate dataframe for table with only the relevant columns

df_table=df.filter(['name','stage','capacity'])

# Conditional formatting 

df_table['opstatus'] = df['capacity'].apply(lambda x:
    '🔴' if x > 89 else (
    '🟠' if x > 69 else (
    '🟡' if x > 49 else (
    '🟢' if x > 9 else ''
))))

# Create a column named "id" based on the index of the dataframe

df_table['id'] = df_table.index 

# Create Table and assign it an id for app callback 

newtable = dash_table.DataTable(
    id='table',
    data=df_table.to_dict('records'),
    columns=[
            {'name':'Zona Espectáculo', 'id':'name'},
            {'name':'Troço', 'id':'stage'},
            {'name':'Status', 'id':'opstatus'},        
    ],
    # Define table styling 
    fixed_rows={'headers': True},
    style_table={'height': 400},  

    # Condition resizing of columns 
    style_cell_conditional=[
        {'if': {'column_id': 'name'},
         'width': '10%'},
         {'if': {'column_id': 'opstatus'},
         'width': '15%'},
        {'if': {'column_id': 'stage'},
         'width': '10%'},
    ],
    # Define overall styling for the table
    style_as_list_view=True,
     style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
    style_cell={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white',
        'fontSize':16, 'font-family':'Open Sans',
    },
    )

# App starts here 

# Import Libraries

import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template


# Get template for layout. This saves time. 

load_figure_template("bootstrap")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],title='Rally de Portugal Vodafone 2021',update_title=None,
                meta_tags=[{'name': 'viewport',
                           'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
        )

server = app.server

# Google Analytics goes here 



# Design top Navbar 

# Design layout 

app.layout = dbc.Container(
    [
        dcc.Interval(
            id='interval-component',
            interval=60*1000, # in milliseconds
            n_intervals=0
        ),
    
    html.Hr(),
    dbc.Row(
        [
       
        dbc.Col(id='table',lg=6),
        ], 
    ),
    

    ],

    fluid=True,
)

@app.callback(
    Output('table', 'children'),
    [Input('interval-component', "n_intervals")]
)

def streamTable(value):
    
    global table
    # Assing CSV to dataframe df 
    url="https://bot-api.vost.pt/rally-pt/rallyptdata.csv"
    s=requests.get(url).content

    df_up=pd.read_csv(io.StringIO(s.decode('utf-8')))

    # Generate dataframe for table 

    df_table_up=df_up.filter(['name','stage','capacity'])

    df_table_up['opstatus'] = df_up['capacity'].apply(lambda x:
    '🔴' if x > 90 else (
    '🟠' if x > 70 else (
    '🟡' if x > 50 else (
    '🟢' if x > 9 else ''
    ))))

    df_table_up['id'] = df_table_up.index 


    newtable_up = dash_table.DataTable(
        
        data=df_table_up.to_dict('records'),
        columns=[
                {'name':'ZE', 'id':'name'},
                {'name':'Troço', 'id':'stage'},
                #{'name':'Lotação', 'id':'capacity','type':'numeric'},
                {'name':'Status', 'id':'opstatus'},

        ],
        fixed_rows={'headers': True},
        style_table={'height': 500},  

        style_cell_conditional=[
            {'if': {'column_id': 'name'},
             'width': '10%'},
             {'if': {'column_id': 'opstatus'},
             'width': '15%'},
            {'if': {'column_id': 'stage'},
             'width': '10%'},
        ],

        style_as_list_view=True,
         style_header={'backgroundColor': '#1f2b45', 'color' :'white'},
        style_cell={
            'backgroundColor': 'rgb(255,255,255)',
            'color': '#1f2b45',
            'fontSize':16, 'font-family':'Open Sans',
        },
        )

    return newtable_up

if _name_ == "_main_":
    app.run_server(host='0.0.0.0', debug=False)