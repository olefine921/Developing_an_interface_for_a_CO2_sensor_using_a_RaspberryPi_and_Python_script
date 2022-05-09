import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from time import time, ctime, sleep #import the time library
from datetime import datetime, date, timedelta

def import_data_from_csv(filename):
    data = pd.read_csv(filename, header = None, names = ['datetime','time','pCO2','temp','mbar','mlg'])
    print("imported data")
#    x = data.loc[:,'time']
#    y = data.loc[:,'temp']
    return data
adresseTime = datetime.now().strftime('%Y.%m.%d')
adresse = '/media/pi/boot/pCO2_Sensor_Data/CSV-Files/' + adresseTime +'.csv'
#fname = adresse

fname = 'D:\FS22\Paind\Dash\LongerTest_Start_20.04.2022_14.46.csv'

data = import_data_from_csv(fname)
x = data.loc[:,'time']
# y1 = data.loc[:,'temp']
# y2 = data.loc[:,'pCO2']

# fig = px.line(data, x="time", y="temp", )


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


app = Dash(__name__)

app.layout = html.Div(children =[
    dcc.Graph(
        id = 'example',
        figure = fig
        ),
    """
    dcc.Slider(
        data['time'].min(),
        data['time'].max(),
        step=None,
        value=data['time'].min(),
        marks={str(time): str(time) for time in data['time'].unique()},
        id='time-slider')
    """
    dcc.Interval(
        id='interval-component',
        interval=60*1000, # in milliseconds
        n_intervals=0
        )
    ])        
        
#trying to create a refreshing loop
  
@app.callback(
    Output('example', 'figure'),
    Input('interval-component', 'n_intervals'))
def update_figure(n):
    #fname = adresse

    fname = 'D:\FS22\Paind\Dash\LongerTest_Start_20.04.2022_14.46.csv'

    data = import_data_from_csv(fname)
    x = data.loc[:, 'time']

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Adding title text to the figure
    fig.update_layout(
        title_text='Average pCO2 and Temperature starting at ' + adresseTime,
        autosize=False,
        width=1900,
        height=800,
    )

    # Naming x-axis
    fig.update_xaxes(title_text="Time")

    # Naming y-axes
    fig.update_yaxes(title_text="Temp ", secondary_y=False)
    fig.update_yaxes(title_text="pCO2 ", secondary_y=True)

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
