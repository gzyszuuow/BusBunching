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

BusIDs = [380]
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
            
            path_headway = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\Product_Condidate_Data\\Headway_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
            path_dwelltime = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\Product_Condidate_Data\\DwellTime_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
            path_stopfeatures = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\StopFeatures_BusRout"+str(busid)+"_Dir"+str(dire)+".json"


            Headway = None
            with open(path_headway) as f:
                d = json.load(f)
                Headway = dict(d)

            Dwelltime = None
            with open(path_dwelltime) as f:
                d = json.load(f)
                Dwelltime = dict(d)

            StopFeatures_each = None
            with open(path_stopfeatures) as f:
                d = json.load(f)
                StopFeatures_each = dict(d)

            Stops_sequence = []
            with open('C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\Product_Condidate_Data\\StopsSequence_BusRout'+str(busid)+'_Dir'+str(dire)+'.txt') as f:
                for line in f:
                    odom = line.split()
                    Stops_sequence.append(str(odom[0]))
            Stops_sequences[busid][dire] = copy.deepcopy(Stops_sequence)
            
            StopFeatures[busid][dire] = StopFeatures_each

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

            dwelltime_num = 0
            for day,dwelltime_dic in Dwelltime.items():
                #delete the pulicholiday data
                if day in PublicHoliday:
                    continue
                Dwelltime_normalization[busid][dire][day] = {}
                for tripid,stop_value_dic in dwelltime_dic.items():
                    newdwelltime = []
                    for stopid in Stops_sequence:
                        if stopid not in stop_value_dic.keys():
                            newdwelltime.append(0)
                        else:
                            x = stop_value_dic[stopid]
                            if x>MaxDwelltime:
                                newdwelltime.append(1)
                            elif x<MinDwelltime:
                                newdwelltime.append(0)
                            else:
                                newdwelltime.append((x-MinDwelltime)/(MaxDwelltime-MinDwelltime))  
                    Dwelltime_normalization[busid][dire][day][tripid] = newdwelltime
                    dwelltime_num+=1

    return Stops_sequences,TripNumber,Headway_normalization,Dwelltime_normalization,StopFeatures

Stops_sequences,TripNumber,Headway_normalization,Dwelltime_normalization,StopFeatures = NormalizeData()



def get_train_dataset():

    X2_train_headway = []
    X1_train_stopfeatures = []
    y_train_target_headway = []

    #build decoder input / historical headway
    for busid in BusIDs:
        for dire in Directions:

            for i in range(historical_prenum,list(TripNumber[busid][dire].keys())[len(TripNumber[busid][dire].keys())-1]):
                ls = []

                pre_num = historical_prenum
                while pre_num>=1:
                    trip_num = i-pre_num
                    day = TripNumber[busid][dire][trip_num]["Day"]
                    tripid = TripNumber[busid][dire][trip_num]["TripID"]
                    trip_headway = Headway_normalization[busid][dire][day][tripid]
                    if dire == 1:
                        ls.append(trip_headway)
                    else:
                        trip_headway_ = []
                        index = len(trip_headway)-1
                        while(index>=0):
                            index-=1
                            trip_headway_.append(trip_headway[index])
                        ls.append(trip_headway_)

                    pre_num-=1
                X2_train_headway.append(ls)


    #build encoder input / Stops features
    for busid in BusIDs:
        for dire in Directions:
            #Stops_sequence = Stops_sequences[busid][dire]

            for i in range(historical_prenum,list(TripNumber[busid][dire].keys())[len(TripNumber[busid][dire].keys())-1]):
                '''
                i_ = i
                day = TripNumber[busid][dire][i_]["Day"]
                tripid = TripNumber[busid][dire][i_]["TripID"]
                while(tripid not in list(StopFeatures[day].keys())):
                    day = TripNumber[busid][dire][i_]["Day"]
                    tripid = TripNumber[busid][dire][i_]["TripID"]
                    i_+=1
                '''
                day = TripNumber[busid][dire][i]["Day"]
                tripid = TripNumber[busid][dire][i]["TripID"]
                #X1_train_stopfeatures.append(StopFeatures[day][tripid])

                #print(StopFeatures[day][tripid])
                #print(type(StopFeatures[day][tripid]))
                #print()
                ls = []
                for x in StopFeatures[busid][dire][day][tripid][0]:
                    #print(x)
                    if len(x)<11:
                        #print(len(x))
                        x.append(0)
                    ls.append(x)

                
                X1_train_stopfeatures.append(ls)

                '''
                i_ = i
                day = TripNumber[busid][dire][i_]["Day"]
                tripid = TripNumber[busid][dire][i_]["TripID"]
                while(tripid not in list(StopFeatures[day].keys())):
                    day = TripNumber[busid][dire][i_]["Day"]
                    tripid = TripNumber[busid][dire][i_]["TripID"]
                    i_+=1
                day = TripNumber[busid][dire][i_]["Day"]
                tripid = TripNumber[busid][dire][i_]["TripID"]
                print(day)
                print(tripid)
                print(type(tripid))
                print(StopFeatures[day].keys())
                X1_train_stopfeatures.append(StopFeatures[day][int(tripid)])
                '''

    #build decoder target / prediction headway
    for busid in BusIDs:
        for dire in Directions:
            for i in range(historical_prenum,list(TripNumber[busid][dire].keys())[len(TripNumber[busid][dire].keys())-1]):

                ls = []
                
                day = TripNumber[busid][dire][i]["Day"]
                tripid = TripNumber[busid][dire][i]["TripID"]
                trip_headway = Headway_normalization[busid][dire][day][tripid]
            
                if dire == 1:
                    ls.append(trip_headway)
                else:
                    trip_headway_ = []
                    index = len(trip_headway)-1
                    while(index>=0):
                        index-=1
                        trip_headway_.append(trip_headway[index])
                    ls.append(trip_headway_)

                y_train_target_headway.append(ls)

    print(len(X2_train_headway))
    print(len(y_train_target_headway))
    print(len(X1_train_stopfeatures))

    X2_train_headway_arr = np.array(X2_train_headway)
    y_train_target_headway_arr = np.array(y_train_target_headway)
    X1_train_stopfeatures_arr = np.array(X1_train_stopfeatures)

    print(X2_train_headway_arr.shape)
    print(y_train_target_headway_arr.shape)
    print(X1_train_stopfeatures_arr.shape)

    x = []
    while(len(x)<X2_train_headway_arr.shape[0]):
        x_ = np.random.randint(0,X2_train_headway_arr.shape[0],1)
        for val in x_:
            if val not in x:
                x.append(val)

    X2_train_headway_shuffle = []
    y_train_target_headway_shuffle = []
    X1_train_stopfeatures_shuffle = []
    for val in x:
        X2_train_headway_shuffle.append(X2_train_headway[val])
        y_train_target_headway_shuffle.append(y_train_target_headway[val])
        X1_train_stopfeatures_shuffle.append(X1_train_stopfeatures[val])

    X1_train_stopfeatures = np.array(X1_train_stopfeatures_shuffle)
    X2_train_headway = np.array(y_train_target_headway_shuffle)
    y_train_target_headway = np.array(y_train_target_headway_shuffle)


    return X1_train_stopfeatures,X2_train_headway,y_train_target_headway


#X1_train_stopfeatures,X2_train_headway,y_train_target_headway = get_train_dataset()

'''
print(X1_train_stopfeatures.shape)
print(X2_train_headway.shape)
print(y_train_target_headway.shape)
print()
'''


'''
for x,y in StopFeatures.items():
    print(x)
    print(y.keys())
    print()
'''