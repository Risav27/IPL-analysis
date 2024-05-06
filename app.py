import streamlit as st
import pandas as pd
import plotly.express as px
import hof,overal , teamWise , playerwise
df= pd.read_csv('Datasets/AllMatch.csv')
df_match=pd.read_csv("Datasets/matches.csv")
df1 = hof.hofhead(df , df_match);
df = hof.upgradge_df(df,df_match);
df2 = hof.caps(df);
st.title("Welcome to IPL Analysis [2008-2020]")
st.header("")
menu = st.sidebar.radio(
    'Select option',
    ('Hall of Fame' , 'Overall Analysis' , 'Team-wise Analysis' , 'Player-wise Analysis')
)

if menu == 'Hall of Fame':
    # st.sidebar.header('Hall of Fame')
    st.header("Hall of Fame")
    st.table(df1)
    st.header("Caps Analysis")
    st.table(df2)

if menu == 'Overall Analysis':
    ls= overal.vals(df , df_match)
    st.title("All in Oneshot")
    col1 , col2 , col3  = st.columns(3);
    with(col1):
        st.header("Seasons")
        st.title(ls[0])
    with(col2):
        st.header("City")
        st.title(ls[1])
    with(col3):
        st.header("venue")
        st.title(ls[2])
    col1 , col2 , col3  = st.columns(3);
    with(col1):
        st.header("Team")
        st.title(ls[3])
    with(col2):
        st.header("Player")
        st.title(ls[5])
    with(col3):
        st.header("Umpire")
        st.title(ls[4])
    col1 , col2 , col3  = st.columns(3);
    with(col1):
        st.header("4s")
        st.title(ls[6])
    with(col2):
        st.header("6s")
        st.title(ls[7])
    with(col3):
        st.header("wickets")
        st.title(ls[8])

    sea , lis = overal.yearVsPlayer(df);

    fig = px.line(x=sea, y=lis, title='player count on every year')
    st.plotly_chart(fig);
    r4 = overal.yearVs46w(df)

    fig = px.line(r4, x='season', y=['4s', '6s', 'Wickets'], title='4s , 6s and wickets in every year')
    st.plotly_chart(fig)

    st.title("Most Successful segment : ")
    player , batsman , bowler = overal.topPlayer(df)
    spot = st.selectbox("select a Option : " , ["Overall" , "Batsman" , "Bowler"])
    if(spot == "Overall"):
        st.table(player)
    elif(spot == "Batsman"):
        st.table(batsman)
    else:
        st.table(bowler);



if menu == 'Team-wise Analysis':
    temList = teamWise.getTeamList(df_match)
    teamName = st.sidebar.selectbox('Select Team :' , temList);
    fig1 , fig2 = teamWise.plots(teamName, df , df_match);
    st.header('Team Performance : ')
    st.plotly_chart(fig2)
    st.header('Match vs Score')
    st.plotly_chart(fig1)
    lis = teamWise.tables(teamName , df , df_match)
    st.header('Batsman with Highest Individual Score : ')
    st.table(lis[0])
    st.header('Bowler with Highest Individual Wicket : ')
    st.table(lis[3])
    st.header('Most Successful Seasonal Batsman : ')
    st.table(lis[1])
    st.header('Most Successful Bowler with total wicket !');
    st.table(lis[2])
    st.header('Season Wise Highest Wicket Taker : ')
    st.table(lis[4])

    ## player wise analysis
if menu == 'Player-wise Analysis':
    playerList = playerwise.plyr(df)
    plyr = st.sidebar.selectbox('Player Name : ' , playerList);
    st.header(f"Player : {plyr}")
    st.header("Hall of Fame : ")
