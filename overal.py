import pandas as pd
import numpy as np


def vals(df , df_match):
    city = df_match.city.unique().shape[0]
    venue = df_match.venue.unique().shape[0]
    total_teams = df_match.team1.unique().shape[0]
    sea = df['season'].unique().shape[0]
    ump = np.append(df_match.umpire1.unique(),
                    df_match.umpire2.unique())
    ump = np.unique(ump).shape[0]
    player = np.append(df.batsman.unique(),
                       df.bowler.unique())
    player = np.unique(player).shape[0]
    wik = df[df['is_wicket'] == 1].shape[0]
    r4 = df[df['batsman_runs'] == 4].shape[0]
    r6 = df[df['batsman_runs'] == 6].shape[0]

    return [sea , city , venue , total_teams , ump , player , r4 , r6 , wik]

def yearVsPlayer(df):
    sea = df['season'].unique()
    lis = [];
    for i in sea:
        player = np.append(df[df['season'] == i]['batsman'].unique(),
                           df[df['season'] == i]['bowler'].unique())
        lis.append(np.unique(player).shape[0])
    lis = np.array(lis)

    return sea , lis

def yearVs46w(df):
    new = df.groupby('season', as_index=False)['batsman_runs'].value_counts()
    r4 = new[new['batsman_runs'] == 4]
    r6 = new[new['batsman_runs'] == 6]
    r4 = r4.merge(r6, on='season')
    new = df.groupby('season', as_index=False)['is_wicket'].value_counts()
    wik = new[new['is_wicket'] == 1]
    r4 = r4.merge(wik, on='season')
    r4 = r4.drop(columns=['batsman_runs_x', 'batsman_runs_y', 'is_wicket'])
    r4 = r4.rename(columns={'count_x': '4s', 'count_y': '6s', 'count': 'Wickets'})
    return r4;

def topPlayer(df):
    new = df.groupby(['batsman'], as_index=False).sum().sort_values(by='batsman_runs', ascending=False)
    batsman = new.iloc[:, [0, 5]].reset_index(drop=True)
    batsman = batsman.head(20)
    new = df[df.is_wicket == 1]
    new = new[new.dismissal_kind != 'run out']
    new = new.groupby('bowler', as_index=False).sum().sort_values(by='is_wicket', ascending=False)
    bowler = new.iloc[:, [0, -2]].reset_index(drop=True)
    bowler = bowler.head(20)
    bowler.rename(columns={"is_wicket": 'Total Wicket'}, inplace=True)
    batsman.rename(columns={"batsman_runs": 'Total Runs'}, inplace=True)
    player = batsman.join(bowler)
    return (player , batsman , bowler)
