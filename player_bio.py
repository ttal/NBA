# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 22:27:52 2016

@author: eyal
"""
import requests
import pandas as pd
#%%
url = 'http://stats.nba.com/stats/leaguedashplayerbiostats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='
u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
response = requests.get(url,headers={"USER-AGENT":u_a})
data = response.json()
player_bio = pd.DataFrame(data['resultSets'][0]['rowSet'],columns=data['resultSets'][0]['headers'])
#%%
height = df.sort_values('PLAYER_HEIGHT_INCHES')
weight = df.sort_values('PLAYER_WEIGHT')
# idx = height['PLAYER_ID']==201566