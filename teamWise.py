import pandas as pd
import numpy as np
import plotly.express as px
import  plotly.graph_objects as go



def getTeamList(df_match):
    lis1 = df_match.team1.unique().tolist()
    lis1 = sorted(lis1);
    return lis1;
def tables( teamName , df , df_match):
    df_team_bat = df[df['batting_team'] == teamName]
    df_team_ball = df[df['bowling_team'] == teamName]
    indiscore = df_team_bat.groupby(['id', 'batsman', 'season'])['batsman_runs'].sum().sort_values(
        ascending=False).reset_index().head(20)
    season_batsman = df_team_bat.groupby(["season", "batsman"])["batsman_runs"].sum().sort_values(
        ascending=False).reset_index().head(20)
    new = df_match.iloc[:, [0, 2]]
    indiscore = indiscore.merge(new, on='id').drop(columns='id').rename(columns={'batsman_runs': 'High Score'})
    wickets = df_team_ball[df_team_ball['is_wicket'] == 1]
    wickets = wickets[wickets['dismissal_kind'] != 'run out']
    indi_bowler = wickets.groupby('bowler')['is_wicket'].sum().sort_values(ascending=False).reset_index().head(20)
    indi_perMatch = wickets.groupby(['id', 'bowler'])['is_wicket'].sum().sort_values(
        ascending=False).reset_index().head(20)
    dt = df_match.iloc[:, [0, 2]]
    indi_per_match = indi_perMatch.merge(dt, on='id')
    season_wicket = wickets.groupby(['season', 'bowler'])['is_wicket'].sum().sort_values(
        ascending=False).reset_index().drop_duplicates(subset='season', keep='first').sort_values(
        by='season').reset_index(drop=True)
    dot_ball = df_team_ball[df_team_ball['total_runs'] == 0]
    new = dot_ball.groupby(['season', 'bowler'], as_index=False)['total_runs'].value_counts().sort_values(by='count',
                                                                                                          ascending=False).drop(
        columns='total_runs')
    best_bowlers = season_wicket.merge(new, on=['season', 'bowler'])
    best_bowlers.rename(columns={'is_wicket': 'Total Wicket', 'count': 'Total Dot Ball'}, inplace=True)

    return [indiscore , season_batsman , indi_bowler , indi_per_match , best_bowlers]



def plots(teamName , df , df_match):
    df_team_bat = df[df['batting_team'] == teamName]
    df_team_ball = df[df['bowling_team'] == teamName]
    team_score = df_team_bat.groupby(["id"])['total_runs'].sum().reset_index()
    new = df_match.iloc[:, [0, 2]]
    team_score = team_score.merge(new, on='id')
    fig1 = px.line(team_score, x=team_score.index, y='total_runs', title=f'Match Count vs Total Score of {teamName}',
                  labels={
                      'index': 'match count', 'total_runs': 'total score'}, hover_data=['date'])

    team_win = df_match[df_match['winner'] == teamName]
    season_wins = team_win['season'].value_counts().reset_index()
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

    trophy_wins = team_win[team_win['date'].isin(finals)]
    new_y = season_wins[season_wins['index'].isin(trophy_wins['season'])].sort_values(by='index')['season'] + 1
    fig2 = go.Figure([
        go.Bar(name='Season Wins', x=season_wins['index'], y=season_wins['season']),
        go.Scatter(x=trophy_wins['season'].sort_values(), y=new_y, mode='markers', name='Trophy', hoverinfo='name')
    ])
    return fig1 , fig2


# def bal():
#     cc = px.bar()



