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

Days = []
with open('C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\Days.txt') as f:
    for line in f:
        odom = line.split()
        Days.append(str(odom[0]))

historical_prenum = 6

def data_each_route(busid,dire):

    path_headway = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\Headway_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
    path_dwelltime = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\DwellTime_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
    path_arrivalTime = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\ArrivalTime_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
    path_neartrip = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\AllNearTrips_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
    path_tripsequence = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\AllNearTrips_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
    
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
    
    return NearTrips,DwellTime,ArrivalTime,TripSequence,Stops_sequence

def get_data():

    X2_headways = []
    X1_stopfeatures = []
    y_target_headway = []

    for busid in BusIDs:
        for dire in Directions:

            NearTrips,DwellTime,ArrivalTime,TripSequence,Stops_sequence = data_each_route(busid,dire)

            for DayNow in Days:
                Trip_Index = historical_prenum+1
                while(Trip_Index<len(TripSequence[DayNow])):
                    #target headway 
                    headway_target = []
                    trip1 = ArrivalTime[DayNow][TripSequence[DayNow][Trip_Index-1]]
                    trip2 = ArrivalTime[DayNow][TripSequence[DayNow][Trip_Index]]
                    for stop in Stops_sequence:
                        headway_target.append(trip2[stop] - trip1[stop])
                    y_target_headway.append(headway_target)

                    #historical headways
                    index_start = Trip_Index - historical_prenum
                    ls = []
                    while(index_start <= Trip_Index-1):
                        headway_his = []
                        trip1_his = ArrivalTime[DayNow][TripSequence[DayNow][index_start-1]]
                        trip2_his = ArrivalTime[DayNow][TripSequence[DayNow][index_start]]
                        for stop in Stops_sequence:
                            headway_his.append(trip2_his[stop] - trip1[stop])
                        ls.append(headway_his)
                    X2_headways.append()


                    Trip_Index+=1






