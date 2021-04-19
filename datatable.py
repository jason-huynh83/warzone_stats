# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 13:24:12 2021

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


def weekly_stats(username,platform):
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

df = weekly_stats('iBHuynhing','psn')
