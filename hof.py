import pandas as pd
import numpy as np
import bs4
import requests


# df= pd.read_csv('Datasets/AllMatch.csv')
# df_match=pd.read_csv("Datasets/matches.csv")

def hofhead(df , df_match):
    win = df_match.winner.value_counts().reset_index()
    allteam = df.groupby('batting_team').sum().reset_index()
    allteam = allteam.iloc[:, [0, -3, -1]]
    allteam = allteam.rename(columns={"batting_team": "index", "is_wicket": "Total wicket", "total_runs": "Total Runs"})
    allteam = allteam.merge(win, on='index')
    new = df.groupby('batting_team', as_index=False)
    new = new['batsman_runs'].value_counts()
    r4 = new[new['batsman_runs'] == 4]
    r6 = new[new['batsman_runs'] == 6]
    r4 = r4.drop(columns='batsman_runs')
    r6 = r6.drop(columns='batsman_runs')
    r4 = r4.rename(columns={"batting_team": 'index', "count": '4s'})
    r6 = r6.rename(columns={"batting_team": 'index', "count": '6s'})
    allteam = allteam.merge(r4, on='index')
    allteam = allteam.merge(r6, on='index')
    finals = [
        "2008-06-01",
        "2009-05-24",
        "2010-04-25",
        "2011-05-28",
        "2012-05-27",
        "2013-05-26",
        "2014-06-01",
        "2015-05-24",
        "2016-05-29",
        "2017-05-21",
        "2018-05-27",
        "2019-05-12",
        "2020-11-10"]
    champ = df_match[df_match['date'].isin(finals)].winner.value_counts().reset_index()
    champ = champ.rename(columns={"winner": "Trophy"})
    allteam = allteam.merge(champ, on='index', how='outer')
    allteam.Trophy = allteam.Trophy.fillna(0)
    allteam.Trophy = allteam.Trophy.astype(int)
    allteam = allteam.sort_values(by=['Trophy', 'winner', 'Total Runs'], ascending=False)
    allteam = allteam.rename(columns={"index": "Team"}).reset_index(drop=True)
    return allteam;

def upgradge_df(df , df_match):
    clm = (df_match['date'][:].str[:4])
    clm = clm.astype(int)
    df_match['season'] = clm
    season = df_match[['id', 'season']]
    df = df.merge(season, on='id')
    return df;

def caps(df):
    new = df.groupby(['season', 'batsman']).sum('batsman_runs').sort_values(ascending=False, by='batsman_runs')
    orcap = new['batsman_runs'].reset_index().drop_duplicates(subset='season', keep='first')
    orcap = orcap.sort_values('season')
    new = df[df.is_wicket == 1]
    new = new[new.dismissal_kind != 'run out']
    purplecap = new.groupby(['season', 'bowler'])['is_wicket'].sum().sort_values(
        ascending=False).reset_index().drop_duplicates(subset='season', keep='first')
    purplecap = purplecap.sort_values(by='season')
    caps = orcap.merge(purplecap, on='season')
    caps = caps.rename(columns={"batsman" : "Orange Cap Holder" , "bowler" : "Purple Cap Holder" , "batsman_runs": 'Total Runs', "is_wicket": 'Total Wickets'})
    # print(caps);
    return caps;


if __name__ == '__main__':
    # hofhead()
    # print(pd.__version__)
    # caps()
    pass
