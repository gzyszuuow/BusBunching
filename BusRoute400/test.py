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

'''
BusIDs = [400,380]
Directions = [1,2]
#PublicHoliday  = ["2016-02-06","2016-02-07","2016-02-13","2016-02-14","2016-02-20","2016-02-21","2016-02-27","2016-02-28",
#"2016-03-05","2016-03-06","2016-03-12","2016-03-13","2016-03-19","2016-03-20","2016-03-25","2016-03-26","2016-03-27","2016-03-28"]
PublicHoliday = []

EncoderStopSequence = {1:[0,0,0,0,1],2:[0,0,0,1,0],3:[0,0,0,1,1],4:[0,0,1,0,0],5:[0,0,1,0,1],6:[0,0,0,1,1],
7:[0,0,1,0,0],8:[0,0,1,0,1],9:[0,0,1,1,0],10:[0,0,1,1,1],11:[0,1,0,0,0],12:[0,1,0,0,1],
13:[0,0,1,0,0],14:[0,0,1,0,1],15:[0,0,1,1,0],16:[0,0,1,1,1],17:[0,1,0,0,0],18:[0,1,0,0,1],19:[0,1,0,1,0],
20:[0,1,0,1,1],21:[0,1,1,0,0],22:[0,1,1,0,1],23:[0,1,1,1,0],24:[0,1,1,1,1],25:[1,0,0,0,0],26:[1,0,0,0,1],
27:[1,0,0,1,0],28:[1,0,0,1,1]}

ExchangeStopsForEachRoute = {400:{1:[202273,202067,202015,221622,221617,2207184,219411,213451],2:[213434,219417,221618,221621,202015,2020113,202266]},
380:{1:[202268,200057,2000421,200065],2:[20002,200081,200071,202267]}}

historical_prenum = 10

MaxHeadway = 30
MinHeadway = 0
MaxDwelltime = 10
MinDwelltime = 0

number_test = 100


def FindNearTripOtherDays(Day,TripID,StartStop,ArrivalTime):
    starttime1 = ArrivalTime[Day][TripID][str(StartStop)]
    NearTripForTripID = {}
    for day,trip_dic in ArrivalTime.items():
        if day!=Day:
            NearTripForTripID[day] = []

            for tripid,trip in trip_dic.items():
                starttime2 = ArrivalTime[day][tripid][str(StartStop)]
                TimeGap = starttime2 - starttime1
                if abs(TimeGap)<=3600*5:
                    dic = {"TripID":tripid,"TimeGap":abs(starttime2 - starttime1)}
                    NearTripForTripID[day].append(dic)
    return NearTripForTripID




for busid in BusIDs:
    for dire in Directions:
        path_ArrivalTime = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\Product_Condidate_Data\\ArrivalTime_BusRout"+str(busid)+"_Dir"+str(dire)+".json"

        ArrivalTime = None
        with open(path_ArrivalTime) as f:
            d = json.load(f)
            ArrivalTime = dict(d)

        Stops_sequence = []
        with open('C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\Product_Condidate_Data\\StopsSequence_BusRout'+str(busid)+'_Dir'+str(dire)+'.txt') as f:
            for line in f:
                odom = line.split()
                Stops_sequence.append(str(odom[0]))
        #Stops_sequences[busid][dire] = copy.deepcopy(Stops_sequence)            
        AllNearTrips = {}
        for day,trip_dic in ArrivalTime.items():
            AllNearTrips[day] = {}
            for tripid,trip in trip_dic.items():
                
                start_stop = str(Stops_sequence[0])
                AllNearTrips[day][tripid] = FindNearTripOtherDays(day,tripid,start_stop,ArrivalTime)
        
        #print(AllNearTrips)

        AllNearTrips_json = json.dumps(AllNearTrips)
        path_json = 'AllNearTrips_BusRout'+str(busid)+'_Dir'+str(dire)+".json"
        fileObject = open(path_json, 'w')
        fileObject.write(AllNearTrips_json)
        fileObject.close()

        print(busid)
        print(dire)
        print()



#-------------------------------------------------------------------------------------
def NormalizeData():

    Headway_normalization = {}  # {busid:{day:{id:[],id:[]...},day:....},busid:{day:{}}}
    Dwelltime_normalization = {} #
    Stops_sequences = {}

    TripNumber = {} # {busid:{num:{"Day":,"Tripid":},num:{"Day":,"Tripid":}},busid:....}
    TestTrip = {}

    for busid in BusIDs:

        Headway_normalization[busid] = {}
        Dwelltime_normalization[busid] = {}
        Stops_sequences[busid] = {}
        TripNumber[busid] = {}
        TestTrip[busid] = {}
        
        for dire in Directions:

            Headway_normalization[busid][dire] = {}
            Dwelltime_normalization[busid][dire] = {}
            Stops_sequences[busid][dire] = {}
            TripNumber[busid][dire] = {}
            TestTrip[busid][dire] = list(np.random.randint(100,4000,size = number_test))
            
            path_headway = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\Product_Condidate_Data\\Headway_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
            path_dwelltime = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\Product_Condidate_Data\\DwellTime_BusRout"+str(busid)+"_Dir"+str(dire)+".json"

            Headway = None
            with open(path_headway) as f:
                d = json.load(f)
                Headway = dict(d)

            Dwelltime = None
            with open(path_dwelltime) as f:
                d = json.load(f)
                Dwelltime = dict(d)

            Stops_sequence = []
            with open('C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\Product_Condidate_Data\\StopsSequence_BusRout'+str(busid)+'_Dir'+str(dire)+'.txt') as f:
                for line in f:
                    odom = line.split()
                    Stops_sequence.append(str(odom[0]))
            Stops_sequences[busid][dire] = copy.deepcopy(Stops_sequence)

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

    return Stops_sequences,TestTrip,TripNumber,Headway_normalization,Dwelltime_normalization

#Stops_sequences,TestTrip,TripNumber,Headway_normalization,Dwelltime_normalization = NormalizeData()


#def HandleStopFeatures(Busid,Direction,Stopid):



def get_train_dataset():

    X2_train_headway = []
    X1_train_stopfeatures = []
    y_train_target_headway = []

    #build decoder input / historical headway
    for busid in BusIDs:
        for dire in Directions:

            for i in range(historical_prenum,list(TripNumber[busid][dire].keys())[len(TripNumber[busid][dire].keys())-1]):
                if i not in TestTrip[busid][dire]:
                    ls = []

                    pre_num = historical_prenum
                    while pre_num>=1:
                        trip_num = i-pre_num
                        day = TripNumber[busid][dire][trip_num]["Day"]
                        tripid = TripNumber[busid][dire][trip_num]["TripID"]
                        trip_headway = Headway_normalization[busid][dire][day][tripid]
                        
                        ls.append(trip_headway)
                        pre_num-=1
                    X2_train_headway.append(ls)

    #build encoder input / Stops features
    for busid in BusIDs:
        for dire in Directions:

            Stops_sequence = Stops_sequences[busid][dire]
            for i in range(historical_prenum,list(TripNumber[busid][dire].keys())[len(TripNumber[busid][dire].keys())-1]):
                if i not in TestTrip[busid][dire]:

                    ls = []
                    for index in range(0,len(Stops_sequence)):
                        stopid = int(Stops_sequence[index])
                        ls_each_stop = []
                        #Stop ID
                        #ls_each_stop+=EncoderStopSequence[index+1]
                        #Exchange stop
                        if stopid in ExchangeStopsForEachRoute[busid][dire]:
                            ls_each_stop.append(1)
                        else:
                            ls_each_stop.append(0)
                        # historical_prenum dwell time
                        pre_num = historical_prenum
                        while pre_num>=1:
                            trip_num = i-pre_num
                            day = TripNumber[busid][dire][trip_num]["Day"]
                            tripid = TripNumber[busid][dire][trip_num]["TripID"]
                            dwelltime = Dwelltime_normalization[busid][dire][day][tripid]
                            ls_each_stop.append(dwelltime[index])
                            pre_num-=1
                        #the probability of BB happened in this stop

                        ls.append(ls_each_stop)        
                    
                    X1_train_stopfeatures.append(ls)


    #build decoder target / prediction headway
    for busid in BusIDs:
        for dire in Directions:
            for i in range(historical_prenum,list(TripNumber[busid][dire].keys())[len(TripNumber[busid][dire].keys())-1]):
                if i not in TestTrip[busid][dire]:

                    ls = []
                    
                    day = TripNumber[busid][dire][i]["Day"]
                    tripid = TripNumber[busid][dire][i]["TripID"]
                    trip_headway = Headway_normalization[busid][dire][day][tripid]
                
                    ls.append(trip_headway)
                    y_train_target_headway.append(ls)



    X2_train_headway = np.array(X2_train_headway)
    y_train_target_headway = np.array(y_train_target_headway)
    X1_train_stopfeatures = np.array(X1_train_stopfeatures)

    return X1_train_stopfeatures,X2_train_headway,y_train_target_headway



def get_test_dataset():

    X2_test_headway = []
    X1_test_stopfeatures = []
    y_test_target_headway = []

    #build decoder input / historical headway
    for busid in BusIDs:
        for dire in Directions:

            for i in range(historical_prenum,list(TripNumber[busid][dire].keys())[len(TripNumber[busid][dire].keys())-1]):
                if i in TestTrip[busid][dire]:
                    ls = []

                    pre_num = historical_prenum
                    while pre_num>=1:
                        trip_num = i-pre_num
                        day = TripNumber[busid][dire][trip_num]["Day"]
                        tripid = TripNumber[busid][dire][trip_num]["TripID"]
                        trip_headway = Headway_normalization[busid][dire][day][tripid]
                        
                        ls.append(trip_headway)
                        pre_num-=1
                    X2_test_headway.append(ls)

    #build encoder input / Stops features
    for busid in BusIDs:
        for dire in Directions:

            Stops_sequence = Stops_sequences[busid][dire]
            for i in range(historical_prenum,list(TripNumber[busid][dire].keys())[len(TripNumber[busid][dire].keys())-1]):
                if i in TestTrip[busid][dire]:

                    ls = []
                    for index in range(0,len(Stops_sequence)):
                        stopid = int(Stops_sequence[index])
                        ls_each_stop = []
                        #Stop ID
                        #ls_each_stop+=EncoderStopSequence[index+1]
                        #Exchange stop
                        if stopid in ExchangeStopsForEachRoute[busid][dire]:
                            ls_each_stop.append(1)
                        else:
                            ls_each_stop.append(0)
                        # historical_prenum dwell time
                        pre_num = historical_prenum
                        while pre_num>=1:
                            trip_num = i-pre_num
                            day = TripNumber[busid][dire][trip_num]["Day"]
                            tripid = TripNumber[busid][dire][trip_num]["TripID"]
                            dwelltime = Dwelltime_normalization[busid][dire][day][tripid]
                            ls_each_stop.append(dwelltime[index])
                            pre_num-=1

                        ls.append(ls_each_stop)        
                    
                    X1_test_stopfeatures.append(ls)


    #build decoder target / prediction headway
    for busid in BusIDs:
        for dire in Directions:
            for i in range(historical_prenum,list(TripNumber[busid][dire].keys())[len(TripNumber[busid][dire].keys())-1]):
                if i in TestTrip[busid][dire]:

                    ls = []
                    
                    day = TripNumber[busid][dire][i]["Day"]
                    tripid = TripNumber[busid][dire][i]["TripID"]
                    trip_headway = Headway_normalization[busid][dire][day][tripid]
                
                    ls.append(trip_headway)
                    y_test_target_headway.append(ls)



    X2_test_headway = np.array(X2_test_headway)
    y_test_target_headway = np.array(y_test_target_headway)
    X1_test_stopfeatures = np.array(X1_test_stopfeatures)

    return X1_test_stopfeatures,X2_test_headway,y_test_target_headway



l = [3,6,9,12]
index = 0
while index<=len(l)-1:
    l[index] = l[index]/3
    index+=1
print(l)
'''


#all bus route cross the same route with 333/380
Stops_sequence = []
with open('StopsSequence_BusRout'+str(333)+'_Dir'+str(380)+'.txt') as f:
    for line in f:
        odom = line.split()
        Stops_sequence.append(int(odom[0]))


for busid in range(0,500):
    for Dir in range(1,3):

        path = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\Data\\DataForAllBuses\\"+str(busid)+".csv"
        if os.path.exists(path) == False:
            continue
        opaldata =  pd.read_csv(path)
        opaldata = opaldata[opaldata["RUN_DIR_CD"] == Dir]
        #drop the outliers
        opaldata = opaldata[~opaldata["TAG1_TS_NUM"].isin(["-1"])]
        opaldata = opaldata[~opaldata["TAG2_TS_NUM"].isin(["-1"])]
        opaldata = opaldata[~opaldata["RUN_DIR_CD"].isin(["-1"])]
        opaldata = opaldata[~opaldata["TRIP_ID"].isin(["-1"])]
        opaldata = opaldata[~opaldata["JS_STRT_DT_FK"].isin(["-1"])]