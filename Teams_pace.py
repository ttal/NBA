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
    
def leaguedashplayerstats(college='',conference='',country='',datefrom='',dateto='',division='',
                          draftpick='',draftyear='',gamescope='',gamesegment='',height='',
                          lastngames=0,leagueid='00',location='',measuretype='Base',month=0,
                          opponentteamid=0,outcome='',poround=0,paceadjust='N',permode='Totals',
                          period=0,playerexperience='',playerposition='',plusminus='N',rank='N',
                          season='2016-17',seasonsegment='',seasontype='Regular Season',shotclockrange='',
                          starterbench='',teamid=0,vsconference='',vsdivision='',weight=''):
    url = 'http://stats.nba.com/stats/leaguedashplayerstats?'
    api_param = {
        'College' : college,
        'Conference' : conference,
        'Country' : country,
        'DateFrom' : datefrom,
        'DateTo' : dateto,
        'Division' : division,
        'DraftPick' : draftpick,
        'DraftYear' : draftyear,
        'GameScope' : gamescope,
        'GameSegment' : gamesegment,
        'Height' : height,
        'LastNGames' : lastngames,
        'LeagueID' : leagueid,
        'Location' : location,
        'MeasureType' : measuretype,
        'Month' : month,
        'OpponentTeamID' : opponentteamid,
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
        'VsConference' : vsconference,
        'VsDivision' : vsdivision,
        'Weight' : weight,
        }
    u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
    response = requests.get(url,params=api_param,headers={"USER-AGENT":u_a})
    data = response.json()
    return pd.DataFrame(data['resultSets'][0]['rowSet'],columns=data['resultSets'][0]['headers'])
#%%   
df = leaguegamelog(season='2015-16')
teams = leaguedashteamstats(permode='Totals',season = '2015-16')
players = leaguedashplayerstats(season = '2015-16')
teams_id = teams['TEAM_ID'].unique()
Pace = []
for team_id in teams_id:
    game_id = df.GAME_ID[df['TEAM_ID']==team_id]
    team1 = df[df.GAME_ID.isin(game_id)]
    Tm = team1[team1['TEAM_ID']==team_id]
    Opp = team1[team1['TEAM_ID']!=team_id]
    Poss = 0.5 * ((1.0*np.sum(Tm['FGA'])+0.4*np.sum(Tm['FTA'])-1.07*(1.0*np.sum(Tm['OREB'])/(1.0*np.sum(Tm['OREB']) + 1.0*np.sum(Opp['DREB']))) * (1.0*np.sum(Tm['FGA']) - 1.0*np.sum(Tm['FGM'])) + 1.0*np.sum(Tm['TOV'])) + (1.0*np.sum(Opp['FGA'])+ 0.4*np.sum(Opp['FTA']) - 1.07*(1.0*np.sum(Opp['OREB'])/(1.0*np.sum(Opp['OREB']) + 1.0*np.sum(Tm['DREB'])))*(1.0*np.sum(Opp['FGA']) - 1.0*np.sum(Opp['FGM'])) + 1.0*np.sum(Opp['TOV'])))
    Pace.append(48.0*Poss/((np.sum(Tm['MIN'])/5.0)))
teams['PACE'] = Pace
teams['pace_adjustment'] = np.mean(teams['PACE'])/teams['PACE']
lg_AST = 1.0*np.sum(df['AST'])
lg_FG = 1.0*np.sum(df['FGM'])
lg_FT = 1.0*np.sum(df['FTM'])
lg_PTS = 1.0*np.sum(df['PTS'])
lg_FGA = 1.0*np.sum(df['FGA'])
lg_ORB = 1.0*np.sum(df['OREB'])
lg_TOV = 1.0*np.sum(df['TOV'])
lg_FTA = 1.0*np.sum(df['FTA'])
lg_TRB = 1.0*np.sum(df['REB'])
lg_PF = 1.0*np.sum(df['PF'])
factor = (2.0/3) - (0.5*(lg_AST/lg_FG))/(2.0*(lg_FG/lg_FT))
VOP    = lg_PTS/(lg_FGA - lg_ORB + lg_TOV + 0.44*lg_FTA)
DRBP   = (lg_TRB - lg_ORB)/lg_TRB
aPER = []
for i in range(players.shape[0]):
    player = players.iloc[i]
    team = teams[teams['TEAM_ID'] == player['TEAM_ID']]
    MP = 1.0*np.sum(player['MIN'])
    FG3M = 1.0*np.sum(player['FG3M'])
    AST = 1.0*np.sum(player['AST'])
    FG = 1.0*np.sum(player['FGM'])
    FT = 1.0*np.sum(player['FTM'])
    FGA = 1.0*np.sum(player['FGA'])
    FTA = 1.0*np.sum(player['FTA'])
    TRB = 1.0*np.sum(player['REB'])
    ORB = 1.0*np.sum(player['OREB'])
    STL = 1.0*np.sum(player['STL'])
    BLK = 1.0*np.sum(player['BLK'])
    TOV = 1.0*np.sum(player['TOV'])
    PF = 1.0*np.sum(player['PF'])
    team_AST = 1.0*np.sum(team['AST'])
    team_FG = 1.0*np.sum(team['FGM'])
    uPER = (1.0 / MP) *(FG3M + 
         (2.0/3) * AST + 
         (2.0 - factor * (team_AST / team_FG)) * FG + 
         (FT *0.5 * (1.0 + (1.0 - (team_AST / team_FG)) + (2.0/3) * (team_AST / team_FG))) -
         VOP * TOV - 
         VOP * DRBP * (FGA - FG) - 
         VOP * 0.44 * (0.44 + (0.56 * DRBP)) * (FTA - FT) + 
         VOP * (1 - DRBP) * (TRB - ORB) + 
         VOP * DRBP * ORB + 
         VOP * STL + 
         VOP * DRBP * BLK -
         PF * ((lg_FT / lg_PF) - 0.44 * (lg_FTA / lg_PF) * VOP))
    aPER.append(uPER*team.pace_adjustment.values[0])
MIN = players['MIN']
lg_aPER = np.sum(MIN*aPER)/np.sum(MIN)
PER = np.array(aPER)*15.0/lg_aPER # add pace_adjustment
players['PER'] = PER