import requests
import json
import ast
import pandas as pd
from datetime import date, datetime, timedelta, time

teams=['ARZ', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GBP', 'HOU', 'IND', 'JAX', 'KCC', 'LAC', 'LAR', 'LVR', 'MIA', 'MIN', 'NYG', 'NYJ', 'NEP', 'NOS', 'PHL', 'PIT', 'SFF', 'SEA', 'TBB', 'TEN', 'WSH']

season = pd.read_csv("results.csv")

