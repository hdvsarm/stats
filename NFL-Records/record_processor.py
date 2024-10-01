import requests
import json
import ast
import pandas as pd
from datetime import date, datetime, timedelta, time

teams=['ARZ', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GBP', 'HOU', 'IND', 'JAX', 'KCC', 'LAC', 'LAR', 'LVR', 'MIA', 'MIN', 'NYG', 'NYJ', 'NEP', 'NOS', 'PHL', 'PIT', 'SFF', 'SEA', 'TBB', 'TEN', 'WSH']
team_perf=pd.DataFrame(columns=["year","team","final_w","final_l","final_t","playoffs"])

team_perf_ot=pd.DataFrame(columns=["year","team","game","w","l","t","record_str"])

with open('numgames.txt') as f:
    numgames = f.read()
numgames = ast.literal_eval(numgames)

season = pd.read_csv("results.csv")

for year in range(1985,2024):
     for team in teams:
        game=0
        team_w=0
        team_l=0
        team_t=0
        for row in range(0,len(season)):
            if season.iloc[row].loc['season']==year and season.iloc[row].loc['win-team']==team:
                team_w+=1
                record_str="'"+str(team_w)+" - "+str(team_l)+" - "+str(team_t)
                if team_w+team_l+team_t <= int(numgames[str(year)]):
                    team_perf_ot.loc[len(team_perf_ot)] = [year,team,game,team_w,team_l,team_t,record_str]
                else:
                    None
                game+=1

            elif season.iloc[row].loc['season']==year and season.iloc[row].loc['lose-team']==team:
                team_l+=1
                record_str="'"+str(team_w)+" - "+str(team_l)+" - "+str(team_t)
                if team_w+team_l+team_t <= int(numgames[str(year)]):
                    team_perf_ot.loc[len(team_perf_ot)] = [year,team,game,team_w,team_l,team_t,record_str]
                else:
                    None
                game+=1

            elif season.iloc[row].loc['season']==year and (season.iloc[row].loc['home-team']==team or season.iloc[row].loc['vis-team']==team) and season.iloc[row].loc['win-team']=="BOTH":
                team_t+=1
                record_str="'"+str(team_w)+" - "+str(team_l)+" - "+str(team_t)
                if team_w+team_l+team_t <= int(numgames[str(year)]):
                    team_perf_ot.loc[len(team_perf_ot)] = [year,team,game,team_w,team_l,team_t,record_str]
                else:
                    None
                game+=1
                
            
        if team_w+team_l+team_t > int(numgames[str(year)]):
             playoff="y"
        else:
             playoff="n"

        team_perf.loc[len(team_perf)] = [year,team,team_w,team_l,team_t,playoff]

team_perf.to_csv("team_perf.csv")
team_perf_ot.to_csv("team_perf_ot.csv")

full_data = pd.merge(team_perf,team_perf_ot,on=["year","team"])
full_data.to_csv("full_data.csv")

records = full_data.record_str.unique()

records_data=pd.DataFrame(columns=["record","w","l","t","count","playoff_count","percent"])

for j in records:
    record_array=full_data[full_data["record_str"]==j]["record_str"].to_list()
    playoff_array=full_data[full_data["record_str"]==j]["playoffs"].to_list()
    wins=min(full_data[full_data["record_str"]==j]["w"].unique())
    losses=min(full_data[full_data["record_str"]==j]["l"].unique())
    ties=min(full_data[full_data["record_str"]==j]["t"].unique())
    record_occur=len(record_array)
    playoff_occur=playoff_array.count("y")
    percent = (playoff_occur/record_occur)*100
    records_data.loc[len(records_data)] = [j,wins,losses,ties,record_occur,playoff_occur,percent]

records_data.to_csv("records_data.csv")