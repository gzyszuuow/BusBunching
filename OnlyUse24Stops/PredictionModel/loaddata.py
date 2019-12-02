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
import matplotlib.pyplot as plt

#---------------------------read input data---------------------------------------
ExchangeStops = [202273,202067,202015,221622,221617,2207184,219411,213451]

path_stopbuses = "C:\\Users\\zg148\\Desktop\\BusBunching\\OnlyUse24Stops\\StopsBuses.json"
Stops_RoutesNumber = None
with open(path_stopbuses) as f:
    d = json.load(f)
    Stops_RoutesNumber = dict(d)
for stopid,l in Stops_RoutesNumber.items():
    Stops_RoutesNumber[stopid] = len(l)

Max_Stops_RoutesNumber = 20
Min_Stops_RoutesNumber = 1

for stopid,num in Stops_RoutesNumber.items():
    if num>=Max_Stops_RoutesNumber:
        Stops_RoutesNumber[stopid] = 1
    elif num<=Min_Stops_RoutesNumber:
        Stops_RoutesNumber[stopid] = 0
    else:
        Stops_RoutesNumber[stopid] = (num-Min_Stops_RoutesNumber)/(Max_Stops_RoutesNumber-Min_Stops_RoutesNumber)

Stops_sequence = []
with open('C:\\Users\\zg148\\Desktop\\BusBunching\\OnlyUse24Stops\\28UsedStopsSequence_BusRout400.txt') as f:
    for line in f:
        odom = line.split()
        Stops_sequence.append(str(odom[0]))

path_headway = "C:\\Users\\zg148\\Desktop\\BusBunching\\OnlyUse24Stops\\Headway_BusRout400_Dir1.json"
path_dwelltime = "C:\\Users\\zg148\\Desktop\\BusBunching\\OnlyUse24Stops\\DwellTime_BusRout400_Dir1.json"

Headway = None
with open(path_headway) as f:
    d = json.load(f)
    Headway = dict(d)

Dwelltime = None
with open(path_dwelltime) as f:
    d = json.load(f)
    Dwelltime = dict(d)

#--------------------------setup parameter------------------------------
number_test = 300
testTrip = list(np.random.randint(100,5900,size = number_test))

TripNumber,Headway_normalization,Dwelltime_normalization = NormalizeData()


def DrawTheHist(AllHeadways,AllDwelltime):
    AllHeadways = np.array(AllHeadways)
    AllDwelltime = np.array(AllDwelltime)

    plt.subplot(121)
    plt.title("AllHeadways")
    plt.hist(AllHeadways,rwidth=0.2)
    plt.xticks(range(0, 60,5))

    plt.subplot(122)
    plt.title("AllDwelltime")
    plt.hist(AllDwelltime,rwidth=0.1)
    plt.xticks(range(0, 10,1))

    plt.show()

def NormalizeData():

    Headway_normalization = {}  # {day:{id:[],id:[]...},day:....}
    Dwelltime_normalization = {} #

    TripNumber = {} # {num:{"Day":,"Tripid":},num:{"Day":,"Tripid":}}

    MaxHeadway = 30
    MinHeadway = 0
    MaxDwelltime = 10
    MinDwelltime = 0

    Headway_num = 0
    for day,dic in Headway.items():
        Headway_normalization[day] = {}

        for tripid,headways in dic.items():

            newlist = []
            for x in headways:
                if x>MaxHeadway:
                    newlist.append(1)
                elif x<MinHeadway:
                    newlist.append(0)
                else:
                    newlist.append((x-MinHeadway)/(MaxHeadway-MinHeadway))
            
            #Headway_normalization[Headway_num] = newlist
            TripNumber[Headway_num] = {"Day":day,"TripID":tripid}

            Headway_normalization[day][tripid] = newlist
            Headway_num+=1


    Dwelltime_num = 0
    for day,dic in Dwelltime.items():
        Dwelltime_normalization[day] = {}

        for tripid,stop_value_dic in dic.items():

            newlist = []
            for stopid in Stops_sequence:
                if stopid not in stop_value_dic.keys():
                    newlist.append(0)
                else:
                    x = stop_value_dic[stopid]
                    if x>MaxDwelltime:
                        newlist.append(1)
                    elif x<MinDwelltime:
                        newlist.append(0)
                    else:
                        newlist.append((x-MinDwelltime)/(MaxDwelltime-MinDwelltime))                    

            #Dwelltime_normalization[Dwelltime_num] = newlist
            Dwelltime_normalization[day][tripid] = newlist
            Dwelltime_num+=1

    return TripNumber,Headway_normalization,Dwelltime_normalization


def get_train_dataset():

    #build decoder input
    X2 = []
    for i in range(5,list(TripNumber.keys())[len(TripNumber.keys())-1]):
        if i not in testTrip:
            ls = []

            pre_num = 5
            while pre_num>=1:
                trip_num = i-pre_num
                day = TripNumber[trip_num]["Day"]
                tripid = TripNumber[trip_num]["TripID"]
                trip_headway = Headway_normalization[day][tripid]
                
                ls.append(trip_headway)
                
                pre_num-=1
            X2.append(ls)
    X2 = np.array(X2)

    #build encoder input
    X1 = []
    for i in range(5,list(TripNumber.keys())[len(TripNumber.keys())-1]):
        if i not in testTrip:
            day = TripNumber[i]["Day"]
            tripid = TripNumber[i]["TripID"]
            trip_dwell = Dwelltime_normalization[day][tripid]

            ls = []

            for index in range(0,len(Stops_sequence)):
                ls_each_stop = []
                stopid = int(Stops_sequence[index])
                if stopid in ExchangeStops:
                    ls_each_stop.append(1)
                else:
                    ls_each_stop.append(0)

                ls_each_stop.append(trip_dwell[index])
                ls_each_stop.append(Stops_RoutesNumber[str(stopid)])

                ls.append(ls_each_stop)        
            
            X1.append(ls)
    X1 = np.array(X1)

    #build decoder target
    y = []
    for i in range(5,list(TripNumber.keys())[len(TripNumber.keys())-1]):
        if i not in testTrip:

            ls = []
            
            day = TripNumber[i]["Day"]
            tripid = TripNumber[i]["TripID"]
            trip_headway = Headway_normalization[day][tripid]
        
            ls.append(trip_headway)
            y.append(ls)
    y = np.array(y)

    return X1,X2,y

#X1,X2,y = get_train_dataset()

'''
a = np.arange(10)
print(a)
print(type(a))
plt.hist(a,rwidth=0.5)
plt.show()


def NormalizeData():

    Headway_normalization = {}  #{1:[],2:[]...}
    Dwelltime_normalization = {} #{1:[],2:[]...}

    AllHeadways = []
    AllDwelltime = []

    MaxHeadway = -1000
    MinHeadway = 1000
    MaxDwelltime = -1000
    MinDwelltime = 1000

    for day,dic in Headway.items():
        for tripid,headways in dic.items():

            max_value = max(headways)
            min_value = min(headways)
            
            if max_value>MaxHeadway:
                MaxHeadway = max_value
            if min_value<MinHeadway:
                MinHeadway = min_value

            AllHeadways+=headways

    for day,dic in Dwelltime.items():
        for tripid,stop_value_dic in dic.items():

            max_value = max(list(stop_value_dic.values()))
            min_value = min(list(stop_value_dic.values()))
            
            if max_value>MaxDwelltime:
                MaxDwelltime = max_value
            if min_value<MinDwelltime:
                MinDwelltime = min_value

            AllDwelltime+=list(stop_value_dic.values())
    
    print(MaxHeadway)
    print(MinHeadway)
    print()
    print(MaxDwelltime)
    print(MinDwelltime)

    #DrawTheHist(AllHeadways,AllDwelltime)
    print()
    print()
    threshold = 10
    num_threshold = 0
    for i in AllDwelltime:
        if i > threshold:
            #print(i)
            num_threshold+=1
    print(num_threshold)
    print(len(AllHeadways))

'''
#NormalizeData()  Headway_num = 0