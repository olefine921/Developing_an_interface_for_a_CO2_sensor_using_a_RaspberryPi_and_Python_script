import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def import_data_from_csv(filename):
    data = pd.read_csv(filename, header = None, names = ['datetime','time','pCO2','temp','mbar','mlg'])
    print("imported data")
#    x = data.loc[:,'time']
#    y = data.loc[:,'temp']
    return data
fname = '/media/pi/boot/pCO2_Sensor_Data/CSV-Files/2022.05.04.csv'

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

# fig.add_trace(
#     go.Scatter(x=x, y=data.loc[:,'mbar'], name="pCO2"),
#     secondary_y=True,)

# fig.add_trace(
#     go.Scatter(x=x, y=data.loc[:,'mlg'], name="pCO2"),
#     secondary_y=True,)
 
# Adding title text to the figure
fig.update_layout(
    title_text="Multiple Y Axis in Plotly"
)
 
# Naming x-axis
fig.update_xaxes(title_text="X - axis")
 
# Naming y-axes
fig.update_yaxes(title_text="<b>Main</b> Y - axis ", secondary_y=False)
fig.update_yaxes(title_text="<b>secondary</b> Y - axis ", secondary_y=True)



app = dash.Dash()

app.layout = html.Div(children =[
    dcc.Graph(
        id = 'example',
        figure = fig
        )
    ])        
        
#         {
#             'data' : [
#                 {'x':x,
#                  'y': data.loc[:,'temp'],
#                  'type':'line',
#                  'name':'Temperature (°C)'},
#                 {'x':x,
#                  'y': data.loc[:,'pCO2'],
#                  'type':'line',
#                  'name':'CO2 Concentration'}
#                 ],
#             'layout': {
#                 'title': 'Example'
#                 }
#             }


if __name__ == '__main__':
    app.run_server(debug = True)
            