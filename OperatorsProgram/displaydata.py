#Program to display data to user within a dash app.
#Will produce internal version too

import csv
import numpy as py
import plotly.express as px
from datetime import date, time, datetime
from time import sleep
import pandas as pd

FILEPATH = 'PHNX_FM_PHNX_MOBC_Status_Beacon'
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
today_real = date.today()
today = '07-09-2022'
print(today, ' ', current_time)
all_yes = ['yes',  'Y', 'y', 'YES', 'Yes']
all_within = ['within', 'with in', 'Within', 'WITHIN', 'With In', ' WITH IN']
all_dash = ['dash', 'Dash', 'DASH']
sleep(0.5)

#def within():
    
display_q = input("Would you like to view the pass data? Y/N")
if display_q in all_yes:
    sleep(0.4)
    within_or_dash = input("Would you like to view the data within this program (input 'within') or via a dash app (input 'dash')?")
    if within_or_dash in all_within:
        datapds = pd.read_csv(f"{FILEPATH}-{today}.csv")
        print(datapds)
    if within_or_dash in all_dash:
        sleep(0.4)
        print("Please navigate to 'app.py's location in your computer's terminal and execute 'python app.py'")



    

