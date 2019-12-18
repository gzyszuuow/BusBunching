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

                #1. y_target_headway
                tripid1 = TripNumber[TripIndex-1]["TripID"]
                tripid2 = TripNumber[TripIndex]["TripID"]

                trip1 = ArrivalTime[daynow][tripid1]
                trip2 = ArrivalTime[daynow][tripid2]
                target_headway = []
                for stop in Stops_sequence:
                    t = abs(trip2[str(stop)] - trip1[str(stop)])
                    if t>MaxHeadway:
                        target_headway.append(1)
                    else:
                        t = (t-MinHeadway)/MaxHeadway
                        target_headway.append(t)
                
                y_target_headway.append(target_headway)

                #2. X2_headways
                headway_his = []

                daynow_index = Days.index(daynow)
                if daynow_index - historical_prenum<0:
                    #2*historical_prenum historical headways before now
                    startindex = TripIndex- historical_prenum*2
                    while(startindex <= TripIndex - 1):
                        tripid1_his = TripNumber[startindex-1]["TripID"]
                        tripid2_his = TripNumber[startindex]["TripID"]
                        
                        trip1_his = ArrivalTime[daynow][tripid1_his]
                        trip2_his = ArrivalTime[daynow][tripid2_his]
                        
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
                    #(1)
                    start_day_index = daynow_index - historical_prenum
                    while(start_day_index <= daynow_index):
                        day = Days[start_day_index]
                        
                        headways_beforeday = HistoricalHeadwaysBeforeDay(TripNumber[TripIndex]["TripID"],daynow,day,NearTrips,TripSequence,ArrivalTime,Stops_sequence)
                        headway_his.append(headways_beforeday)
                    #(2)
                    startindex = TripIndex - historical_prenum
                    while(startindex <= TripIndex - 1):
                        tripid1_his = TripNumber[startindex-1]["TripID"]
                        tripid2_his = TripNumber[startindex]["TripID"]
                        
                        trip1_his = ArrivalTime[daynow][tripid1_his]
                        trip2_his = ArrivalTime[daynow][tripid2_his]
                        
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
                TripIndex+=1

                #3. Stop Features
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
                        
                        dwell = DwellTime[TripNumber[startindex]["Day"]][tripid][stop]

                        stopfeatures_eachstop.append(dwell)

                        dropon,dropoff = KindsofPassengers(TripNumber[startindex]["Day"],stop,timefeature)


                        





        


