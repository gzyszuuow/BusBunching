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

BusIDs = [400,380]
Directions = [1,2]
PublicHoliday  = ["2016-02-06","2016-02-07","2016-02-13","2016-02-14","2016-02-20","2016-02-21","2016-02-27","2016-02-28",
"2016-03-05","2016-03-06","2016-03-12","2016-03-13","2016-03-19","2016-03-20","2016-03-25","2016-03-26","2016-03-27","2016-03-28"]
#PublicHoliday = []

ExchangeStopsForEachRoute = {400:{1:[202273,202067,202015,221622,221617,2207184,219411,213451],2:[213434,219417,221618,221621,202015,2020113,202266]},
380:{1:[202268,200057,2000421,200065],2:[20002,200081,200071,202267]}}

historical_prenum = 6

MaxHeadway = 30
MinHeadway = 0
MaxDwelltime = 10
MinDwelltime = 0

number_test = 100

def NormalizeData():

    Headway_normalization = {}  # {busid:{day:{id:[],id:[]...},day:....},busid:{day:{}}}
    Dwelltime_normalization = {} #
    StopFeatures = {}
    Stops_sequences = {}

    TripNumber = {} # {busid:{num:{"Day":,"Tripid":},num:{"Day":,"Tripid":}},busid:....}


    for busid in BusIDs:

        Headway_normalization[busid] = {}
        Dwelltime_normalization[busid] = {}
        Stops_sequences[busid] = {}
        StopFeatures[busid] = {}
        TripNumber[busid] = {}

        
        for dire in Directions:

            Headway_normalization[busid][dire] = {}
            Dwelltime_normalization[busid][dire] = {}
            Stops_sequences[busid][dire] = {}
            StopFeatures[busid][dire] = {}
            TripNumber[busid][dire] = {}
            
            #path_headway = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\Product_Condidate_Data\\Headway_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
            #path_dwelltime = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\Product_Condidate_Data\\DwellTime_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
            path_headway = "/Users/gongcengyang/Desktop/Headway_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
            path_dwelltime = "/Users/gongcengyang/Desktop/DwellTime_BusRout"+str(busid)+"_Dir"+str(dire)+".json"

            Headway = None
            with open(path_headway) as f:
                d = json.load(f)
                Headway = dict(d)

            headway_num = 0
            for day,headway_dic in Headway.items():
                #delete the pulicholiday data
                if day in PublicHoliday:
                    continue
                Headway_normalization[busid][dire][day] = {}
                for tripid,headways in headway_dic.items():
                    newheadways = []
                    for x in headways:
                        if x>MaxHeadway:
                            newheadways.append(1)
                        elif x<MinHeadway:
                            newheadways.append(0)
                        else:
                            newheadways.append((x-MinHeadway)/(MaxHeadway-MinHeadway)) 
                    Headway_normalization[busid][dire][day][tripid] = newheadways

                    TripNumber[busid][dire][headway_num] = {"Day":day,"TripID":tripid}
                    headway_num+=1

    return TripNumber,Headway_normalization

TripNumber,Headway_normalization = NormalizeData()

Avgnum = 5

num_i = 0
num_j = num_i+Avgnum

scatters = {}
for stopindex_ in range(0,28):
    scatters[stopindex_] = []

for busid in BusIDs:
    for dire in Directions:
        
        for stopindex in range(0,28):
            
            while (num_j<= 900):
                num_i_ = num_i
                avg = 0
                while(num_i_<=num_j):
                    day = TripNumber[busid][dire][num_i_]["Day"]
                    tripid = TripNumber[busid][dire][num_i_]["TripID"]
                    headway = Headway_normalization[busid][dire][day][tripid]
                    avg+=headway[stopindex]
                    num_i_+=1
                avg = avg/Avgnum * 20

                scatters[stopindex].append(avg)
                print(stopindex)
                num_i = num_j
                num_j+=Avgnum

print(scatters)
print()
print(scatters[0])


plt.plot(scatters[0])
plt.show()












