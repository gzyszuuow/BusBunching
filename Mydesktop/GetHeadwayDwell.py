import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import random
import time
import math
import datetime as dt
import random
import copy
from datetime import datetime
from time import mktime
import os
import json
from functools import cmp_to_key
import imageio
from itertools import groupby

import numpy as np  # 数组相关的库
import matplotlib.pyplot as plt  # 绘图库

def GetdictKeyByValue(dic,value):
    Keys = []
    for key,value_ in dic.items():
        if value == value_:
            Keys.append(key)
    return Keys


#ROUTEID from right to left
ROUTEsID1 = ['400-39','400-40','400-57','400-58','400-59']
#ROUTEID from left to right 
ROUTEsID2 = ['400-41','400-42','400-60','400-61','400-62']
#ROUTEID delete
ROUTEsID3 = ['400-43','400-44','400-49','400-50','400-51','400-54','400-69']

busid = 400
path = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\"+str(busid)+".csv"
opaldata =  pd.read_csv(path)
#opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'OPRTR_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_TS_NM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_TS_NM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]
opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]

opaldata = opaldata[~opaldata["ROUTE_VAR_ID"].isin(ROUTEsID3)]
opaldata = opaldata[opaldata["RUN_DIR_CD"] == 1]

Stops_sequence = []

with open('C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\UsedStopsSequence_BusRout400.txt') as f:
    for line in f:
        odom = line.split()
        Stops_sequence.append(int(odom[0]))


#print(opaldata)

#All trajectoies  {Date1:{tripid:[{time:stop},{time:stop}...]},{tripid:[{time:stop},{time:stop}...]}, Date2:}
Trajectoies = {}
#arrival time to every stop in each trip  {Date1:{tripid:{stop:time,stop:time...}},{tripid:{stop:time,stop:time...}}, Date2:}
ArrivalTime = {}
#dwell time in every stop in each trip    {Date1:{tripid:{stop:dwell,stop:dwell...}},{tripid:{stop:dwell,stop:dwell...}}, Date2:} 
DwellTime = {}

num1 = 0
num2 = 0
grouped_byday = opaldata.groupby("JS_STRT_DT_FK")
for name_byday,group_byday in grouped_byday:
    #group_byday.sort_values(by=['TAG1_TM'],inplace=True)
    Trajectoies[name_byday] = {}

    grouped_bytrip = group_byday.groupby("TRIP_ID")
    
    for name_bytrip,group_bytrip in grouped_bytrip:

        #group_bytrip.sort_values(by=['TAG1_TM'],inplace=True)
        #group_bytrip.sort_values(by=['TAG2_TM'],inplace=True)

        busids = list(set(group_bytrip["BUS_ID"]))
        if len(busids)>1:
            num1+=1
        else:
            num2+=1

            Trajectoies[name_byday][name_bytrip] = []

            for index,row in group_bytrip.iterrows():
                dic1 = {row["TAG1_TM"]:row["TAG1_TS_NUM"]}
                dic2 = {row["TAG2_TM"]:row["TAG2_TS_NUM"]}
                Trajectoies[name_byday][name_bytrip].append(dic1)
                Trajectoies[name_byday][name_bytrip].append(dic2)





            



'''
grouped_byday = opaldata.groupby("JS_STRT_DT_FK")
for name_byday,group_byday in grouped_byday:
    #group_byday.sort_values(by=['TAG1_TM'],inplace=True)
    grouped_bytrip = group_byday.groupby("TRIP_ID")
    for name_bytrip,group_bytrip in grouped_bytrip:
        busids = list(set(group_bytrip["BUS_ID"]))
        dic = {}
        for busid in busids:
            df = group_bytrip[group_bytrip["BUS_ID"] == busid]
            dic[busid] = df.shape[0]
        if len(busids)>1:
            #print(busids)
            #print(group_bytrip)
            print(dic)
'''