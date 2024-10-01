import requests
import json
import ast
import pandas as pd
from datetime import date, datetime, timedelta, time

teams=['ARZ', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GBP', 'HOU', 'IND', 'JAX', 'KCC', 'LAC', 'LAR', 'LVR', 'MIA', 'MIN', 'NYG', 'NYJ', 'NEP', 'NOS', 'PHL', 'PIT', 'SFF', 'SEA', 'TBB', 'TEN', 'WSH']

with open('numgames.txt') as f:
    numgames = f.read()
numgames = ast.literal_eval(numgames)

# KEY: NatStat key

season=pd.DataFrame(columns=["date","home-team","vis-team","win-team","lose-team"])

for i in range(1966,2024):
    start_date=str(i)+"-04-01"
    start_date=datetime.strptime(start_date,"%Y-%m-%d")
    season_end=start_date+pd.DateOffset(days=365)
    day1=start_date
    day1=day1.date()
    day2=day1+pd.DateOffset(days=10)
    day2=day2.date()
    while day2 <= season_end:
            temp=pd.DataFrame(columns=["season","date","home-team","vis-team","win-team","lose-team"])
            url = "https://api3.natst.at/" + KEY + "/games/PFB/"+str(day1)+","+str(day2)
            data=requests.get(url).json()
            try:
                for j in data["games"]:
                        seasonyear=i
                        try:
                            gamedate=data["games"][j]["gameday"]
                        except:
                            gamedate="null"

                        try:
                            hometeam=data["games"][j]["home-code"]
                        except:
                            hometeam="null"
                        
                        try:
                            visteam=data["games"][j]["visitor-code"]
                        except:
                            visteam="null"

                        try:
                            winteam=data["games"][j]["winner-code"]
                        except:
                             winteam="null"
                        
                        try:
                            loseteam=data["games"][j]["loser-code"]
                        except:
                            loseteam="null"
                        
                        temp.loc[len(temp)] = [seasonyear,gamedate,hometeam,visteam,winteam,loseteam]
            except:
                next
            season=season.append(temp)
            day1=day2+timedelta(days=1)
            day2=day1+timedelta(days=30)

season['date']=pd.to_datetime(season['date'],format="%Y-%m-%d")
season.sort_values(by="date",ascending=True,inplace=True)
season.to_csv("results.csv")

season=pd.read_csv("results.csv")

team_perf=pd.DataFrame(columns=["year","team","w","l","playoffs"])

for year in range(1985,2024):
     for team in teams:
        team_w=0
        team_l=0
        for row in range(0,len(season)):
            if season.iloc[row].loc['season']==year and season.iloc[row].loc['win-team']==team:
                team_w+=1
            elif season.iloc[row].loc['season']==year and season.iloc[row].loc['lose-team']==team:
                team_l+=1
        if team_w+team_l > int(numgames[str(year)]):
             playoff="y"
        else:
             playoff="n"

        team_perf.loc[len(team_perf)] = [year,team,team_w,team_l,playoff]

team_perf.to_csv("team_perf.csv")


        
