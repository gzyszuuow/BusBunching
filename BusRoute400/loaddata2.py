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
from itertools import groupby
import matplotlib.pyplot as plt

BusIDs = [400]
Directions = [1,2]
PublicHoliday  = ["2016-02-06","2016-02-07","2016-02-13","2016-02-14","2016-02-20","2016-02-21","2016-02-27","2016-02-28",
"2016-03-05","2016-03-06","2016-03-12","2016-03-13","2016-03-19","2016-03-20","2016-03-25","2016-03-26","2016-03-27","2016-03-28"]
#PublicHoliday = []

ExchangeStopsForEachRoute = {400:{1:[202273,202067,202015,221622,221617,2207184,219411,213451],2:[213434,219417,221618,221621,202015,2020113,202266]},
380:{1:[202268,200057,2000421,200065],2:[20002,200081,200071,202267]}}

TimeFeatures = {7*3600:0,10*3600:1,15*3600:2,19*3600:3,24*3600:0}
PassengersType = {0:['Child/Youth','School Student'],1:['Adult','Concession','Employee'],2:['Senior/Pensioner']}


Days = []
with open('C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\Days.txt') as f:
    for line in f:
        odom = line.split()
        Days.append(str(odom[0]))

path_NumberofRoutes = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\StopsBuses.json"
NumberofRoutes = None
with open(path_NumberofRoutes) as f:
    d = json.load(f)
    NumberofRoutes = dict(d)

path = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\400.csv"
opaldata =  pd.read_csv(path)
#opaldata = opaldata.head(10000)


historical_prenum = 3

MaxHeadway = 30
MinHeadway = 0
MaxDwelltime = 10
MinDwelltime = 0

def data_each_route(busid,dire):

    path_headway = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\Headway_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
    path_dwelltime = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\DwellTime_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
    path_arrivalTime = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\ArrivalTime_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
    path_neartrip = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\NearTrips_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
    path_tripsequence = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\TripSequence_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
    
    Stops_sequence = []
    with open('C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\StopsSequence_BusRout'+str(busid)+'_Dir'+str(dire)+'.txt') as f:
        for line in f:
            odom = line.split()
            Stops_sequence.append(str(odom[0]))

    NearTrips = None
    with open(path_neartrip) as f:
        d = json.load(f)
        NearTrips = dict(d)

    DwellTime = None
    with open(path_dwelltime) as f:
        d = json.load(f)
        DwellTime = dict(d)
    
    ArrivalTime = None
    with open(path_arrivalTime) as f:
        d = json.load(f)
        ArrivalTime = dict(d)
    
    TripSequence = None
    with open(path_tripsequence) as f:
        d = json.load(f)
        TripSequence = dict(d)

    TripNumber = {} #{0:{"Day":,"TripID":},1:...}
    num = 0
    for day,l in TripSequence.items():
        for item in l:
            dic = {"Day":day,"TripID":item}
            TripNumber[num] = dic
            num+=1
    
    return NearTrips,DwellTime,ArrivalTime,TripSequence,Stops_sequence,TripNumber


def HistoricalHeadwaysBeforeDay(TripNow_id,daynow,day,NearTrips,TripSequence,ArrivalTime,Stops_sequence):
    headway_day = []

    neartrips_day = NearTrips[daynow][TripNow_id][day]

    tripsequence_day = TripSequence[day]

    for item in neartrips_day:
        tripid_day = item["TripID"]
        tripindex_day = tripsequence_day.index(tripid_day)
        if tripindex_day!=0:
            trip1 = ArrivalTime[day][tripsequence_day[tripindex_day-1]]
            trip2 = ArrivalTime[day][tripsequence_day[tripindex_day]]

            for stop in Stops_sequence:
                t = abs(trip2[str(stop)] - trip1[str(stop)])
                if t>MaxHeadway:
                    headway_day.append(1)
                else:
                    t = (t-MinHeadway)/MaxHeadway
                    headway_day.append(t)
            break
    
    return headway_day


def KindsofPassengers(Day,Stop,TimeFeature,opaldata):
    dropon = []
    dropoff = []
    #name=["CIN","CARD_TYP_CD","ROUTE_ID","ROUTE_VAR_ID","BUS_ID","TS_TYP_CD","OPRTR_ID","RUN_DIR_CD","TRIP_ID","JS_STRT_DT_FK","TAG1_TM","TAG1_TS_NUM","TAG1_TS_NM","TAG1_LAT_VAL","TAG1_LONG_VAL","TAG2_TM","TAG2_TS_NUM","TAG2_TS_NM","TAG2_LAT_VAL","TAG2_LONG_VAL"]
    #opaldata = opaldata["JS_STRT_DT_FK"]
    opaldata = opaldata[opaldata["JS_STRT_DT_FK"] == Day]
    #drop on 
    opaldata_dropon = opaldata[opaldata["TAG1_TS_NUM"] == int(Stop)]
    opaldata_dropon = opaldata_dropon[opaldata_dropon["TimeFeature_Dropon"] == TimeFeature]
    for x in PassengersType.keys():
        opaldata_dropon_ = opaldata_dropon[opaldata_dropon["Passenger_Type"] == x]
        if opaldata_dropon.shape[0] > 0:
            dropon.append(opaldata_dropon_.shape[0]/opaldata_dropon.shape[0])
        else:
            dropon.append(0)
    #drop off
    opaldata_dropoff = opaldata[opaldata["TAG2_TS_NUM"] == int(Stop)]
    opaldata_dropoff = opaldata_dropoff[opaldata_dropoff["TimeFeature_Dropoff"] == TimeFeature]
    for x in PassengersType.keys():
        opaldata_dropoff_ = opaldata_dropoff[opaldata_dropoff["Passenger_Type"] == x]
        if opaldata_dropoff.shape[0] > 0:
            dropoff.append(opaldata_dropoff_.shape[0]/opaldata_dropoff.shape[0])
        else:
            dropoff.append(0)
    return dropon,dropoff

def get_data():

    X2_headways = []
    X1_stopfeatures = []
    y_target_headway = []

    for busid in BusIDs:
        for dire in Directions:

            NearTrips,DwellTime,ArrivalTime,TripSequence,Stops_sequence,TripNumber = data_each_route(busid,dire)

            TripIndex = 2*historical_prenum+1
            while(TripIndex<=list(TripNumber.keys())[len(TripNumber.keys()) - 1]):
                daynow = TripNumber[TripIndex]["Day"]

                print(TripIndex)
                print(daynow)
                print()
                #if TripIndex<470: ##########################################################gaidong
                #    TripIndex+=1
                #    continue

                #1. y_target_headway
                print("y_target_headway")
                tripid1 = TripNumber[TripIndex-1]["TripID"]
                tripid2 = TripNumber[TripIndex]["TripID"]

                trip1 = ArrivalTime[TripNumber[TripIndex-1]["Day"]][tripid1]
                trip2 = ArrivalTime[TripNumber[TripIndex]["Day"]][tripid2]
                target_headway = []
                for stop in Stops_sequence:
                    t = abs(trip2[str(stop)] - trip1[str(stop)])
                    if t>MaxHeadway:
                        target_headway.append(1)
                    else:
                        t = (t-MinHeadway)/MaxHeadway
                        target_headway.append(t)
                ls = []
                ls.append(target_headway)
                
                y_target_headway.append(ls)

                #2. X2_headways
                print("X2_headways")
                headway_his = []

                daynow_index = Days.index(daynow)
                if daynow_index - historical_prenum<0:
                    #2*historical_prenum historical headways before now
                    print("2*historical_prenum historical headways before now")
                    startindex = TripIndex- historical_prenum*2
                    while(startindex <= TripIndex - 1):
                        tripid1_his = TripNumber[startindex-1]["TripID"]
                        tripid2_his = TripNumber[startindex]["TripID"]
                        
                        trip1_his = ArrivalTime[TripNumber[startindex-1]["Day"]][tripid1_his]
                        trip2_his = ArrivalTime[TripNumber[startindex]["Day"]][tripid2_his]
                        
                        headway_his_each = []
                        for stop in Stops_sequence:
                            t = abs(trip2_his[str(stop)] - trip1_his[str(stop)])
                            if t>MaxHeadway:
                                headway_his_each.append(1)
                            else:
                                t = (t-MinHeadway)/MaxHeadway
                                headway_his_each.append(t)
                        headway_his.append(headway_his_each)
                        startindex+=1
                else:
                    #historical days headways + historical_prenum historical headways before now
                    print("historical days headways + historical_prenum historical headways before now")
                    #(1)
                    start_day_index = daynow_index - historical_prenum
                    while(start_day_index < daynow_index):  ######################################gaidong
                        day = Days[start_day_index]
                        
                        headways_beforeday = HistoricalHeadwaysBeforeDay(TripNumber[TripIndex]["TripID"],daynow,day,NearTrips,TripSequence,ArrivalTime,Stops_sequence)
                        headway_his.append(headways_beforeday)
                        start_day_index+=1
                    #(2)
                    startindex = TripIndex - historical_prenum
                    while(startindex <= TripIndex - 1):
                        tripid1_his = TripNumber[startindex-1]["TripID"]
                        tripid2_his = TripNumber[startindex]["TripID"]
                        
                        trip1_his = ArrivalTime[TripNumber[startindex-1]["Day"]][tripid1_his]
                        trip2_his = ArrivalTime[TripNumber[startindex]["Day"]][tripid2_his]
                        
                        headway_his_each = []
                        for stop in Stops_sequence:
                            t = abs(trip2_his[str(stop)] - trip1_his[str(stop)])
                            if t>MaxHeadway:
                                headway_his_each.append(1)
                            else:
                                t = (t-MinHeadway)/MaxHeadway
                                headway_his_each.append(t)
                        headway_his.append(headway_his_each)
                        startindex+=1

                X2_headways.append(headway_his)

                #3. Stop Features
                print("Stop Features")
                ls = []

                startindex = TripIndex - 1
                while(startindex <= TripIndex - 1):
                    tripid = TripNumber[startindex]["TripID"]
                    trip = ArrivalTime[TripNumber[startindex]["Day"]][tripid]

                    stopfeatures_ = []
                    
                    for stop in Stops_sequence:
                        stopfeatures_eachstop = []

                        stopfeatures_eachstop.append(Stops_sequence.index(stop))
                        stopfeatures_eachstop.append(len(NumberofRoutes[stop]))

                        if stop in ExchangeStopsForEachRoute[busid][dire]:
                            stopfeatures_eachstop.append(1)
                        else:
                            stopfeatures_eachstop.append(0)
                        
                        timefeature = -1
                        for k in TimeFeatures.keys():
                            if trip[stop]<k:
                                timefeature = TimeFeatures[k]
                                stopfeatures_eachstop.append(timefeature)
                                break
                        
                        dwell = None
                        if tripid in list(DwellTime[TripNumber[startindex]["Day"]].keys()):
                            if stop in list(DwellTime[TripNumber[startindex]["Day"]][tripid].keys()):
                                dwell = DwellTime[TripNumber[startindex]["Day"]][tripid][stop]
                            else:
                                dwell = 0
                        else:
                            dwell = 0

                        stopfeatures_eachstop.append(dwell)

                        dropon,dropoff = KindsofPassengers(TripNumber[startindex]["Day"],stop,timefeature,opaldata)

                        for i in dropon:
                            stopfeatures_eachstop.append(i)
                        for i in dropoff:
                            stopfeatures_eachstop.append(i)

                        stopfeatures_.append(stopfeatures_eachstop)
                    startindex+=1
                    X1_stopfeatures.append(stopfeatures_)

                #X1_stopfeatures.append(ls)

                TripIndex+=1
        
    return X1_stopfeatures,X2_headways,y_target_headway


X1_stopfeatures,X2_headways,y_target_headway = get_data()

X1_stopfeatures = np.array(X1_stopfeatures)
X2_headways = np.array(X2_headways)
y_target_headway = np.array(y_target_headway)


print(y_target_headway.shape)
print(X2_headways.shape)
print(X1_stopfeatures.shape)

np.save("y_target_headway",y_target_headway)
np.save("X2_headways",X2_headways)
np.save("X1_stopfeatures",X1_stopfeatures)


'''
path1 = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\Test\\y_target_headway.npy"
path2 = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\Test\\X2_headways.npy"
path3 = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\Test\\X1_stopfeatures.npy"

y_target_headway = np.load(path1)
X2_headways = np.load(path2)
X1_stopfeatures = np.load(path3)

index = 0
while index<=49:
    print(y_target_headway[index][0])
    print()
    print()
    print(X2_headways[index][0])
    print()
    print()
    print(X1_stopfeatures[index][0])
    print()
    print()

    print("-------------------------------------")
    for i in y_target_headway[index][0]:
        print(i)
    print()
    print()
    print()
    print("**********************")
    index+=1
'''


###############################################################################################
'''
#label the opldata with TimeFeatures/PassengersType
opaldata_dropon_timefeature = []
opaldata_dropoff_timefeature = []
Types = []
for index,row in opaldata.iterrows():
    dropon_time = row["TAG1_TM"]
    dropoff_time = row["TAG2_TM"]
    pas_type = row["CARD_TYP_CD"]
    
    dropon_feature = None
    dropoff_feature = None
    for x,y in TimeFeatures.items():
        if dropoff_time<=x:
            dropoff_feature = y
        if dropon_time<=x:
            dropon_feature = y
        if (dropoff_feature!=None) and (dropon_feature!=None):
            break
    
    t = None
    for key,l in PassengersType.items():
        if pas_type in l:
            t = key
        if t!=None:
            break
    opaldata_dropon_timefeature.append(dropon_feature)
    opaldata_dropoff_timefeature.append(dropoff_feature)
    Types.append(t)

opaldata["TimeFeature_Dropon"] = opaldata_dropon_timefeature
opaldata["TimeFeature_Dropoff"] = opaldata_dropoff_timefeature
opaldata["Passenger_Type"] = Types

print(opaldata)
opaldata.to_csv("C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\400_labled.csv")
'''


'''
#3. Stop Features
print("Stop Features")
ls = []

startindex = TripIndex - historical_prenum
while(startindex <= TripIndex - 1):
    tripid = TripNumber[startindex]["TripID"]
    trip = ArrivalTime[daynow][tripid]

    stopfeatures_eachtime = []
    
    for stop in Stops_sequence:
        stopfeatures_eachstop = []

        stopfeatures_eachstop.append(Stops_sequence.index(stop))
        stopfeatures_eachstop.append(len(NumberofRoutes[stop]))

        if stop in ExchangeStopsForEachRoute[busid][dire]:
            stopfeatures_eachstop.append(1)
        else:
            stopfeatures_eachstop.append(0)
        
        timefeature = -1
        for k in TimeFeatures.keys():
            if trip[stop]<k:
                timefeature = TimeFeatures[k]
                stopfeatures_eachstop.append(timefeature)
                break
        
        dwell = None
        if tripid in list(DwellTime[TripNumber[startindex]["Day"]].keys()):
            if stop in list(DwellTime[TripNumber[startindex]["Day"]][tripid].keys()):
                dwell = DwellTime[TripNumber[startindex]["Day"]][tripid][stop]
            else:
                dwell = 0
        else:
            dwell = 0

        stopfeatures_eachstop.append(dwell)

        dropon,dropoff = KindsofPassengers(TripNumber[startindex]["Day"],stop,timefeature,opaldata)

        for i in dropon:
            stopfeatures_eachstop.append(i)
        for i in dropoff:
            stopfeatures_eachstop.append(i)

        stopfeatures_eachtime.append(stopfeatures_eachstop)
    startindex+=1
    ls.append(stopfeatures_eachstop)

X1_stopfeatures.append(ls)
'''