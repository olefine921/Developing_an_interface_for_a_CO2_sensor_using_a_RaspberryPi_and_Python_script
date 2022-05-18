import dash #import dash
from dash import dcc #import dash core components
from dash import html #import dash html components
import pandas as pd #import pandas for calculations, measurement.py uses numpy for calculation
import plotly.express as px #import plotly modules
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from time import time, ctime, sleep #import the time & datetime library
from datetime import datetime, date, timedelta
from dash.dependencies import Input, Output #import to enable callback


def import_data_from_csv(filename):
    data = pd.read_csv(filename, header = None, names = ['datetime','time','pCO2','temp','mbar','mlg'])
    print("imported data")

    return data

adresseTime = datetime.now().strftime('%Y.%m.%d')
adresse = '/media/pi/boot/pCO2_Sensor_Data/CSV-Files/' + adresseTime +'.csv'

#adressTime = '2022.05.09'
#adresse = '/media/pi/boot/pCO2_Sensor_Data/CSV-Files/2022.05.09.csv'

fname = adresse

data = import_data_from_csv(fname)
x = data.loc[:,'datetime']

fig = make_subplots(specs=[[{"secondary_y": True}]])
 
# plot a scatter chart by specifying the x and y values
# Use add_trace function to specify secondary_y axes.
fig.add_trace(
    go.Scatter(x=x, y=data.loc[:,'temp'], name="Temp"),
    secondary_y=False)
 
# Use add_trace function and specify secondary_y axes = True.
fig.add_trace(
    go.Scatter(x=x, y=data.loc[:,'pCO2'], name="pCO2"),
    secondary_y=True,)


app = dash.Dash(__name__)

app.layout = html.Div(
    children = [
        dcc.Interval(
        id='interval-component',
        interval=60*1000, # in milliseconds
        n_intervals=0
        ),
    html.Div([
        dcc.Graph(
            id = 'example',
            figure = fig)

        ])
        ]
    )
        
#trying to create a refreshing loop
  
@app.callback(
    Output('example', 'figure'),
    Input('interval-component', 'n_intervals'))
def update_figure(n):

    fname = adresse

    data = import_data_from_csv(fname)
    x = data.loc[:, 'datetime']

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Adding title text to the figure put adresseTime-Variable back in
    fig.update_layout(
        title_text='Average pCO2 and Temperature',
        font=dict(family='Arial',
                  size=16,
                  color='rgb(37,37,37)'),
        autosize=False,
        width=1900,
        height=800,
    )

    # Naming x-axis
    fig.update_xaxes(title_text="Time")

    # Naming y-axes
    fig.update_yaxes(title_text="Temp ", secondary_y=False)
    fig.update_yaxes(title_text="pCO2 ", secondary_y=True)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    # plot a scatter chart by specifying the x and y values
    # Use add_trace function to specify secondary_y axes.
    fig.add_trace(
        go.Scatter(x=x, y=data.loc[:, 'temp'], name="Temp"),
        secondary_y=False)

    # Use add_trace function and specify secondary_y axes = True.
    fig.add_trace(
        go.Scatter(x=x, y=data.loc[:, 'pCO2'], name="pCO2"),
        secondary_y=True, )


    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
