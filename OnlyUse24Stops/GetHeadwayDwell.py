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


def TimesDuringTwoTrips(trip1,trip2,DuringSeconds):
    flag = -1
    stops = [val for val in trip1.keys() if val in trip2.keys()]
    for stopid in stops:
        if abs(trip1[stopid] - trip1[stopid]) <= DuringSeconds:
            flag = 1
            break
    return flag


def FindNearTripsAccrossStops(ArrivalTime,stopsNotinTrip,GivenTrip):
    #路过给出trip的未经过stop的 且含有给出trip中的其他stop的 所有trip
    NearTripsAcrossStops = {}   #{stopid:{1hour:[{'Day':,'TripId':},...],{2hour:...}}}

    for stopid in stopsNotinTrip:
        NearTripsAcrossStops[stopid] = {}
        hour = 0
        
        NearTripsNum = 0
        #while(len(NearTripsAcrossStops[stopid]) <= 7 and hour<3):
        #while(NearTripsNum <= 7 and hour<3):
        while(NearTripsNum <= 60):
            NearTripsAcrossStops[stopid][hour] = []
            during_secons = hour*3600

            for day,trip_dic in ArrivalTime.items():
                for tripid,trip in trip_dic.items():

                    if stopid in trip.keys() and len([val for val in trip.keys() if val in GivenTrip.keys()])>0 and TimesDuringTwoTrips(trip,GivenTrip,during_secons) == 1:
                       NearTripsAcrossStops[stopid][hour].append({"Day":day,"Tripid":tripid})

            NearTripsNum += len(NearTripsAcrossStops[stopid][hour])
            hour+=1

    return NearTripsAcrossStops


def AverageArrivalTime(ArrivalTime,Day,Tripid,stopsNotinTrip,GivenTrip,NearTripsAcrossStops):

    for stopnotintrip_id in stopsNotinTrip:
        arrivetimeforstop = []

        neartrips = NearTripsAcrossStops.get(stopnotintrip_id)

        for _, triplist in neartrips.items():
            for dic_item in triplist:
                neartrip = ArrivalTime[dic_item["Day"]][dic_item["Tripid"]]

                stopsintwotrips = [val for val in GivenTrip.keys() if val in neartrip.keys()] 

                for stopintrips_id in stopsintwotrips:
                    traveltime = abs(neartrip[stopintrips_id] - neartrip[stopnotintrip_id])
                    
                    index_stopintrips_id = Stops_sequence28.index(stopintrips_id)
                    if stopnotintrip_id in Stops_sequence28[:index_stopintrips_id]:
                        arrivetimeforstop.append(GivenTrip[stopintrips_id] - traveltime)
                    else:
                        arrivetimeforstop.append(GivenTrip[stopintrips_id] + traveltime)

        ArrivalTime[Day][Tripid][stopnotintrip_id] = sum(arrivetimeforstop)/len(arrivetimeforstop)






def FillNoneValueInArrivalTime(ArrivalTime):

    for day,trip_dic in ArrivalTime.items():
        for tripid,trip in trip_dic.items():
            stopsNotinTrip = [stopid for stopid in Stops_sequence28 if stopid not in trip.keys()]
            
            GivenTrip = copy.deepcopy(trip)

            NearTripsAcrossStops = FindNearTripsAccrossStops(ArrivalTime,stopsNotinTrip,GivenTrip)
            
            AverageArrivalTime(ArrivalTime,day,tripid,stopsNotinTrip,GivenTrip,NearTripsAcrossStops)
            #for dic in NearTripsAcrossStops.values():
            #    print(dic.keys())
            #print(NearTripsAcrossStops.values())
            #print(NearTripsAcrossStops)
            #print("----------------------------------------------")
            #print()



FillNoneValueInArrivalTime(ArrivalTime)


Headway = {}
for day,trip_dic in ArrivalTime.items():

    TripSartTime = []
    for tripid,trip in trip_dic.items():
        start_stop = str(Stops_sequence28[0])
        start_time = trip[start_stop]
        dic = {"SatrtTime":start_time,"TripID":tripid}
        TripSartTime.append(dic)

    TripSartTimeSort = sorted(TripSartTime, key=lambda k: k['SatrtTime'])
    trip_seuence = []
    for dic_item in TripSartTimeSort:
        trip_seuence.append(dic_item["TripID"])

    Headway[day] = {}

    #tripids = list(trip_dic.keys())
    tripids = trip_seuence
    index1 = 0
    index2 = 1
    while(index2<=len(tripids)-1):
        Headway[day][tripids[index2]] = []
        
        trip1 = trip_dic[tripids[index1]]
        trip2 = trip_dic[tripids[index2]]
        flag = 1
        for stopid in Stops_sequence28:
            headway = abs((trip2[str(stopid)] - trip1[str(stopid)])/60)

            Headway[day][tripids[index2]].append(headway)

            if headway>60:
                flag = -1
                break

        if flag == -1:
            del Headway[day][tripids[index2]]

        index1+=1
        index2+=1

print(Headway)


#dwell time in every stop in each trip    {Date1:{tripid:{stop:dwell,stop:dwell...}},{tripid:{stop:dwell,stop:dwell...}}, Date2:} 
DwellTime = {}

for day, trip_dic in Trajectoies.items():
    DwellTime[day] = {}
    for tripid,l in trip_dic.items():
        DwellTime[day][tripid] = {}
        
        index_now = 0
        index_pre = 0
        while(index_now <= len(l)-1):

            stop_now = l[index_now]["Stop"]
            stop_pre = l[index_pre]["Stop"]

            if DwellTime[day][tripid].get(stop_pre) == None:
                while(l[index_now]["Stop"] == l[index_pre]["Stop"]):
                    index_now+=1
                    if index_now == len(l):
                        index_now-=1
                        break
                
                DwellTime[day][tripid][l[index_pre]["Stop"]] = (l[index_now]["Time"] - l[index_pre]["Time"])/60

                index_pres = index_now
            
            else:
                index_now+=1
                index_pre = index_now

print(DwellTime)

