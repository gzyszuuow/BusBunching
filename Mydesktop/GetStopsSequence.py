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
#path = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\"+str(busid)+".csv"
#opaldata =  pd.read_csv(path)
#opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'OPRTR_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_TS_NM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_TS_NM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]
#opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]

#opaldata = opaldata[~opaldata["ROUTE_VAR_ID"].isin(ROUTEsID3)]



Stops_sequence = []
Stops_Direction1 = {}

Stops_400Bus_Direction_1_path  = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\Stops_400Bus_Direction_1.json"
#Stops_400Bus_Direction_1_path  = "/Users/gongcengyang/Desktop/BusBunching-master/Data/Stops_400Bus_Direction_1.json"
Stops_400Bus_Direction_1 = None
with open(Stops_400Bus_Direction_1_path) as f:
    d = json.load(f)
    Stops_400Bus_Direction_1 = dict(d)

AllTrips_400Bus_Direction1_path  = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\AllTrips_400Bus_Direction1.json"
#AllTrips_400Bus_Direction1_path  = "/Users/gongcengyang/Desktop/BusBunching-master/Data/AllTrips_400Bus_Direction1.json"
AllTrips_400Bus_Direction1 = None
with open(AllTrips_400Bus_Direction1_path) as f:
    d = json.load(f)
    AllTrips_400Bus_Direction1 = dict(d)

#Filter the stops not in Stops_400Bus_Direction_1
KeysFilterEachTrip = {}
for num,trip_dic in AllTrips_400Bus_Direction1.items():
    KeysFilterEachTrip[num] = []

    for time, stopid in trip_dic.items():
        if str(stopid) not in list(Stops_400Bus_Direction_1.keys()):
            KeysFilterEachTrip[num]+=GetdictKeyByValue(trip_dic,stopid)

for num,trip_dic in AllTrips_400Bus_Direction1.items():
    Keys = KeysFilterEachTrip[num]
    for key in list(set(Keys)):
        del trip_dic[key]


#Trips to determine the sequence of stops
def FindAndInsertPartStops(Stops_sequence,stops):

    Stops_sequence_ = copy.deepcopy(Stops_sequence)

    index = 1
    while(index<=len(Stops_sequence_)-1):
        stopA = Stops_sequence_[index-1]
        stopB = Stops_sequence_[index]
        if (stopA in stops) and (stopB in stops):
            stopA_index = stops.index(stopA)
            stopB_index = stops.index(stopB)

            StopsPart = stops[stopA_index+1:stopB_index]

            index_StopsPart = len(StopsPart)-1
            while(index_StopsPart>=0):
                Stops_sequence_.insert(stopA_index+1,StopsPart[index_StopsPart])
                index_StopsPart-=1
        
        #print(index)
        #print(len(Stops_sequence)-1)
        #print(Stops_sequence)
        #print()
        index+=1

    #return Stops_sequence_
    



def InsertStopIntoStops_sequence(Stops_sequence,stops):

    start_value = Stops_sequence[0]
    end_value = Stops_sequence[len(Stops_sequence)-1]
    
    if (start_value in stops) and (end_value in stops):
        print("InsertStopIntoStops_sequence") 
        start_index_stops = stops.index(start_value)
        end_index_stops = stops.index(end_value)

        index1 = start_index_stops-1
        while(index1>=0):
            Stops_sequence.insert(0,stops[index1])
            index1-=1
        index2 = end_index_stops+1
        while(index2<=len(stops)-1):
            Stops_sequence.insert(len(Stops_sequence),stops[index2])
            index2+=1
        FindAndInsertPartStops(Stops_sequence,stops)
        #Stops_sequence = copy.deepcopy(FindAndInsertPartStops(Stops_sequence,stops))

    elif start_value in stops:

        start_index_stops = stops.index(start_value)
        index1 = start_index_stops-1
        while(index1>=0):
            Stops_sequence.insert(0,stops[index1])
            index1-=1
    
    elif end_value in stops:

        end_index_stops = stops.index(end_value)
        index2 = end_index_stops+1
        while(index2<=len(stops)-1):
            Stops_sequence.insert(len(Stops_sequence),stops[index2])
            index2+=1




Stops_sequence = []

num = 0
for _,trip_dic in AllTrips_400Bus_Direction1.items():
    print(num)
    stops = list(trip_dic.values())
    stops = [x[0] for x in groupby(stops)]

    # if a stop in a trip show more than once at different time ,this trip cannot use
    dic = {}
    for stopid in Stops_400Bus_Direction_1.keys():
        dic[str(stopid)] = 0

    trip_continue_flag = -1
    for stopid in stops:
        dic[str(stopid)] += 1
        if dic[str(stopid)]>1:
            trip_continue_flag = 1
            break
    if trip_continue_flag != 1:
        if num == 0:
            Stops_sequence+=stops
        else:
            InsertStopIntoStops_sequence(Stops_sequence,stops)
        num+=1

print(Stops_sequence)

'''
test part----------------------------------------------todo

def FindAndInsertPartStops(Stops_sequence,stops):

    #Stops_sequence_ = copy.deepcopy(Stops_sequence)

    index = 1
    while(index<=len(Stops_sequence)-1):
        stopA = Stops_sequence[index-1]
        stopB = Stops_sequence[index]
        print(stopA)
        print(stopB)
        print()
        if (stopA in stops) and (stopB in stops):
            stopA_index = stops.index(stopA)
            stopB_index = stops.index(stopB)

            StopsPart = stops[stopA_index+1:stopB_index]

            index_StopsPart = len(StopsPart)-1
            while(index_StopsPart>=0):
                Stops_sequence.insert(stopA_index+1,StopsPart[index_StopsPart])
                index_StopsPart-=1
        
        #print(index)
        #print(len(Stops_sequence)-1)
        #print(Stops_sequence)
        #print()
        index+=1

    #return Stops_sequence_

Stops_sequence = ['a','b','c','d']
stops = ['x','y','b',1,2,3,'c',5,6,7,'d']
FindAndInsertPartStops(Stops_sequence,stops)
print(Stops_sequence)


'''

'''
Stops_sequence = {}
for stopid,_ in Stops_400Bus_Direction_1.items():
    Stops_sequence[stopid] = None

num = 0
for _,trip_dic in AllTrips_400Bus_Direction1.items():

    stops = list(trip_dic.values())
    stops = [x[0] for x in groupby(stops)]

    # if a stop in a trip show more than once at different time ,this trip cannot use
    dic = {}
    for stopid in Stops_400Bus_Direction_1.keys():
        dic[str(stopid)] = 0

    trip_continue_flag = -1
    for stopid in stops:
        dic[str(stopid)] += 1
        if dic[str(stopid)]>1:
            trip_continue_flag = 1
            break
    if trip_continue_flag != 1:
        if num == 0:
            index = 0
            for stopid in stops:
                Stops_sequence[stopid] = index
                index+=1
        #else------------------------------------------todo
        else:
            index_stops = 0
            while(index_stops<=len(stops)):




        num+=1
    else:
        continue
print(Stops_sequence)
'''



'''
    if len(stops)>len(Stops_400Bus_Direction_1.keys()):
        dic = {}
        for stopid in Stops_400Bus_Direction_1.keys():

            dic[str(stopid)] = 0
        for stopid in stops:

            dic[str(stopid)] += 1
        #print(stops)
        print(dic)
        print("********************************")
        print(trip_dic)
        print("--------------------------------")
        print()
    if num == '1':
        for stopid in stops:
            Stops_sequence[stopid] = stops.index(stopid)
'''
    
#print(Stops_sequence)




'''
#For direction 1
#(1)找到y值最低的点作为原点
#(2)原点右边的值按照x值由大到小的排列
#(3)原点左边的值按照y值由小到大排列
minStopY = 10000
minStop = 10000
StopsRight = []
StopsLeft = []
for stopid,location_dic in Stops_400Bus_Direction_1.items():
    y = location_dic["Y"]
    if y<minStopY:
        minStopY = y
        minStop = stopid
minStopX = Stops_400Bus_Direction_1[minStop]["X"]
StopsRight_dic = {}
StopsLeft_dic = {}
for stopid,location_dic in Stops_400Bus_Direction_1.items():
    if minStop == stopid:
        continue
    x = location_dic["X"]
    if x>minStopX:
        StopsRight_dic[location_dic["X"]] = stopid
    else:
        StopsLeft_dic[location_dic["Y"]] = stopid
StopsRight_dic = dict(sorted(StopsRight_dic.items(),reverse=True))
StopsLeft_dic = dict(sorted(StopsLeft_dic.items()))
StopsRight = list(StopsRight_dic.values())
StopsLeft = list(StopsLeft_dic.values())
for stopid in StopsRight:
    Stops_sequence.append(stopid)
Stops_sequence.append(minStop)
for stopid in StopsLeft:
    Stops_sequence.append(stopid)
# determine the right sequence of stops
for i,trip in AllTrips_400Bus_Direction1.items():
    
    tripStopsSquence = list(trip.values())
    index1 = 0
    index2 = 0
    while(index1<=len(tripStopsSquence)-2):
        index2 = index1+1
        while(index2<=len(tripStopsSquence)-1):
            stop1 = tripStopsSquence[index1]
            stop2 = tripStopsSquence[index2]
            stop1_index_ = Stops_sequence.index(str(stop1))
            stop2_index_ = Stops_sequence.index(str(stop2))
            if stop1_index_ > stop2_index_:
                print(tripStopsSquence)
                print("--------------------------")
                print()
            index2+=1
        index1+=1            
'''



#For direction 2
#(1)找到y值最低的点作为原点
#(2)原点左边的值按照y值由大到小排列
#(3)原点右边的值按照x值由小到大排列

'''
#Find all the stops can be used
grouped_bydirection = opaldata.groupby("RUN_DIR_CD")
for name_bydirection,group_bydirection in grouped_bydirection:
    #draw all the stops
    StopMapsEachGroup = {}
    StopIDs = []
    Xs = []
    Ys = []
    for index,row in group_bydirection.iterrows():
        TAG1_TS_NUM = row["TAG1_TS_NUM"]
        TAG2_TS_NUM = row["TAG2_TS_NUM"]
        if StopMapsEachGroup.get(TAG1_TS_NUM) == None:
            StopMapsEachGroup[TAG1_TS_NUM] = {"X":row["TAG1_LONG_VAL"],"Y":row["TAG1_LAT_VAL"]}
            StopIDs.append(TAG1_TS_NUM)
            Xs.append(row["TAG1_LONG_VAL"])
            Ys.append(row["TAG1_LAT_VAL"])
        if StopMapsEachGroup.get(TAG2_TS_NUM) == None:
            StopMapsEachGroup[TAG2_TS_NUM] = {"X":row["TAG2_LONG_VAL"],"Y":row["TAG2_LAT_VAL"]}
            StopIDs.append(TAG2_TS_NUM)
            Xs.append(row["TAG2_LONG_VAL"])
            Ys.append(row["TAG2_LAT_VAL"])
        
    plt.subplot(121)
    plt.scatter(Xs, Ys, alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
    plt.title("All stops")
    plt.xlim(xmin = 151.075,xmax = 151.30)
    plt.ylim(ymin = -33.985 ,ymax = -33.84)
    #Threshold = 1500
    Threshold = 2000
    #The stops passengers(drop on + drop off)<=Threshold
    PartStopIDsNoMoreThreshold = []
    for stopid in StopIDs:
        num_on = group_bydirection[group_bydirection["TAG1_TS_NUM"] == stopid].shape[0]
        num_off = group_bydirection[group_bydirection["TAG2_TS_NUM"] == stopid].shape[0]
        if num_on+num_off <= Threshold:
            PartStopIDsNoMoreThreshold.append(stopid)
    PartXsNoMoreThreshold = []
    PartYsNoMoreThreshold = []
    for stopid in PartStopIDsNoMoreThreshold:
        PartXsNoMoreThreshold.append(StopMapsEachGroup[stopid]["X"])
        PartYsNoMoreThreshold.append(StopMapsEachGroup[stopid]["Y"])
    plt.subplot(222)
    plt.scatter(PartXsNoMoreThreshold, PartYsNoMoreThreshold, alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
    plt.title("NoMoreThresold: "+str(len(PartStopIDsNoMoreThreshold))+" stops")
    plt.xlim(xmin = 151.075,xmax = 151.30)
    plt.ylim(ymin = -33.985 ,ymax = -33.84)
    #The stops passengers(drop on + drop off)>Threshold
    PartStopIDsMoreThreshold= []
    for stopid in StopIDs:
        if stopid not in PartStopIDsNoMoreThreshold:
            PartStopIDsMoreThreshold.append(stopid)
    PartXsMoreThreshold = []
    PartYsMoreThreshold = []
    for stopid in PartStopIDsMoreThreshold:
        PartXsMoreThreshold.append(StopMapsEachGroup[stopid]["X"])
        PartYsMoreThreshold.append(StopMapsEachGroup[stopid]["Y"])
    plt.subplot(122)
    plt.scatter(PartXsMoreThreshold, PartYsMoreThreshold, alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
    #plt.title("MoreThresold: "+str(len(PartStopIDsMoreThreshold))+" stops")
    plt.title("Selected stops")
    plt.xlim(xmin = 151.075,xmax = 151.30)
    plt.ylim(ymin = -33.985 ,ymax = -33.84)
    print("Direction: "+str(name_bydirection))
    print("Passenger num: "+str(group_bydirection.shape[0]))
    print(set(group_bydirection["ROUTE_VAR_ID"]))
    print(len(Xs))
    print(len(PartXsMoreThreshold))
    StopMapsEachGroup_partuse = {}
    for stopid in PartStopIDsMoreThreshold:
        StopMapsEachGroup_partuse[stopid] = copy.deepcopy(StopMapsEachGroup[stopid])
    print(StopMapsEachGroup_partuse)
    StopMapsEachGroup_partuse_json = json.dumps(StopMapsEachGroup_partuse)
    path_json = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\Stops_400Bus_Direction_"+str(name_bydirection)+".json"
    fileObject = open(path_json, 'w')
    fileObject.write(StopMapsEachGroup_partuse_json)
    fileObject.close()
    plt.show()
    plt.close()
    print()
    print()
'''  

'''
StopsTimeEachtrip = {}
AllTripsEachDirection = {}
grouped_bydirection = opaldata.groupby("RUN_DIR_CD")
for name_bydirection,group_bydirection in grouped_bydirection:
    num = 0
    grouped_byday = group_bydirection.groupby("JS_STRT_DT_FK")
    for name_byday,group_byday in grouped_byday:
        #group_byday.sort_values(by=['TAG1_TM'],inplace=True)
        grouped_bytrip = group_byday.groupby("TRIP_ID")
        for name_bytrip,group_bytrip in grouped_bytrip:
            AllTripsEachDirection[num] = {}
            for index,row in group_bytrip.iterrows():
                tapontime = row["TAG1_TM"]
                tapoftime = row["TAG2_TM"]
                taponstop = row["TAG1_TS_NUM"]
                tapoffstop = row["TAG2_TS_NUM"]
                AllTripsEachDirection[num][tapontime] = taponstop
                AllTripsEachDirection[num][tapoftime] = tapoffstop
            num+=1
    AllTripsEachDirection_sorted = {}
    #print(StopsTimeEachtrip)
    for i,j in AllTripsEachDirection.items():
        j_ = dict(sorted(j.items()))
        AllTripsEachDirection_sorted[i] = j_
    
    AllTripsEachDirection_json = json.dumps(AllTripsEachDirection_sorted)
    path_json = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\AllTrips_400Bus_Direction"+str(name_bydirection)+".json"
    fileObject = open(path_json, 'w')
    fileObject.write(AllTripsEachDirection_json)
    fileObject.close()
'''

'''
#1. the earliest time of each routid each day
EarliestTime = {}
grouped_byday = opaldata.groupby("JS_STRT_DT_FK")
for name_byday,group_byday in grouped_byday:
    EarliestTime[name_byday] = {}
    #group_byday.sort_values(by=['TAG1_TM'],inplace=True)
    grouped_byROUTE_VAR = group_byday.groupby("ROUTE_VAR_ID")
    for name_byROUTE_VAR,group_byROUTE_VAR  in grouped_byROUTE_VAR:
        group_byROUTE_VAR.sort_values(by=['TAG1_TM'],inplace=True)
        for index,row in group_byROUTE_VAR.iterrows():
            EarliestTime[name_byday][name_byROUTE_VAR] = row["TAG1_TM"]
            break
print(EarliestTime)
'''

#2. The bus ids of each ROUTE_VAR_ID
'''
BusidsForEachROUTE_VAR_ID = {}
BusidsNumForEachROUTE_VAR_ID = {}
grouped_byROUTE_VAR = opaldata.groupby("ROUTE_VAR_ID")
for name_byROUTE_VAR,group_byROUTE_VAR  in grouped_byROUTE_VAR:
    BusidsForEachROUTE_VAR_ID[name_byROUTE_VAR] = list(set(group_byROUTE_VAR["BUS_ID"]))
    BusidsNumForEachROUTE_VAR_ID[name_byROUTE_VAR] = len(list(set(group_byROUTE_VAR["BUS_ID"])))
#print(BusidsForEachROUTE_VAR_ID)
dic1 = {}
dic2 = {}
dic3 = {}
for routeid1 in ROUTEsID1:
    dic1[routeid1] = {}
    dic2[routeid1] = {}
    dic3[routeid1] = {}
    l1 = BusidsForEachROUTE_VAR_ID["400-"+str(routeid1)]
    for routeid2 in ROUTEsID1:
        if routeid1 == routeid2:
            continue
        l2 = BusidsForEachROUTE_VAR_ID["400-"+str(routeid2)]
        #dic1[routeid1][routeid2] = list(set([value for value in l1 if value in l2]))
        dic1[routeid1][routeid2] = len(list(set([value for value in l1 if value in l2])))
    for routeid2 in ROUTEsID2:
        l2 = BusidsForEachROUTE_VAR_ID["400-"+str(routeid2)]
        #dic2[routeid1][routeid2] = list(set([value for value in l1 if value in l2]))
        dic2[routeid1][routeid2] = len(list(set([value for value in l1 if value in l2])))
    for routeid2 in ROUTEsID3:
        l2 = BusidsForEachROUTE_VAR_ID["400-"+str(routeid2)]
        #dic3[routeid1][routeid2] = list(set([value for value in l1 if value in l2]))
        dic3[routeid1][routeid2] = len(list(set([value for value in l1 if value in l2])))
print(dic1)
print()
print(dic2)
print()
print(dic3)
print()
'''
#3. draw stops map for each ROUTEs

#4.intersections stops of each ROUTE_VAR_ID

#passenger number of each ROUTE_VAR_ID

'''
#the direction of each 
num = 0
grouped_bydirection = opaldata.groupby("RUN_DIR_CD")
for name_bydirection,group_bydirection in grouped_bydirection:
    print(name_bydirection)
    print(group_bydirection)
    print(list(set(group_bydirection["ROUTE_VAR_ID"])))
    print()
    num+=1
'''