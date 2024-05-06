import pandas as pd
import numpy as np
import plotly.express as px
import  plotly.graph_objects as go




def plyr(df):
    l1 = ['batsman', 'non_striker', 'bowler']
    player = pd.concat([df[i] for i in l1]).unique().tolist()
    return player;