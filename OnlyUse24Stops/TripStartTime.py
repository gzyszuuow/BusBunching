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


#ROUTEID from right to left
ROUTEsID1 = ['400-39','400-40','400-57','400-58','400-59']
#ROUTEID from left to right 
ROUTEsID2 = ['400-41','400-42','400-60','400-61','400-62']
#ROUTEID delete
ROUTEsID3 = ['400-43','400-44','400-49','400-50','400-51','400-54','400-69']

Stops_sequence28 = []

with open('C:\\Users\\zg148\\Desktop\\BusBunching\\OnlyUse24Stops\\28UsedStopsSequence_BusRout400.txt') as f:
    for line in f:
        odom = line.split()
        Stops_sequence28.append(int(odom[0]))


busid = 400
path = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\"+str(busid)+".csv"
opaldata =  pd.read_csv(path)
#opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'OPRTR_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_TS_NM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_TS_NM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]
opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]

opaldata = opaldata[~opaldata["ROUTE_VAR_ID"].isin(ROUTEsID3)]
opaldata = opaldata[opaldata["RUN_DIR_CD"] == 1]
opaldata = opaldata[opaldata["TAG1_TS_NUM"].isin(Stops_sequence28) & opaldata["TAG2_TS_NUM"].isin(Stops_sequence28)]

'''

#busid = 400
path = "/Users/gongcengyang/Desktop/BusBunching-master/Data/Part400.csv"
opaldata =  pd.read_csv(path)
#opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'OPRTR_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_TS_NM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_TS_NM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]
opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]

opaldata = opaldata[~opaldata["ROUTE_VAR_ID"].isin(ROUTEsID3)]
opaldata = opaldata[opaldata["RUN_DIR_CD"] == 1]

Stops_sequence = []

#with open('C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\UsedStopsSequence_BusRout400.txt') as f:
#    for line in f:
#        odom = line.split()
#        Stops_sequence.append(int(odom[0]))
'''

#print(opaldata)

num1 = 0
num2 = 0

#All trajectoies  {Date1:{tripid:[{time:stop},{time:stop}...]},{tripid:[{time:stop},{time:stop}...]}, Date2:}
Trajectoies = {}
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
                dic1 = {'Time':row["TAG1_TM"],'Stop':row["TAG1_TS_NUM"]}
                dic2 = {'Time':row["TAG2_TM"],'Stop':row["TAG2_TS_NUM"]}
                Trajectoies[name_byday][name_bytrip].append(dic1)
                Trajectoies[name_byday][name_bytrip].append(dic2)


for day, trip_dic in Trajectoies.items():

    for tripid,l in trip_dic.items():
        newlist = sorted(l, key=lambda k: k['Time'])
        Trajectoies[day][tripid] = newlist


#arrival time to every stop in each trip  {Date1:{tripid:{stop:time,stop:time...}},{tripid:{stop:time,stop:time...}}, Date2:}
ArrivalTime = {}
for day, trip_dic in Trajectoies.items():
    ArrivalTime[day] = {}
    for tripid,l in trip_dic.items():
        ArrivalTime[day][tripid] = {}
        
        for dic_item in l:
            stopid = dic_item["Stop"]
            time = dic_item["Time"]

            if ArrivalTime[day][tripid].get(stopid) == None:
                ArrivalTime[day][tripid][stopid] = time


TripStartTime = {} #{Date1:{tripid:starttime,tripid:starttime, Date2:}

for day,trip_dic in ArrivalTime.items():

    TripSartTime = []
    for tripid,trip in trip_dic.items():
        #start_stop = str(Stops_sequence28[0])

        i = 0
        start_stop = int(Stops_sequence28[i])
        while start_stop not in trip.keys():
            start_stop = int(Stops_sequence28[i])
            i+=1
        '''
        print(start_stop)
        print(type(start_stop))
        print(trip)
        print(list(trip.keys())[0])
        print(type(list(trip.keys())[0]))
        '''
        start_time = trip[start_stop]
        dic = {"SatrtTime":start_time,"TripID":tripid}
        TripSartTime.append(dic)

    TripSartTimeSort = sorted(TripSartTime, key=lambda k: k['SatrtTime'])





TripStartTime = {} #{Date1:{tripid:starttime,tripid:starttime, Date2:}

for day, trip_dic in Trajectoies.items():

    TripStartTime[day] = {}

    for tripid,l in trip_dic.items():


        starttime_dic = l[0]
        starttime = starttime_dic["Time"]
        starttime = int(starttime)

        hour = starttime//3600
        mint = (starttime%3600)//60

        TripStartTime[day][tripid] = str(hour)+" : "+str(mint)


TripStartTime_ = {} #{Date:[{"Hour":,"Minute":,...}]}

for day, trip_dic in Trajectoies.items():

    TripStartTime_[day] = []

    for tripid,l in trip_dic.items():


        starttime_dic = l[0]
        starttime = starttime_dic["Time"]
        starttime = int(starttime)

        hour = starttime//3600
        mint = (starttime%3600)//60

        dic = {"Hour":hour,"Minute":mint}

        TripStartTime_[day].append(dic)


for day, l in TripStartTime_.items():

    newlist = sorted(l, key=lambda k: k['Hour'])
    TripStartTime_[day] = newlist     

for day,l in TripStartTime_.items():
    print(day)
    print(l)
    print("--------------------------------")
    print()