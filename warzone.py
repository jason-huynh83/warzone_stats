# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 20:01:51 2021

@author: Jason
"""
import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import time
import warnings
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
warnings.filterwarnings("ignore")
import os
os.chdir('C:\\Users\\jason\\Documents\\code\\warzone')

global xaxis,colors
xaxis = ['Match 1','Match 2','Match 3','Match 4','Match 5','Match 6','Match 7','Match 8','Match 9',
          'Match 10','Match 11','Match 12','Match 13','Match 14','Match 15','Match 16','Match 17','Match 18','Match 19','Match 20']
colours = ['lightsteelblue','lightgray','lightslategrey','steelblue','lightskyblue']

def weekly_stats(username,platform):
    try:
        url = "https://call-of-duty-modern-warfare.p.rapidapi.com/weekly-stats/"+username+"/"+platform
        
        headers = {
            'x-rapidapi-key': "e5ebce8953mshb052759675fa2b3p15385ajsnc449b9ed0f9b",
            'x-rapidapi-host': "call-of-duty-modern-warfare.p.rapidapi.com"
            }
     
        response = requests.request("GET", url, headers=headers)
        
        response_text = response.text
        
        stats_dict = json.loads(response_text)
    
        df_wz = stats_dict['wz']
        df_all = df_wz['all']
        df_summary = df_all['properties']
        
        df = pd.DataFrame(list(df_summary.items()),columns=['stats','value'])
        df = df.set_index('stats').transpose()
        df = df[['matchesPlayed','damageDone','damageTaken','kdRatio','kills','deaths','scorePerMinute','killsPerGame','headshots','assists','headshotPercentage','gulagKills','gulagDeaths']]

        return df
    except:
        print(stats_dict)
        return stats_dict

def get_stats(username,platform):
    try:
        url = "https://call-of-duty-modern-warfare.p.rapidapi.com/warzone-matches/"+username+"/"+platform
        headers = {
            'x-rapidapi-key': "e5ebce8953mshb052759675fa2b3p15385ajsnc449b9ed0f9b",
            'x-rapidapi-host': "call-of-duty-modern-warfare.p.rapidapi.com"
            }
        
        response = requests.request("GET", url, headers=headers)
        
        response_text = response.text
        
        stats_dict = json.loads(response_text)
        
        df_matches = pd.DataFrame(stats_dict['matches'])
        df_summary = pd.DataFrame(stats_dict['summary'])
        df_summary = df_summary.transpose()
        
        
        df_playerStats = pd.json_normalize(df_matches['playerStats'])
        df_player = pd.json_normalize(df_matches['player'])
        
        df_concat = pd.concat([df_playerStats, df_player], axis=1)
        
        
        df_main = pd.concat([df_matches, df_concat], axis = 1)
        df_main.drop(['playerStats','player'], axis = 1, inplace=True)

    
        return df_main
    except:
        print(stats_dict)


def squad(team,platform):
    '''
    squad = []
    platform = []
    team = []
    print('How many are in your squad?')
    num_squad = int(input())
    
    print('Please Enter gamertag followed by platform of each member')
    for i in range(num_squad):
        squad.append(input())
        
    for j in squad:
        team.append(j.split(', ')[0])
        platform.append(j.split(', ')[1])
    '''
    
    #team = ['iBHuynhing','SonImYourDaddy','Frayhnn','Grey%231858','accoy%231972']
    #platform = ['psn','psn','psn','battle','battle']
    
    df = {}
    for i in range(len(team)):
        time.sleep(1)
        df['df{}'.format(i)] = get_stats(team[i], platform[i])
        
    
    timeMoving = []
    arr = ['Match 1','Match 2','Match 3','Match 4','Match 5','Match 6','Match 7','Match 8','Match 9','Match 10',
       'Match 11','Match 12','Match 13','Match 14','Match 15','Match 16','Match 17','Match 18','Match 19','Match 20']
    for i in range(len(df)):
        timeMoving.append(round(df['df{}'.format(i)]['percentTimeMoving'].mean(),2))
    
    
    
    return df

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
                                 textposition='inside'))

        else:
            data.append(go.Bar(x=df['df{}'.format(i)]['username'],
                                 y=np.array(df['df{}'.format(i)][df['df{}'.format(i)]['deaths'] > 0]['gulagKills'].value_counts()[1]),
                                 name='Gulag Win',marker_color='slategray',showlegend=showlegend))
            data.append(go.Bar(x=df['df{}'.format(i)]['username'],
                                 y=np.array(df['df{}'.format(i)][df['df{}'.format(i)]['deaths'] > 0]['gulagKills'].value_counts()[0]),
                                 name='Gulag Loss',marker_color='plum',showlegend=showlegend,
                                 text='Gulag Win%:{}'.format(round(df['df{}'.format(i)][df['df{}'.format(i)]['deaths'] > 0]['gulagKills'].value_counts()[1]/len(df['df{}'.format(i)][df['df{}'.format(i)]['deaths'] > 0]['gulagKills']),2)), 
                                 textposition='inside'))

        count += 1

    layout = go.Layout(barmode='stack',showlegend=True, title='Gulag Wins Vs. Losses')
    gulag = go.Figure(data=data, layout=layout)
    return gulag

def avg_circle_kills(df):
    circle = []
    for i in range(len(df)):
        circle.append(pd.pivot_table(df['df{}'.format(i)],values=[col for col in df['df{}'.format(i)] if col.startswith('objectiveBrDownEnemy')],
                       index='username',aggfunc='mean').reset_index())
    circles = pd.concat(circle)
    
    circle1 = go.Bar(x=circles['username'],y=circles['objectiveBrDownEnemyCircle1'],name='circle1',visible=True,
                     marker_color=colours)
    circle2 = go.Bar(x=circles['username'],y=circles['objectiveBrDownEnemyCircle2'],name='circle2',visible=False,
                    marker_color=colours)
    circle3 = go.Bar(x=circles['username'],y=circles['objectiveBrDownEnemyCircle3'],name='circle3',visible=False,
                   marker_color=colours)
    circle4 = go.Bar(x=circles['username'],y=circles['objectiveBrDownEnemyCircle4'],name='circle4',visible=False,
                     marker_color=colours)
    circle5 = go.Bar(x=circles['username'],y=circles['objectiveBrDownEnemyCircle5'],name='circle5',visible=False,
                     marker_color=colours)
    circle6 = go.Bar(x=circles['username'],y=circles['objectiveBrDownEnemyCircle6'],name='circle6',visible=False,
                     marker_color=colours)
    
    
    data = [circle1, circle2, circle3, circle4, circle5, circle6]
        
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
    circle_g = go.Figure(data=data,layout=layout)
    return circle_g

def total_xp(df):
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

