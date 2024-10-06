import requests
import json
import ast
import pandas as pd
from geopy.distance import distance
from datetime import date, datetime, timedelta, time
from record_processor import records_processor

teams=['ARZ', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GBP', 'HOU', 'IND', 'JAX', 'KCC', 'LAC', 'LAR', 'LVR', 'MIA', 'MIN', 'NYG', 'NYJ', 'NEP', 'NOS', 'PHL', 'PIT', 'SFF', 'SEA', 'TBB', 'TEN', 'WSH']

with open('numgames.txt') as f:
    numgames = f.read()
numgames = ast.literal_eval(numgames)

def intl(stadium):
    if stadium in ["Wembley Stadium", "Twickenham Stadium", "Tottenham Stadium"]:
        long=-0.454295
        lat=51.470020
    if stadium == "Azteca Stadium":
        long=-99.0785
        lat=19.4207
    if stadium == "Allianz Arena":
        long=11.78610
        lat=48.35380
    if stadium == "Deutsche Bank Park":
        long=8.570556
        lat=50.033333
    return lat, long

def dist(long1,long2,lat1,lat2):
    loc1=tuple([lat1,long1])
    loc2=tuple([lat2,long2])
    print(loc2)
    miles=distance(loc1,loc2).miles
    return miles

locations = pd.read_csv("team_cities.csv")

intl_locations=["Wembley Stadium", "Twickenham Stadium", "Tottenham Stadium", "Azteca Stadium", "Allianz Arena"]
# frankfurt locations not listed in data, need exception for 2023-11-05 MIAvKCC and 2023-11-12 INDvNEP

season = pd.DataFrame(columns=["season","date","home-team","home-lat", "home-long", "vis-team", "vis-lat", "vis-long","intl-flag","intl-lat","intl-long","win-team","lose-team"])

for i in range(1996,2024):
    start_date=str(i)+"-04-01"
    start_date=datetime.strptime(start_date,"%Y-%m-%d")
    season_end=start_date+pd.DateOffset(days=365)
    day1=start_date
    day1=day1.date()
    day2=day1+pd.DateOffset(days=30)
    day2=day2.date()
    intl_flag=0
    while day2 <= season_end:
            temp=pd.DataFrame(columns=["season","date","home-team","home-lat", "home-long", "vis-team", "vis-lat", "vis-long","intl-flag","intl-lat","intl-long","win-team","lose-team"])
            url = "https://api3.natst.at/"+"KEY HERE"+"/games/PFB/"+str(day1)+","+str(day2)
            data = requests.get(url).json()
            try:
                for j in data["games"]:
                        seasonyear=i
                        try:
                            gamedate=data["games"][j]["gameday"]
                        except:
                            gamedate="null"
                        try:
                            winteam=data["games"][j]["winner-code"]
                        except:
                             winteam="null"
                        try:
                            loseteam=data["games"][j]["loser-code"]
                        except:
                            loseteam="null"
                        try:
                            hometeam=data["games"][j]["home-code"]
                        except:
                            hometeam="null"
                        try:
                            game_lat=locations[(locations['Year']==i) & (locations['Team']==hometeam)]["Lat"].values.tolist()[0]
                            game_long=locations[(locations['Year']==i) & (locations['Team']==hometeam)]["Long"].values.tolist()[0]
                        except:
                            long="null"
                            lat="null"
                        try:
                            visteam=data["games"][j]["visitor-code"]
                        except:
                            visteam="null"
                        try:
                            vis_lat=locations[(locations['Year']==i) & (locations['Team']==visteam)]["Lat"].values.tolist()[0]
                            vis_long=locations[(locations['Year']==i) & (locations['Team']==visteam)]["Long"].values.tolist()[0]
                            stadium=data["games"][j]["venue"]
                            print("here7")
                            if stadium in intl_locations:
                                lat,long = intl(stadium)
                                intl_lat=lat
                                intl_long=long
                                intl_flag=1
                            else:
                                intl_lat=None
                                intl_long=None

                        except:
                            long="null"
                            lat="null"
                        temp.loc[len(temp)] = [seasonyear,gamedate,hometeam,game_lat,game_long,visteam,vis_lat,vis_long,intl_flag,intl_lat,intl_long,winteam,loseteam]
                        if intl_flag==1:
                            temp2=pd.DataFrame(columns=["season","date","home-team","home-lat", "home-long", "vis-team", "vis-lat", "vis-long","intl-flag","intl-lat","intl-long","win-team","lose-team"])
                            temp2.loc[0] = temp.loc[len(temp)-1].values.tolist()
                            temp=temp.append(temp2)
                            temp.loc[len(temp)-2,"intl-flag"]="X"
                            intl_flag=0
            except:
                next
                # if day1 >= date(i, 8, 1):
                #     with open('output'+'_'+str(day1)+'_'+str(day2)+'.txt', 'w') as file:
                #         json.dump(data, file, indent=4)

                # else:
                #     next
            season=season.append(temp,ignore_index=True)
            print(season)
            day1=day2+timedelta(days=1)
            day2=day1+timedelta(days=30)

season.reset_index

for i in range(0,len(season)):
    if season.loc[i,"intl-flag"]==1:
        season.loc[i, "travel team"] = season.iloc[i,5]
        season.loc[i, "distance (miles)"]=dist(season.iloc[i,10],season.iloc[i,7],season.iloc[i,9],season.iloc[i,6])
    
    elif season.loc[i,"intl-flag"]=="X":
        season.loc[i, "travel team"] = season.iloc[i,2]
        season.loc[i, "distance (miles)"]=dist(season.iloc[i,10],season.iloc[i,4],season.iloc[i,9],season.iloc[i,3])
    
    else:
        season.loc[i, "travel team"] = season.iloc[i,5]
        season.loc[i, "distance (miles)"]=dist(season.iloc[i,4],season.iloc[i,7],season.iloc[i,3],season.iloc[i,6])

season.sort_values(by="date",inplace=True)
records=pd.read_csv("team_perf_ot.csv")
merged_table=pd.merge(season,records,left_on=["season","travel team"],right_on=["year","team"])
merged_table.to_csv("distance2.csv")
distance_table=pd.DataFrame(columns=["season","team","total-distance"])

row=0
for year in range(1996,2024):
    for team in teams:
        traveled=sum(merged_table[(merged_table["season"]==year) & (merged_table["travel team"]==team)]["distance (miles)"].unique())
        distance_table.loc[row,"season"]=year
        distance_table.loc[row,"team"]=team
        distance_table.loc[row,"total-distance"]=traveled
        row+=1

distance_table.to_csv("distance_table2.csv")
playoffs=pd.read_csv("team_perf.csv")
final_table=pd.merge(distance_table,playoffs,left_on=["season","team"],right_on=["year","team"])
final_table.to_csv("final_dist_table2.csv")



