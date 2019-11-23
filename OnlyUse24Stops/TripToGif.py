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
import imageio

#path = "/Users/gongcengyang/Desktop/BusBunching-master/Data/400Afterfilter.csv"
busid = 400
path = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\"+str(busid)+".csv"
opaldata =  pd.read_csv(path)

opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'OPRTR_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_TS_NM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_TS_NM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]
#opaldata = opaldata[["ROUTE_ID", 'ROUTE_VAR_ID','BUS_ID', "TRIP_ID","JS_STRT_DT_FK","TAG1_TM","TAG1_TS_NUM","TAG2_TM","TAG2_TS_NUM"]]
#opaldata = opaldata.head(10000)

path_json = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\AllStopsBusRoute400.json"
AllStopsBusRoute400 = None
with open(path_json) as f:
    d = json.load(f)
    AllStopsBusRoute400 = dict(d)

path_json = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\StopsTimeEachtrip.json"
AllBusTrip400 = None
with open(path_json) as f:
    d = json.load(f)
    AllBusTrip400 = dict(d)

#print(AllBusTrip400)

#draw each trip
def create_gif(image_list, gif_name):
 
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    # Save them as frames into a gif 
    imageio.mimsave(gif_name, frames, 'GIF', duration = 1.5)

'''
for trip_num,trip in AllBusTrip400.items():

    stopimage_list = []
    for stopid in trip.values():
        x = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\Pictures\\Route400Stops\\"+str(stopid)+".png"
        stopimage_list.append(x)
    
    gif_name = 'C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\400Trips\\TripNum'+str(trip_num)+'_gif.gif'
    create_gif(stopimage_list, gif_name)

    print("Trip: "+str(trip_num))
    print(list(trip.values()))
    print()
'''

#每个ROUTE_VAR_ID选出一个trip draw一个看看行驶方向
All_ROUTE_VAR_IDs = list(set(list(opaldata["ROUTE_VAR_ID"])))

for rouid in All_ROUTE_VAR_IDs:

    opaldata_part = opaldata[opaldata["ROUTE_VAR_ID"] == rouid]

    grouped_byday = opaldata_part.groupby("JS_STRT_DT_FK")

    num_day = 0
    for name_byday,group_byday in grouped_byday:

        grouped_bytrip = group_byday.groupby("TRIP_ID")
        #Each ROUTE_VAR_ID draw 21 gif (7 days 3 gif each day)
        num_trip = 0
        for name_bytrip,group_bytrip in grouped_bytrip:
            StopsTimeinEachtrip = {}
            for index,row in group_bytrip.iterrows():
                tapontime = row["TAG1_TM"]
                tapoftime = row["TAG2_TM"]
                taponstop = row["TAG1_TS_NUM"]
                tapoffstop = row["TAG2_TS_NUM"]

                StopsTimeinEachtrip[tapontime] = taponstop
                StopsTimeinEachtrip[tapoftime] = tapoffstop
            
            StopsTimeinEachtrip_sorted = dict(sorted(StopsTimeinEachtrip.items()))

            #draw the gif
            stopimage_list = []
            for stopid in StopsTimeinEachtrip_sorted.values():
                x = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\Pictures\\Route400Stops\\"+str(stopid)+".png"
                stopimage_list.append(x)
            gif_name = 'C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\400Trips\\Direction\\'+str(rouid)+'_TripNum'+str(num_day)+'_'+str(num_trip)+'_gif.gif'
            create_gif(stopimage_list, gif_name)
            num_trip+=1
            if num_trip == 3:
                break

        num_day+=1
        if num_day == 7:
            break



#########################################################
'''
busid = 400
path = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\"+str(busid)+".csv"
opaldata =  pd.read_csv(path)
#all the stops
AllStopsBusRoute400 = {}
StopIDs = []
Xs = []
Ys = []
for index,row in opaldata.iterrows():
    TAG1_TS_NUM = row["TAG1_TS_NUM"]
    TAG2_TS_NUM = row["TAG2_TS_NUM"]

    if AllStopsBusRoute400.get(TAG1_TS_NUM) == None:
        AllStopsBusRoute400[TAG1_TS_NUM] = {"X":row["TAG1_LONG_VAL"],"Y":row["TAG1_LAT_VAL"]}
        StopIDs.append(TAG1_TS_NUM)
    if AllStopsBusRoute400.get(TAG2_TS_NUM) == None:
        AllStopsBusRoute400[TAG2_TS_NUM] = {"X":row["TAG2_LONG_VAL"],"Y":row["TAG2_LAT_VAL"]}
        StopIDs.append(TAG2_TS_NUM)

Threshold = 1500

#The stops passengers(drop on + drop off)<=Threshold
PartStopIDsNoMoreThreshold = []
for stopid in StopIDs:
    num_on = opaldata[opaldata["TAG1_TS_NUM"] == stopid].shape[0]
    num_off = opaldata[opaldata["TAG2_TS_NUM"] == stopid].shape[0]
    if num_on+num_off <= Threshold:
        PartStopIDsNoMoreThreshold.append(stopid)

#The stops passengers(drop on + drop off)>Threshold
PartStopIDsMoreThreshold= []
for stopid in StopIDs:
    if stopid not in PartStopIDsNoMoreThreshold:
        PartStopIDsMoreThreshold.append(stopid)

#draw the picture of each stop

for stopid in AllStopsBusRoute400.keys():
    X = AllStopsBusRoute400[stopid]["X"]
    Y = AllStopsBusRoute400[stopid]["Y"]

    plt.xlim(xmin = 151.075,xmax = 151.30)
    plt.ylim(ymin = -33.985 ,ymax = -33.84)
    plt.scatter(X, Y, alpha=0.6)
    plt.title("StopID: "+str(stopid))
    plt.savefig("C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\Pictures\\Route400Stops\\"+str(stopid)+".png")
    plt.close()
    #plt.show()
'''


'''
AllStopsBusRoute400_json = json.dumps(AllStopsBusRoute400)
print(AllStopsBusRoute400_json)
path_json = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\AllStopsBusRoute400.json"
fileObject = open(path_json, 'w')
fileObject.write(AllStopsBusRoute400_json)
fileObject.close()
'''