import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pymongo import MongoClient
import numpy as np
import time

mongo = {
    'uri': 'mongodb://localhost:27017/',
    'db': 'motors',
    'collect': 'project'
}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Monitor de MOTORES", style={'textAlign': 'center', 'height': '4vh'}),
    
    html.Div([
        html.Label("Dispositivo:"),
        dcc.Dropdown(
            id='device-dropdown',
            options=[
                {'label': 'Motor', 'value': '0'},
                {'label': 'Servomotor', 'value': '1'}
            ],
            value='1',
            clearable=False
        ),
        ], style={'width': '200px', 'margin': '0 auto', 'height': '5vh'}),
    
    dcc.Graph(id='position-error-graph', style={'height': '50vh', 'width': '100%'}),
    
    dcc.Graph(id='action-value-graph', style={'height': '100%', 'width': '100%'}),
    
    dcc.Interval(
        id='interval-component',
        interval=250,
        n_intervals=0
    )
])

@app.callback(
    [Output('position-error-graph', 'figure'),
     Output('action-value-graph', 'figure')],
    [Input('interval-component', 'n_intervals'),
     Input('device-dropdown', 'value')]
)
def update_graphs_live(n, ID):
    cursor = collection.find(
        {"ID": ID}
    ).sort("timestamp", -1).limit(100)
    
    df = pd.DataFrame(list(cursor))
    
    if df.empty:
        fig_empty = px.line()
        fig_empty.update_layout(title="Esperando datos...")
        return fig_empty, fig_empty 

    df = df.sort_values(by='timestamp', ascending=True)
    df['time'] = pd.to_datetime(df['timestamp'], unit='s')
    df['current_pos_rev'] = df['POS']
    df['pos_des_rev'] = df['REF']
    df['error_rev'] = df['ERR']
    df['action_value'] = df['OUT'].apply(lambda x: x.get('VAL'))
    
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(x=df['time'], y=df['current_pos_rev'],
                              mode='lines', name='Posición Actual (rev)', yaxis='y1'))
    
    fig1.add_trace(go.Scatter(x=df['time'], y=df['pos_des_rev'],
                              mode='lines', name='Posición Deseada (rev)', yaxis='y1', line={'dash': 'dash'}))
                              
    fig1.add_trace(go.Scatter(x=df['time'], y=df['error_rev'],
                              mode='lines', name='Error (rev)', yaxis='y1', line={'color': 'red'}))
                              
    fig1.update_layout(
        title=f"Posición y Error",
        xaxis_title="Tiempo",
        yaxis=dict(title="Posición (rev)", side='left', showgrid=True),
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255, 0.7)'),
        margin=dict(l=40, r=40, t=40, b=40),
    )

    fig2 = px.line(df, x='time', y='action_value', 
                   title=f"Salida")
    
    action_type = df['OUT'].iloc[-1]['TYPE'] if not df.empty else "N/A"
    fig2.update_layout(
        xaxis_title="Tiempo",
        yaxis_title=f"{action_type}",
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255, 0.7)'),
        margin=dict(l=40, r=40, t=40, b=40),
    )
    
    return fig1, fig2

if __name__ == '__main__':
    try:
        client = MongoClient(mongo['uri'])
        db = client[mongo['db']]
        collection = db[mongo['collect']]
        print(f' * MONGODB OK')
    except Exception as e:
        print(f' * MONGODB FAIL')
    app.run(debug=True)
