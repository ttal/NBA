# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 23:15:40 2016

@author: eyal
"""
import requests
import pandas as pd
import numpy as np
#%%
def leaguedashteamstats(conference='',datefrom='',dateto='',div='',gamescope='',gamesegment='',lastngames=0,
              leagueid='00',location='',measuretype='Base',month=0,oppenentteamid=0,outcome='',
              poround=0,paceadjust='N',permode='PerGame',period=0,playerexperience='',
              playerposition='',plusminus='N',rank='N',
              season='2015-16',seasonsegment='',seasontype='Regular Season',shotclockrange='',
              starterbench='',teamid=0,vsconference='',vsdivision=''):
    url = 'http://stats.nba.com/stats/leaguedashteamstats?'
    api_param = {
        'Conference' :conference,
        'DateFrom' :  datefrom,
        'DateTo' : dateto,
        'Division' : div,
        'GameScope' : gamescope,
        'GameSegment' : gamesegment,
        'LastNGames' : lastngames,
        'LeagueID' : leagueid,
        'Location' : location,
        'MeasureType' : measuretype,
        'Month' : month,
        'OpponentTeamID' : oppenentteamid,
        'Outcome' : outcome,
        'PORound' : poround,
        'PaceAdjust' : paceadjust,
        'PerMode' : permode,
        'Period' : period,
        'PlayerExperience' : playerexperience,
        'PlayerPosition' : playerposition,
        'PlusMinus' : plusminus,
        'Rank' : rank,
        'Season' : season,
        'SeasonSegment' : seasonsegment,
        'SeasonType' : seasontype,
        'ShotClockRange' : shotclockrange,
        'StarterBench' : starterbench,
        'TeamID' : teamid,
        'VsConference': vsconference,
        'VsDivision' : vsdivision              
    }
    u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
    response = requests.get(url,params=api_param,headers={"USER-AGENT":u_a})
    data = response.json()
    return pd.DataFrame(data['resultSets'][0]['rowSet'],columns=data['resultSets'][0]['headers'])

def leaguegamelog(counter = 1000,datefrom='',dateto='',direction='DESC',leagueid='00',
                  playerorteam='T',season='2015-16',seasontype='Regular Season',sorter='PTS'):   
    url = 'http://stats.nba.com/stats/leaguegamelog?'
    api_param = {
        'Counter' : counter,
        'DateFrom' :  datefrom,
        'DateTo' : dateto,
        'Direction' : direction,
        'LeagueID' : leagueid,
        'PlayerOrTeam' : playerorteam,
        'Season' : season,
        'SeasonType' : seasontype,
        'Sorter' : sorter,              
    }
    u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
    response = requests.get(url,params=api_param,headers={"USER-AGENT":u_a})
    data = response.json()
    return pd.DataFrame(data['resultSets'][0]['rowSet'],columns=data['resultSets'][0]['headers'])
#%%   
df = leaguegamelog()
#df['HOME'] = ~df['MATCHUP'].str.contains("@")
#df = df.sort_values(['TEAM_ABBREVIATION'], ascending=[True])
teams_id = df['TEAM_ABBREVIATION'].unique()
df_pace = pd.DataFrame(columns=['TEAM_ABBREVIATION','PACE']) 
Pace = []
for team_id in teams_id:
    game_id = df.GAME_ID[df['TEAM_ABBREVIATION']==team_id]
    team1 = df[df.GAME_ID.isin(game_id)]
    Tm = team1[team1['TEAM_ABBREVIATION']==team_id]
    Opp = team1[team1['TEAM_ABBREVIATION']!=team_id]
    Poss = 0.5 * ((1.0*np.sum(Tm['FGA'])+0.4*np.sum(Tm['FTA'])-1.07*(1.0*np.sum(Tm['OREB'])/(1.0*np.sum(Tm['OREB']) + 1.0*np.sum(Opp['DREB']))) * (1.0*np.sum(Tm['FGA']) - 1.0*np.sum(Tm['FGM'])) + 1.0*np.sum(Tm['TOV'])) + (1.0*np.sum(Opp['FGA'])+ 0.4*np.sum(Opp['FTA']) - 1.07*(1.0*np.sum(Opp['OREB'])/(1.0*np.sum(Opp['OREB']) + 1.0*np.sum(Tm['DREB'])))*(1.0*np.sum(Opp['FGA']) - 1.0*np.sum(Opp['FGM'])) + 1.0*np.sum(Opp['TOV'])))
    Pace.append(48.0*Poss/((np.sum(Tm['MIN'])/5.0)))
df_pace['TEAM_ABBREVIATION'] = teams_id
df_pace['PACE'] = Pace