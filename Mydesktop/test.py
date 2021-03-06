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

#path = "C:\\Users\\zg148\\Desktop\\gzy\\BusBunching\\BusData\\2016-02-01.csv"
#busid = 400
#path = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\"+str(busid)+".csv"
path = "/Users/gongcengyang/Desktop/BusBunching-master/Data/400Afterfilter.csv"
opaldata =  pd.read_csv(path)

#drop the outliers
#opaldata = opaldata[~opaldata["TAG1_TS_NUM"].isin(["-1"])]
#opaldata = opaldata[~opaldata["TAG2_TS_NUM"].isin(["-1"])]

opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'OPRTR_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_TS_NM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_TS_NM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]


#how many stops in each ROUTE_VAR_ID
ROUTE_VARs = {}
ROUTE_VARs_STOPS = {}
ROUTE_VARs_STOPS_NUM = {}
for ROUTE_VAR_ID, group in opaldata.groupby("ROUTE_VAR_ID"):
    
    ROUTE_VARs[ROUTE_VAR_ID] = group.shape[0]

    ROUTE_VARs_STOPS[ROUTE_VAR_ID] = []
    for stop in list(group["TAG1_TS_NUM"]):
        if stop not in ROUTE_VARs_STOPS[ROUTE_VAR_ID]:
            ROUTE_VARs_STOPS[ROUTE_VAR_ID].append(stop)
    for stop in list(group["TAG2_TS_NUM"]):
        if stop not in ROUTE_VARs_STOPS[ROUTE_VAR_ID]:
            ROUTE_VARs_STOPS[ROUTE_VAR_ID].append(stop)
    
    ROUTE_VARs_STOPS_NUM[ROUTE_VAR_ID] = len(ROUTE_VARs_STOPS[ROUTE_VAR_ID])

#rint(ROUTE_VARs_STOPS)

ROUTE_VARs_STOPS_INTERSECTIONS = {}
for routeid in ROUTE_VARs_STOPS.keys():
    ROUTE_VARs_STOPS_INTERSECTIONS[routeid] = {}
    for route_vars_id, route_vars_stops in ROUTE_VARs_STOPS.items():
        if routeid!=route_vars_id:
            l1 = copy.deepcopy(ROUTE_VARs_STOPS[routeid])
            l2 = copy.deepcopy(route_vars_stops)
            l3 = list(set([value for value in l1 if value in l2]))
            #ROUTE_VARs_STOPS_INTERSECTIONS[routeid][route_vars_id] = list(set(l3))
            ROUTE_VARs_STOPS_INTERSECTIONS[routeid][route_vars_id] = len(list(set(l3)))


#print(ROUTE_VARs_STOPS_NUM)
#print()
#print("-------------")
#print()
#print(ROUTE_VARs_STOPS_INTERSECTIONS)

print("------------------------------")
print("------------------------------")
print("------------------------------")

#the sequence of stops
StopsSequence = []
StopsTimeEachtrip = {}
opaldata = opaldata[["ROUTE_ID", 'ROUTE_VAR_ID','BUS_ID', "TRIP_ID","JS_STRT_DT_FK","TAG1_TM","TAG1_TS_NUM","TAG2_TM","TAG2_TS_NUM"]]
grouped_byday = opaldata.groupby("JS_STRT_DT_FK")
num = 0
for name_byday,group_byday in grouped_byday:
    #a json file per day
    dataperday_json = {}
    group_byday.sort_values(by=['TAG1_TM'],inplace=True)
    tripnum_perday = 0
    grouped_bytrip = group_byday.groupby("TRIP_ID")
    for name_bytrip,group_bytrip in grouped_bytrip:
        StopsTimeEachtrip[num] = {}

        for index,row in opaldata.iterrows():
            tapontime = row["TAG1_TM"]
            tapoftime = row["TAG2_TM"]
            taponstop = row["TAG1_TS_NUM"]
            tapoffstop = row["TAG2_TS_NUM"]

            StopsTimeEachtrip[num][tapontime] = taponstop
            StopsTimeEachtrip[num][tapoftime] = tapoffstop
        num+=1

print(StopsTimeEachtrip)
'''
#draw all the stops
StopMapsEachGroup = {}
StopIDs = []
Xs = []
Ys = []
for index,row in opaldata.iterrows():
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
    

plt.subplot(221)
plt.scatter(Xs, Ys, alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
plt.title("All stops")
plt.xlim(xmin = 151.075,xmax = 151.30)
plt.ylim(ymin = -33.985 ,ymax = -33.84)


Threshold = 1500

#The stops passengers(drop on + drop off)<=Threshold
PartStopIDsNoMoreThreshold = []
for stopid in StopIDs:
    num_on = opaldata[opaldata["TAG1_TS_NUM"] == stopid].shape[0]
    num_off = opaldata[opaldata["TAG2_TS_NUM"] == stopid].shape[0]
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

plt.subplot(223)
plt.scatter(PartXsMoreThreshold, PartYsMoreThreshold, alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
plt.title("MoreThresold: "+str(len(PartStopIDsMoreThreshold))+" stops")
plt.xlim(xmin = 151.075,xmax = 151.30)
plt.ylim(ymin = -33.985 ,ymax = -33.84)
plt.show()

#After filter the number of ROUTE_VAR_ID
opaldata_filter = opaldata[opaldata["TAG1_TS_NUM"].isin(PartStopIDsMoreThreshold) & opaldata["TAG2_TS_NUM"].isin(PartStopIDsMoreThreshold)]
ROUTE_VARs = {}
ROUTE_VARs_STOPS = {}
for ROUTE_VAR_ID, group in opaldata_filter.groupby("ROUTE_VAR_ID"):
    
    ROUTE_VARs[ROUTE_VAR_ID] = group.shape[0]

    ROUTE_VARs_STOPS[ROUTE_VAR_ID] = []
    for stop in list(group["TAG1_TS_NUM"]):
        if stop not in ROUTE_VARs_STOPS[ROUTE_VAR_ID]:
            ROUTE_VARs_STOPS[ROUTE_VAR_ID].append(stop)
    for stop in list(group["TAG2_TS_NUM"]):
        if stop not in ROUTE_VARs_STOPS[ROUTE_VAR_ID]:
            ROUTE_VARs_STOPS[ROUTE_VAR_ID].append(stop)
    
    ROUTE_VARs_STOPS[ROUTE_VAR_ID] = len(ROUTE_VARs_STOPS[ROUTE_VAR_ID])
    

print(ROUTE_VARs)
print()
print(ROUTE_VARs_STOPS)
print()
print(len(ROUTE_VARs))
print(len(ROUTE_VARs_STOPS))
'''



#------------------------------------------------------
'''
#The number of ROUTE_VAR_ID
ROUTE_VARs = {}
ROUTE_VARs_STOPS = {}
for ROUTE_VAR_ID, group in opaldata.groupby("ROUTE_VAR_ID"):
    
    ROUTE_VARs[ROUTE_VAR_ID] = group.shape[0]
    ROUTE_VARs_STOPS[ROUTE_VAR_ID] = []
    for stop in list(group["TAG1_TS_NUM"]):
        if stop not in ROUTE_VARs_STOPS[ROUTE_VAR_ID]:
            ROUTE_VARs_STOPS[ROUTE_VAR_ID].append(stop)
    for stop in list(group["TAG2_TS_NUM"]):
        if stop not in ROUTE_VARs_STOPS[ROUTE_VAR_ID]:
            ROUTE_VARs_STOPS[ROUTE_VAR_ID].append(stop)
    
    ROUTE_VARs_STOPS[ROUTE_VAR_ID] = len(ROUTE_VARs_STOPS[ROUTE_VAR_ID])   
    #draw the stops in the ROUTE_VARs_STOPS each group
    StopMapsEachGroup = {}
    StopIDs = []
    Xs = []
    Ys = []
    for index,row in group.iterrows():
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
    
    plt.scatter(Xs, Ys, alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
    plt.xlim(xmin = 151.075,xmax = 151.30)
    plt.ylim(ymin = -33.985 ,ymax = -33.84)
    plt.title("Route ID: "+str(ROUTE_VAR_ID)+"  Passenger Number: "+str(group.shape[0])+"  Stop Number: "+str(len(StopIDs)))
    plt.savefig("C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\"+ROUTE_VAR_ID+".png")
    plt.show()
    
print(ROUTE_VARs)
print()
print(ROUTE_VARs_STOPS)
print()
print(len(ROUTE_VARs))
print(len(ROUTE_VARs_STOPS))
'''



'''
StopMapsFor412 = {}
StopIDs = []
Xs = []
Ys = []
for index,row in opaldata.iterrows():
    TAG1_TS_NUM = row["TAG1_TS_NUM"]
    TAG2_TS_NUM = row["TAG2_TS_NUM"]
    if StopMapsFor412.get(TAG1_TS_NUM) == None:
        StopMapsFor412[TAG1_TS_NUM] = {"X":row["TAG1_LONG_VAL"],"Y":row["TAG1_LAT_VAL"]}
        StopIDs.append(TAG1_TS_NUM)
        Xs.append(row["TAG1_LONG_VAL"])
        Ys.append(row["TAG1_LAT_VAL"])
    if StopMapsFor412.get(TAG2_TS_NUM) == None:
        StopMapsFor412[TAG2_TS_NUM] = {"X":row["TAG2_LONG_VAL"],"Y":row["TAG2_LAT_VAL"]}
        StopIDs.append(TAG2_TS_NUM)
        Xs.append(row["TAG2_LONG_VAL"])
        Ys.append(row["TAG2_LAT_VAL"])
#All the stpos
plt.subplot(221)
plt.scatter(Xs, Ys, alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
plt.xlim(xmin = 151.08,xmax = 151.2)
plt.ylim(ymin = -33.950 ,ymax = -33.8)
Threshold = 1500
#The stops passengers(drop on + drop off)<=Threshold
PartStopIDsNoMoreThreshold = []
for stopid in StopIDs:
    num_on = opaldata[opaldata["TAG1_TS_NUM"] == stopid].shape[0]
    num_off = opaldata[opaldata["TAG2_TS_NUM"] == stopid].shape[0]
    if num_on+num_off <= Threshold:
        PartStopIDsNoMoreThreshold.append(stopid)
PartXsNoMoreThreshold = []
PartYsNoMoreThreshold = []
for stopid in PartStopIDsNoMoreThreshold:
    PartXsNoMoreThreshold.append(StopMapsFor412[stopid]["X"])
    PartYsNoMoreThreshold.append(StopMapsFor412[stopid]["Y"])
plt.subplot(222)
plt.scatter(PartXsNoMoreThreshold, PartYsNoMoreThreshold, alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
plt.xlim(xmin = 151.08,xmax = 151.2)
plt.ylim(ymin = -33.950 ,ymax = -33.8)
#The stops passengers(drop on + drop off)>Threshold
PartStopIDsMoreThreshold= []
for stopid in StopIDs:
    if stopid not in PartStopIDsNoMoreThreshold:
        PartStopIDsMoreThreshold.append(stopid)
PartXsMoreThreshold = []
PartYsMoreThreshold = []
for stopid in PartStopIDsMoreThreshold:
    PartXsMoreThreshold.append(StopMapsFor412[stopid]["X"])
    PartYsMoreThreshold.append(StopMapsFor412[stopid]["Y"])
plt.subplot(223)
plt.scatter(PartXsMoreThreshold, PartYsMoreThreshold, alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
plt.xlim(xmin = 151.08,xmax = 151.2)
plt.ylim(ymin = -33.950 ,ymax = -33.8)
print(len(StopIDs))
print(len(PartXsNoMoreThreshold))
print(len(PartStopIDsMoreThreshold))
print()
print(PartStopIDsMoreThreshold)
plt.show()
opaldata = opaldata[(opaldata["TAG1_TS_NUM"].isin(PartStopIDsMoreThreshold)) | (opaldata["TAG2_TS_NUM"].isin(PartStopIDsMoreThreshold))]
print(opaldata)
opaldata.to_csv("C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\Filtered412.csv")
'''





'''
with open("C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\StopsFor412.txt","a") as f:
    for stopid in PartStopIDsMoreThreshold:
        f.write(str(stopid))
        f.write("\n")
'''


'''
StopMapsFor412 = {}
IDs = []
Xs = []
Ys = []
for index,row in opaldata.iterrows():
    TAG1_TS_NUM = int(row["TAG1_TS_NUM"])
    TAG2_TS_NUM = int(row["TAG2_TS_NUM"])
    if StopMapsFor412.get(TAG1_TS_NUM) == None:
        StopMapsFor412[TAG1_TS_NUM] = {"X":row["TAG1_LONG_VAL"],"Y":row["TAG1_LAT_VAL"]}
        IDs.append(TAG1_TS_NUM)
        Xs.append(row["TAG1_LONG_VAL"])
        Ys.append(row["TAG1_LAT_VAL"])
    if StopMapsFor412.get(TAG2_TS_NUM) == None:
        StopMapsFor412[TAG2_TS_NUM] = {"X":row["TAG2_LONG_VAL"],"Y":row["TAG2_LAT_VAL"]}
        IDs.append(TAG2_TS_NUM)
        Xs.append(row["TAG2_LONG_VAL"])
        Ys.append(row["TAG2_LAT_VAL"])
#print(StopMapsFor412)
StopMapsFor412 = pd.DataFrame(StopMapsFor412)
print(StopMapsFor412)
plt.scatter(Xs, Ys, alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
plt.xlim(xmin = 151.08,xmax = 151.2)
plt.ylim(ymin = -33.950 ,ymax = -33.8)
plt.show()
'''





'''
#The number of ROUTE_VAR_ID
ROUTE_VARs = {}
ROUTE_VARs_STOPS = {}
for ROUTE_VAR_ID, group in opaldata.groupby("ROUTE_VAR_ID"):
    #ROUTE_VARs.append(ROUTE_VAR_ID)
    ROUTE_VARs[ROUTE_VAR_ID] = group.shape[0]
    ROUTE_VARs_STOPS[ROUTE_VAR_ID] = []
    for stop in list(group["TAG1_TS_NUM"]):
        if stop not in ROUTE_VARs_STOPS[ROUTE_VAR_ID]:
            ROUTE_VARs_STOPS[ROUTE_VAR_ID].append(stop)
    for stop in list(group["TAG2_TS_NUM"]):
        if stop not in ROUTE_VARs_STOPS[ROUTE_VAR_ID]:
            ROUTE_VARs_STOPS[ROUTE_VAR_ID].append(stop)
    
    ROUTE_VARs_STOPS[ROUTE_VAR_ID] = len(ROUTE_VARs_STOPS[ROUTE_VAR_ID])   
    print(ROUTE_VAR_ID)
    print(group)
    print("-----------------------------")
print(ROUTE_VARs)
print()
print(ROUTE_VARs_STOPS)
'''

'''
for day,group_byday in opaldata.groupby("JS_STRT_DT_FK"):
    group_byday.sort_values(by=['TAG1_TM'],inplace=True)
    for ROUTE_VAR_ID, group_ROUTE_VAR_ID in group_byday.groupby("ROUTE_VAR_ID"):
        print(ROUTE_VAR_ID)
        print(group_ROUTE_VAR_ID)
        print("------------------------------------------")
'''