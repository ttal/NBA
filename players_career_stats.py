# -*- coding: utf-8 -*-
"""
Created on Fri Dec 02 16:04:24 2016

@author: eyal
"""
import requests
import pandas as pd
import numpy as np
#%%
def commonallplayers(currentseason=0,leagueid='00',season='2015-16'):
    url = 'http://stats.nba.com/stats/commonallplayers?'
    api_param = {
        'IsOnlyCurrentSeason' : currentseason,
        'LeagueID' : leagueid,
        'Season' : season,             
    }
    u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
    response = requests.get(url,params=api_param,headers={"USER-AGENT":u_a})
    data = response.json()
    return pd.DataFrame(data['resultSets'][0]['rowSet'],columns=data['resultSets'][0]['headers'])
    
def playercareerstats(playerid,permode='PerGame',leagueid='00'):
    url = 'http://stats.nba.com/stats/playercareerstats?'
    api_param = {
        'PerMode' : permode,
        'LeagueID' : leagueid,
        'PlayerID' : playerid,             
    }
    u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
    response = requests.get(url,params=api_param,headers={"USER-AGENT":u_a})
    data = response.json()
    return pd.DataFrame(data['resultSets'][0]['rowSet'],columns=data['resultSets'][0]['headers'])

def drafthistory(college='',leagueid='00',overallpick='',roundnum='',roundpick='',
                 season='',teamid=0,topx=''):
    url = 'http://stats.nba.com/stats/drafthistory?'
    api_param = {
        'College' : college,
        'LeagueID' : leagueid,
        'OverallPick' : overallpick,
        'RoundNum' : roundnum,
        'RoundPick' : roundpick,
        'Season' : season,
        'TeamID' : teamid,
        'TopX' : topx
    }
    u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
    response = requests.get(url,params=api_param,headers={"USER-AGENT":u_a})
    data = response.json()
    return pd.DataFrame(data['resultSets'][0]['rowSet'],columns=data['resultSets'][0]['headers'])
#%%
i=0
all_players = commonallplayers()
l = all_players.shape[0]
p = pd.DataFrame([])
for playerid in all_players['PERSON_ID']:
    p = p.append(playercareerstats(playerid))
    if i%100 == 0:
        print '%.2f' %(100*i/l)
    i = i+1
#all_players.rename(columns = {'PERSON_ID':'PLAYER_ID'}, inplace = True)
#all_players.rename(columns = {'DISPLAY_FIRST_LAST':'PLAYER_NAME'}, inplace = True)
#player_stats = pd.merge(p,all_players[['PLAYER_ID','PLAYER_NAME']],on='PLAYER_ID')
#cols = player_stats.columns.tolist()
#cols = [cols[0]]+ cols[-1:] + cols[1:-1]
#player_stats = player_stats[cols]
#%%
dh = drafthistory()
dh.rename(columns = {'PERSON_ID':'PLAYER_ID'}, inplace = True)
dh.rename(columns = {'TEAM_ID':'DRAFT_TEAM_ID'}, inplace = True)
dh.rename(columns = {'TEAM_ABBREVIATION':'DRAFT_TEAM_ABBREVIATION'}, inplace = True)
#%%
player_stats_dh = pd.merge(p,dh,on='PLAYER_ID')
cols = player_stats_dh.columns.tolist()
cols = [cols[27]]+ cols[:27] + cols[28:]
player_stats_dh = player_stats_dh[cols]
#%%
player_stats_dh.to_csv(r'C:\Users\eyal\Desktop\NBA\player_stats.csv')