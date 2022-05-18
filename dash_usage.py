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

#define function that reads csv file created by measurement.py & defines columm names
#important: if order of columns changes, this has to be updated in dash_usage.py & measurement.py
def import_data_from_csv(filename):
    data = pd.read_csv(filename, header = None, names = ['datetime','time','pCO2','temp','mbar','mlg'])
    print("imported data") #print to show it worked

    return data

#define adresse of csv by measurement.py
#by now code doesn't update adresse after 4 days, code has to be stopped & restarted at the same day as the new 4 days measurement starts
adresseTime = datetime.now().strftime('%Y.%m.%d')
adresse = '/media/pi/boot/pCO2_Sensor_Data/CSV-Files/' + adresseTime +'.csv'

#if time window was missed for restarting this code, the following line can be made uncommented and filled with the name (incl path) of the active csv file
#adresse = '/media/pi/boot/pCO2_Sensor_Data/CSV-Files/2022.05.09.csv'

#create informations for 1st graph
fname = adresse

#open & read csv file into variable
data = import_data_from_csv(fname)
#define content of x axis
x = data.loc[:,'datetime']

#define figure that has 2 y axis
fig = make_subplots(specs=[[{"secondary_y": True}]])
 
#Use add_trace function to specify secondary_y axes.
fig.add_trace(
    go.Scatter(x=x, y=data.loc[:,'temp'], name="Temp"),
    secondary_y=False)
 
# Use add_trace function and specify secondary_y axes = True.
fig.add_trace(
    go.Scatter(x=x, y=data.loc[:,'pCO2'], name="pCO2"),
    secondary_y=True,)

#define app
app = dash.Dash(__name__)

#specify layout, Intervall has to be introduced seperately to Graph
app.layout = html.Div(
    children = [
        dcc.Interval(
        id='interval-component',
        interval=60*1000, # in milliseconds = 60sec
        n_intervals=0
        ),
    html.Div([
        dcc.Graph(
            id = 'example',
            figure = fig)

        ])
        ]
    )
        
#create a refreshing loop  
@app.callback(
    Output('example', 'figure'),
    Input('interval-component', 'n_intervals'))

#define function to update graph for every interval
def update_figure(n):
    
    #create informations for every new graph
    fname = adresse
    data = import_data_from_csv(fname)
    x = data.loc[:, 'datetime']
    
    #define figure that has 2 y axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    #Adding title text to the figure, define size of graph and fonts
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
    fig.update_yaxes(title_text="Temp ", secondary_y=False) #Temp = blue line
    fig.update_yaxes(title_text="pCO2 ", secondary_y=True) #pCO2 = red line
    #place legend
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    #plot a scatter chart by specifying the x and y values
    #Use add_trace function to specify secondary_y axes.
    fig.add_trace(
        go.Scatter(x=x, y=data.loc[:, 'temp'], name="Temp"),
        secondary_y=False)

    #Use add_trace function and specify secondary_y axes = True.
    fig.add_trace(
        go.Scatter(x=x, y=data.loc[:, 'pCO2'], name="pCO2"),
        secondary_y=True, )


    return fig #after function is done, app shows updated figure

if __name__ == '__main__':
    app.run_server(debug=True) #run app, debug mode has to be activated to let callbacks work
