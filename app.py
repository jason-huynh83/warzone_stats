import os
os.chdir('C:\\Users\\jason\\Documents\\code\\warzone')
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import time
from datatable import weekly_stats
from warzone import *


# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'top': 0,
    'padding': '20px 10px'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

controls = dbc.FormGroup(
    [
        html.H6("Please enter your gamertag"),
        dcc.Input(id='input-1-state', type='text', value='gamertag'),
        dcc.Input(id='input-2-state', type='text', value='platform'),
        html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
        
    ]
)
                
sidebar = html.Div(
    [
        html.H2('Players', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['Card Title 1'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_1', children=['Sample text.'], style=CARD_TEXT_STYLE),
      
                    ]
                )
            ]
        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_2', children=['Card Title 2'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_2', children=['Sample text.'], style=CARD_TEXT_STYLE),
                   
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_title_3', children=['Card Title 3'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_3', children=['Sample text.'], style=CARD_TEXT_STYLE),
                        
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_title_4', children=['Card Title 4'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_4', children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]
        ),
        md=3
    )
])

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_1'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_2'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_3'), md=4
        )
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_4'), md=12,
        )
    ]
)

content_fourth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_5'), md=6
        ),
        dbc.Col(
            dcc.Graph(id='graph_6'), md=6
        )
    ]
)

content_fifth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_7'), md=6
        ),
        dbc.Col(
            dcc.Graph(id='graph_8'), md=6
        )
    ]
)

content = html.Div(
    [
        html.H2('Warzone Analytics and Stats', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        content_second_row,
        content_third_row,
        content_fourth_row,
        content_fifth_row
    ],
    style=CONTENT_STYLE
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])

def avg_dmg(df):
    count = 0
    data = []
    for i in range(len(df)):
        showlegend = True
        if count >= 1:
            showlegend = False
            data.append(go.Bar(x=df['df{}'.format(i)]['username'], 
                                 y=np.array(df['df{}'.format(i)]['damageDone'].mean()), 
                                 name='Average Damage Done',
                                 marker_color='lightslategrey',showlegend=showlegend))
            data.append(go.Bar(x=df['df{}'.format(i)]['username'], 
                                 y=np.array(df['df{}'.format(i)]['damageTaken'].mean()), 
                                 marker_color='crimson', 
                                 name='Average Damage Taken',showlegend=showlegend))

        else:
            data.append(go.Bar(x=df['df{}'.format(i)]['username'], 
                                 y=np.array(df['df{}'.format(i)]['damageDone'].mean()), 
                                 name='Average Damage Done',
                                 marker_color='lightslategrey',showlegend=showlegend))
            data.append(go.Bar(x=df['df{}'.format(i)]['username'], 
                                 y=np.array(df['df{}'.format(i)]['damageTaken'].mean()), 
                                 marker_color='crimson', 
                                 name='Average Damage Taken',showlegend=showlegend))
        count += 1

    layout = go.Layout(barmode='stack',title='Avg Damage Done vs. Avg Damage Taken')
    dmg = go.Figure(data=data, layout=layout)
    return dmg

def dmg_done(df):
    colours = ['lightsteelblue','lightgray','lightslategrey','steelblue','lightskyblue']
    data = []
    done = []
    taken = []
    for i in range(len(df)):
        data.append(go.Bar(x=xaxis, y=df['df{}'.format(i)]['damageDone'], 
                             name=df['df{}'.format(i)]['username'][0], 
                             marker_color=colours[i]))
        done.append(df['df{}'.format(i)]['damageDone'])
        taken.append(df['df{}'.format(i)]['damageTaken'])


    buttons = []

    buttons.append(dict(method='restyle',
                        label='Damage Done',
                        visible=True,
                        args=[{'y':done,
                               'x':[xaxis]}]))

    buttons.append(dict(method='restyle',
                        label='Damage Taken',
                        visible=True,
                        args=[{'y':taken,
                               'x':[xaxis]}]))


    updatemenu = []
    your_menu = {}
    updatemenu.append(your_menu)

    updatemenu[0]['buttons'] = buttons
    updatemenu[0]['direction'] = 'down'
    updatemenu[0]['showactive'] = True

    # add dropdown menus to the figure
    layout = go.Layout(title='Damage Done Vs. Damage Taken',barmode='stack',showlegend=True, updatemenus=updatemenu)
    dd_dt = go.Figure(data=data, layout=layout)
    return dd_dt

def avg_kills(df):
    count = 0
    data = []
    for i in range(len(df)):
        showlegend=True
        if count >= 1:
            showlegend=False
            data.append(go.Bar(x=df['df{}'.format(i)]['username'], 
                                 y=np.array(df['df{}'.format(i)]['kills'].mean()), 
                                 name='Average Kills',
                                 marker_color='lightsteelblue',showlegend=showlegend))      
            data.append(go.Bar(x=df['df{}'.format(i)]['username'], 
                                 y=np.array(df['df{}'.format(i)]['deaths'].mean()), 
                                 marker_color='lightpink', 
                                 name='Average Deaths',showlegend=showlegend))
        else:
            data.append(go.Bar(x=df['df{}'.format(i)]['username'], 
                                 y=np.array(df['df{}'.format(i)]['kills'].mean()), 
                                 name='Average Kills',
                                 marker_color='lightsteelblue',showlegend=showlegend))   
            data.append(go.Bar(x=df['df{}'.format(i)]['username'], 
                                 y=np.array(df['df{}'.format(i)]['deaths'].mean()), 
                                 marker_color='lightpink', 
                                 name='Average Deaths',showlegend=showlegend))
        count +=1

    layout = go.Layout(barmode='stack',title='Avg Kills vs. Avg Deaths')
    avg_kd = go.Figure(data=data, layout=layout)
    return avg_kd

def kdm(df):
    data = []
    data.append(go.Bar(x=xaxis, y=df['df0']['kills'], name='Kills',marker_color='lightsteelblue'))
    data.append(go.Bar(x=xaxis, y=df['df0']['deaths'], name='Deaths',marker_color='lightpink'))


    buttons = []

    for i in range(len(df)):
        buttons.append(dict(method='restyle',
                            label=df['df{}'.format(i)]['username'][0],
                            visible=True,
                            args=[{'y':[df['df{}'.format(i)]['kills'],
                                        df['df{}'.format(i)]['deaths']],
                                   'x':[xaxis]}]))


    updatemenu = []
    your_menu = {}
    updatemenu.append(your_menu)

    updatemenu[0]['buttons'] = buttons
    updatemenu[0]['direction'] = 'down'
    updatemenu[0]['showactive'] = True

    # add dropdown menus to the figure
    layout = go.Layout(title='Kills Vs. Deaths By Match',barmode='stack',
                       showlegend=True, updatemenus=updatemenu)
    kdm = go.Figure(data=data,layout=layout)
    return kdm

def kdfm(df):
    colours = ['lightsteelblue','lightgray','lightslategrey','steelblue','lightskyblue']
    data = []
    kills = []
    deaths = []
    for i in range(len(df)):
        data.append(go.Bar(x=xaxis, y=df['df{}'.format(i)]['kills'], 
                             name=df['df{}'.format(i)]['username'][0],marker_color=colours[i]))
        kills.append(df['df{}'.format(i)]['kills'])
        deaths.append(df['df{}'.format(i)]['deaths'])


    buttons = []
    stats = [kills, deaths]
    count = 0
    for i in stats:
        if count >=1:
            buttons.append(dict(method='restyle',
                                label='Deaths',
                                visible=True,
                                args=[{'y':i,
                                       'x':[xaxis]}]))
        else:
            buttons.append(dict(method='restyle',
                                label='Kills',
                                visible=True,
                                args=[{'y':i,
                                       'x':[xaxis]}]))
        count += 1

    updatemenu = []
    your_menu = {}
    updatemenu.append(your_menu)

    updatemenu[0]['buttons'] = buttons
    updatemenu[0]['direction'] = 'down'
    updatemenu[0]['showactive'] = True

    # add dropdown menus to the figure
    layout = go.Layout(title='Kills Vs. Deaths Vs. Friends By Match ',barmode='stack',showlegend=True, updatemenus=updatemenu)
    kdfm = go.Figure(data=data, layout=layout)
    return kdfm

def gulag(df):
    data = []
    count = 0 
    for i in range(len(df)):
        showlegend=True
        if count >=1:
            showlegend = False
            data.append(go.Bar(x=df['df{}'.format(i)]['username'],
                                 y=np.array(df['df{}'.format(i)][df['df{}'.format(i)]['deaths'] > 0]['gulagKills'].value_counts()[1]),
                                 name='Gulag Win',marker_color='slategray',showlegend=showlegend))
            data.append(go.Bar(x=df['df{}'.format(i)]['username'],
                                 y=np.array(df['df{}'.format(i)][df['df{}'.format(i)]['deaths'] > 0]['gulagKills'].value_counts()[0]),
                                 name='Gulag Loss',marker_color='plum',showlegend=showlegend,
                                 text='Gulag Win%:{}'.format(round(df['df{}'.format(i)][df['df{}'.format(i)]['deaths'] > 0]['gulagKills'].value_counts()[1]/len(df['df{}'.format(i)][df['df{}'.format(i)]['deaths'] > 0]['gulagKills']),2)), 
                                 textposition='outside'))

        else:
            data.append(go.Bar(x=df['df{}'.format(i)]['username'],
                                 y=np.array(df['df{}'.format(i)][df['df{}'.format(i)]['deaths'] > 0]['gulagKills'].value_counts()[1]),
                                 name='Gulag Win',marker_color='slategray',showlegend=showlegend))
            data.append(go.Bar(x=df['df{}'.format(i)]['username'],
                                 y=np.array(df['df{}'.format(i)][df['df{}'.format(i)]['deaths'] > 0]['gulagKills'].value_counts()[0]),
                                 name='Gulag Loss',marker_color='plum',showlegend=showlegend,
                                 text='Gulag Win%:{}'.format(round(df['df{}'.format(i)][df['df{}'.format(i)]['deaths'] > 0]['gulagKills'].value_counts()[1]/len(df['df{}'.format(i)][df['df{}'.format(i)]['deaths'] > 0]['gulagKills']),2)), 
                                 textposition='outside'))

        count += 1

    layout = go.Layout(barmode='stack',showlegend=True, title='Gulag Wins Vs. Losses')
    gulag = go.Figure(data=data, layout=layout)
    return gulag

def all_xp(df):
    colours = ['lightsteelblue','lightgray','lightslategrey','steelblue','lightskyblue']
    xp = []
    for i in range(len(df)):
        xp.append(pd.pivot_table(df['df{}'.format(i)],values=['totalXp','medalXp','matchXp',
                                                                   'scoreXp','challengeXp','bonusXp',
                                                                   'miscXp'],columns='username').transpose().reset_index())
    all_xp = pd.concat(xp)
    
    matchXp = go.Bar(x=all_xp['username'],y=all_xp['matchXp'],name='Match XP',visible=False,
                     marker_color=colours)
    medalXp = go.Bar(x=all_xp['username'],y=all_xp['medalXp'],name='Medal XP',visible=False,
                    marker_color=colours)
    miscXp = go.Bar(x=all_xp['username'],y=all_xp['miscXp'],name='Misc XP',visible=False,
                   marker_color=colours)
    scoreXp = go.Bar(x=all_xp['username'],y=all_xp['scoreXp'],name='Score XP',visible=False,
                     marker_color=colours)
    totalXp = go.Bar(x=all_xp['username'],y=all_xp['totalXp'],name='Total XP',visible=True,
                     marker_color=colours)
    
    
    data = [totalXp, medalXp, matchXp, scoreXp]
        
    updatemenus = list([
        dict(active=0,
             showactive = True,
             buttons=list([   
                dict(label = "totalXp",
                     method = "update",
                     args = [{"visible": [True,False,False,False]}]), # hide trace2
                dict(label = "medalXp",
                     method = "update",
                     args = [{"visible": [False,True,False,False]}]),
                dict(label = "matchXp",
                     method = "update",
                     args = [{"visible": [False,False,True,False]}]),
                dict(label = "scoreXp",
                     method = "update",
                     args = [{"visible": [False,False,False,True]}]),
                ]))])
    
    layout = go.Layout(title='Amount of XP',updatemenus=updatemenus,showlegend=False)
    avg_xp = go.Figure(data=data,layout=layout)
    return avg_xp

def circle_kills(df):
    circle = []
    for i in range(len(df)):
        circle.append(pd.pivot_table(df['df{}'.format(i)],values=[col for col in df['df{}'.format(i)] if col.startswith('objectiveBrDownEnemy')],
                       index='username',aggfunc='mean').reset_index())
    circles = pd.concat(circle)
    circle_dict = {}
    for i in range(len(circles.columns[1:])):
        circle_dict['{}'.format(i)] = go.Bar(x=circles['username'],y=circles['objectiveBrDownEnemyCircle{}'.format(i+1)],name='circle{}'.format(i+1),visible=True,
                     marker_color=colours)
        
    circle_graphs = []
    for i in range(len(circle_dict)):
        circle_graphs.append(circle_dict['{}'.format(i)])
        
    updatemenus = list([
        dict(active=0,
             showactive = True,
             buttons=list([   
                dict(label = "circle 1",
                     method = "update",
                     args = [{"visible": [True,False,False,False,False,False]}]), # hide trace2
                dict(label = "circle 2",
                     method = "update",
                     args = [{"visible": [False,True,False,False,False,False]}]),
                dict(label = "circle 3",
                     method = "update",
                     args = [{"visible": [False,False,True,False,False,False]}]),
                dict(label = "circle 4",
                     method = "update",
                     args = [{"visible": [False,False,False,True,False,False]}]),
                dict(label = "circle 5",
                     method = "update",
                     args = [{"visible": [False,False,False,False,True,False]}]),
                dict(label = "circle 6",
                     method = "update",
                     args = [{"visible": [False,False,False,False,False,True]}]),
                 
                ]))])
    
    layout = go.Layout(title='Circle Kills',updatemenus=updatemenus,showlegend=False)
    circle_g = go.Figure(data=circle_graphs,layout=layout)
    return circle_g
    
def squad(username, platform):
    df = {}
    for i in range(len(username)):
        time.sleep(1)
        df['df{}'.format(i)] = get_stats(username[i], platform[i])
    
    return df

def team_avg(username,platform):
    df = {}
    for i in range(len(username)):
        time.sleep(1)
        df['df{}'.format(i)] = weekly_stats(username[i], platform[i])
    
    text1 = df['df0'].columns[0]
    text2 = df['df0'].columns[1]
    text3 = df['df0'].columns[2]
    text4 = df['df0'].columns[3]
    
    matches = int(df['df0'][df['df0'].columns[0]])
    for i in range(len(df)):
        matches += int(df['df{}'.format(i)][df['df{}'.format(i)].columns[0]])
    avg_matches = matches / len(df)
    
    dmgDone = int(df['df0'][df['df0'].columns[1]])
    for i in range(len(df)):
        dmgDone += int(df['df{}'.format(i)][df['df{}'.format(i)].columns[1]])
    avg_dmgDone = dmgDone / len(df)
    
    dmgTaken = int(df['df0'][df['df0'].columns[2]])
    for i in range(len(df)):
        dmgTaken += int(df['df{}'.format(i)][df['df{}'.format(i)].columns[2]])
    avg_dmgTaken = dmgTaken / len(df)
    
    kd = int(df['df0'][df['df0'].columns[3]])
    for i in range(len(df)):
        kd += int(df['df{}'.format(i)][df['df{}'.format(i)].columns[3]])
    avg_kd = round(kd / len(df),2)
    return (text1, text2, text3, text4,
            avg_matches, avg_dmgDone, avg_dmgTaken, avg_kd)
    
@app.callback([
     
     Output('card_title_1', 'children'),
     Output('card_text_1', 'children'),
     
     Output('card_title_2', 'children'),
     Output('card_text_2', 'children'),
     
     Output('card_title_3', 'children'),
     Output('card_text_3', 'children'),
     
     Output('card_title_4', 'children'),
     Output('card_text_4', 'children'),
          
     Output('graph_1','figure'),
     Output('graph_2','figure'),
     Output('graph_3','figure'),
     Output('graph_4','figure'),
     Output('graph_5','figure'),
     Output('graph_6','figure'),
     Output('graph_7','figure'),
     Output('graph_8','figure'),
     
    ],
    [Input('submit-button-state', 'n_clicks')],
    [State('input-1-state', 'value'),
     State('input-2-state', 'value'),
     ])
def update_card_title_1(n_clicks, input1, input2):
    
    username = input1.split(', ')
    platform = input2.split(', ')

    text1, text2, text3, text4, card1, card2, card3, card4 = team_avg(username,platform)
    
    dff = squad(username,platform)
    
    a = avg_dmg(dff)
    b = avg_kills(dff)
    c = gulag(dff)
    d = kdm(dff)
    e = kdfm(dff)
    f = dmg_done(dff)
    g = all_xp(dff)
    h = circle_kills(dff)
        
    return (text1,round(card1,2),
            text2,round(card2,2),
            text3,round(card3,2),
            text4,card4,
            a,b,c,d,e,f,g,h)


if __name__ == '__main__':
    app.run_server(port='8085')
