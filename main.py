from datetime import time
from turtle import width
import dash
from dash.dcc.Graph import Graph
from dash.dcc.RadioItems import RadioItems
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import math

# import plotly.express as px
import pandas as pd
# import plotly.graph_objects as go

start=datetime.now()
df  = pd.read_csv("data.csv")


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash()


timeFrame = 300
df = df[df["Time"] < timeFrame]
parts = ["Left Hand", "Right Hand", "Left Leg", "Right Leg", "Body"]
joints = ["Hip","Right Thigh", "Right Knee", "Right Ankle", "Left Thigh", "Left Knee", "Left Ankle", "Waist", "Neck", "Head 1",
            "Head 0", "Left Shoulder", "Left Elbow", "Left Palm", "Right Shoulder", "Right Elbow", "Right Palm"]
jointsByParts = [
            ["Neck", "Left Shoulder", "Left Elbow", "Left Palm"],
            ["Neck", "Right Shoulder", "Right Elbow", "Right Palm" ],
            ["Hip", "Left Thigh", "Left Knee", "Left Ankle"],
            ["Hip", "Right Thigh", "Right Knee", "Right Ankle"],
            ["Hip", "Waist", "Neck", "Head 1", "Head 0"]
            ]


frames = {}
#jointsData = {k:{} for k in joints}
jointsData = {}

for joint in joints:
    jointsData[joint] = {"X" : {}, "Y": {}, "Z": {}, "E": {}}
    jointsData[joint]["X"] = list(df[df["Joint"] == joint]["X"]*0.5)
    jointsData[joint]["Y"] = list(df[df["Joint"] == joint]["Y"]*0.5)
    jointsData[joint]["Z"] = list(df[df["Joint"] == joint]["Z"]*0.5)


for joint in joints:
    jointsData[joint]["E"] = []
    for i in range(timeFrame):   
        x = jointsData[joint]["X"][i]
        y = jointsData[joint]["Y"][i]
        z = jointsData[joint]["Z"][i]
        jointsData[joint]["E"].append(math.sqrt(x**2 + y**2 + z**2))


index = 0
for i in range(timeFrame):
    frames[i] = []
    index = 0
    for part in parts:
        frames[i].append({
            "type" : "scatter",
            "x" : list(df[((df["Parts"] == part) & (df["Time"] == i))]["X"]*0.5),
            "y" : list(df[((df["Parts"] == part) & (df["Time"] == i))]["Z"]*0.5),
            "name" : part,
            "meta" : jointsByParts[index],
            "hovertemplate" : "%{meta} <br> (%{x}, %{y})"
        })
        index += 1


        

        
    
"""
        frames["Joint"][i]["X"] = list(df[((df["Parts"] == part) & (df["Time"] == i))]["X"]*0.5)
        frames["Joint"][i]["Y"] = list(df[((df["Parts"] == part) & (df["Time"] == i))]["Z"]*0.5)
        frames["Joint"][i]["name"] = df.loc[i, 'Joint']

    [go.Scatter(
                        x=df[((df["Parts"] == part) & (df["Time"] == i))]["X"]*0.5, 
                        y =df[((df["Parts"] == part) & (df["Time"] == i))]["Z"]*0.5,
                        mode='markers',
                        name=part
                    ) for part in parts]
    
    frames["Skeleton"][i] = [go.Scatter(
                        x=df[((df["Parts"] == part) & (df["Time"] == i))]["X"]*0.5, 
                        y =df[((df["Parts"] == part) & (df["Time"] == i))]["Z"]*0.5,
                        mode='markers + lines',
                        name=part
                    ) for part in parts]
"""
"""
layout={"humanModel" : go.Layout(
            xaxis = dict(range=[-1,1],nticks=4,showticklabels=False,autorange=False),
            yaxis = dict(range=[0,1],nticks=4,showticklabels=False,autorange=False),),
        "graph" : go.Layout(
            xaxis = dict(range=[0,timeFrame],autorange=False),
            yaxis = dict(autorange=False)

        )    
        }
"""
humanModelLayout = go.Layout(
    autosize=False,
            xaxis = dict(range=[-1,1],nticks=4,showticklabels=False,autorange=False),
            yaxis = dict(range=[0,1],nticks=4,showticklabels=False,autorange=False),
            width = 1000,
            height = 100
            )
print(humanModelLayout)
graphLayout = go.Layout(
    autosize=False,
            xaxis = dict(range=[0,timeFrame],autorange=False),
            yaxis = dict(autorange=False),
            width = 1000,
            height = 100)

def get_JointOption():
    dict_list = []
    for joint in joints:
        dict_list.append({'label': joint, 'value': joint})
    return dict_list

#print(frames["Joint"][0])
#fig = go.Figure(data=frames[0], layout=humanModelLayout)
#print(fig)
#print(fig)
print (datetime.now()-start)
app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(
        id = 'humanModel',
        figure = go.Figure(
            data = frames[0],
            layout = humanModelLayout
                
            )

    ),

    dcc.Store(
        id = 'timeFrame',
        data = timeFrame

    ),

    dcc.Store(
        id = 'framesData',
        data = frames

    ),

    dcc.Store(
        id = 'humanModelLayoutData',
        data = humanModelLayout
    ),

    dcc.Store(
        id = 'graphLayoutData',
        data = graphLayout
    ),

    dcc.Store(
        id = 'jointsData',
        data = jointsData
    ),


    html.Button(
        "Play",
        id = "playButton",
        n_clicks = 0
    ),

    html.Button(
        "Pause",
        id = "pauseButton",
        n_clicks = 0
    ),

    dcc.Slider(
        id = "animeSlider",
        min = 0,
        max = timeFrame - 1,
        value = 0
    ),

    dcc.Dropdown(
            id = 'jointSelector',
            options = get_JointOption(),
            value=None,
            multi=True
            
            ),

    

    dcc.Interval(
        id = "interval",
        n_intervals = 0,
        interval= 10,
        disabled = True
    
    ),

    dcc.Graph(
        id = "xGraph",
        figure = go.Figure(
            data = {
                "x": [0],
                "y" : [jointsData[joints[0]]["X"][0]],
                "type" : "scatter"

            },
             layout = humanModelLayout
            
        )
    ),

    dcc.Graph(
        id = "yGraph",
        figure = go.Figure(
            data = {
                "x": [0],
                "y" : [jointsData[joints[0]]["Y"][0]],
                "type" : "scatter"

            },
            layout = graphLayout
            
        )
    ),

    dcc.Graph(
        id = "zGraph",
        figure = go.Figure(
            data = {
                "x": [0],
                "y" : [jointsData[joints[0]]["Z"][0]],
                "type" : "scatter"

            },
            layout = graphLayout
        )
    ),

    dcc.Graph(
        id = "eGraph",
        figure = go.Figure(
            data = {
                "x": [0],
                "y" : [jointsData[joints[0]]["E"][0]],
                "type" : "scatter"

            },
            layout = graphLayout
            
        )
    ),

    


])
"""
dcc.RadioItems(
        id = 'modeSelector',
        options=[
            {'label' : 'Joint', 'value' : 'Joint'},
            {'label' : 'Skeleton', 'value' : 'Skeleton'},
        ],
        value = 'Joint',
        labelStyle={'display': 'inline-block'} 
    ),
"""

@app.callback(
    Output("interval", "disabled"),
    Input("playButton","n_clicks"),
    Input("pauseButton", "n_clicks")
)
def playORpause(play, pause):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if ("playButton") in changed_id:
        return False
    if ("pauseButton") in changed_id:
        return True
"""
@app.callback(
    Output("animeSlider", "value"),
    Input("interval", "n_intervals"),
    State("animeSlider", "value")
)
def doAnimate(i, frame):
    if frame < (timeFrame-1): 
        frame += 1
    else:
        frame = 0
    return frame
"""

app.clientside_callback(
    """
    //function (frame, data, humanLayout, graphLayout, timeFrame, jointsData){
    function (frame, data, timeFrame, jointsData, joints){
        graphDataX = [];
        graphDataY = [];
        graphDataZ = [];
        graphDataE = [];
        if (joints != null){
            for (var i = 0; i < joints.length; i++){
                graphDataX.push({'y': jointsData[joints[i]]["X"].slice(0, frame+1),'type':'scatter', 'name': joints[i]});
                graphDataY.push({'y': jointsData[joints[i]]["Y"].slice(0, frame+1),'type':'scatter', 'name': joints[i]});
                graphDataZ.push({'y': jointsData[joints[i]]["Z"].slice(0, frame+1),'type':'scatter', 'name': joints[i]});
                graphDataE.push({'y': jointsData[joints[i]]["E"].slice(0, frame+1),'type':'scatter', 'name': joints[i]});

            }
        }
        humanModelLayout = {
            'xaxis': {'autorange': false, 'range': [-1, 1], 'showticklabels': false},
            'yaxis': {'autorange': false, 'range': [0, 1], 'showticklabels': false}
        }
        if (frame < timeFrame){

            return [{'data':data[frame], 'layout': humanModelLayout},
            {'data': graphDataX},
            {'data': graphDataY},
            {'data': graphDataZ},
            {'data': graphDataE}];
        }
       
    }
    """

    ,

        Output('humanModel', 'figure'),
        Output('xGraph', 'figure'),
        Output('yGraph', 'figure'),
        Output('zGraph', 'figure'),
        Output('eGraph', 'figure'),
        # Output("animeSlider", "value"),
        # Input('interval', 'n_intervals'),
        Input('animeSlider', 'value'),
        State('framesData', 'data'),
        #State('humanModelLayoutData','data'),
        # State('graphLayoutData','data'),
        State('timeFrame','data'),
        State('jointsData', 'data'),
        State('jointSelector', 'value')
    )




app.clientside_callback(
    """
    function (i, frame, maxFrame){
        if (frame < maxFrame - 1){
            frame += 1;
        }else frame = 0
        return frame
    }
    """,
    Output("animeSlider", "value"),
    Input("interval", "n_intervals"),
    State("animeSlider", "value"),
    State("timeFrame", "data")
)


if __name__ == '__main__': 
    app.run_server()