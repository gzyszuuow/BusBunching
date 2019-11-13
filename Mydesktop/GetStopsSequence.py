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

import numpy as np  # 数组相关的库
import matplotlib.pyplot as plt  # 绘图库


#ROUTEID from right to left
ROUTEsID1 = ['400-39','400-40','400-57','400-58','400-59']
#ROUTEID from left to right 
ROUTEsID2 = ['400-41','400-42','400-60','400-61','400-62']
#ROUTEID delete
ROUTEsID3 = ['400-43','400-44','400-49','400-50','400-51','400-54','400-69']

busid = 400
path = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\"+str(busid)+".csv"
opaldata =  pd.read_csv(path)
#opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'OPRTR_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_TS_NM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_TS_NM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]
opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]

opaldata = opaldata[~opaldata["ROUTE_VAR_ID"].isin(ROUTEsID3)]

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
