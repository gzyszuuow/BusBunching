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

#path = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusData\\2016-02-01.csv"
busid = 412
path = "/Users/gongcengyang/Desktop/BusBunching-master/Data/"+str(busid)+".csv"
opaldata =  pd.read_csv(path)

#opaldata = opaldata[["TRIP_ID","BUS_ID","JS_STRT_DT_FK","TAG1_TM","TAG1_TS_NUM","TAG1_TS_NM","TAG1_LAT_VAL", "TAG1_LONG_VAL","TAG2_TM","TAG2_TS_NUM","TAG2_TS_NM","TAG2_LAT_VAL", "TAG2_LONG_VAL"]]
opaldata = opaldata[["ROUTE_ID","BUS_ID","TRIP_ID","JS_STRT_DT_FK","TAG1_TM","TAG1_TS_NUM","TAG1_TS_NM","TAG2_TM","TAG2_TS_NUM","TAG2_TS_NM"]]
#drop the outliers
opaldata = opaldata[~opaldata["TAG1_TS_NUM"].isin([-1])]
opaldata = opaldata[~opaldata["TAG2_TS_NUM"].isin([-1])]
'''
opaldata.sort_values(by=['TAG1_TM'],inplace=True)

grouped = opaldata.groupby(["BUS_ID","TRIP_ID"])

l = []

for _,group in grouped:
    #print(_)
    #print(group)
    l.append(group)
    #print()

def sort_df(s1,s2):
    times1 = list(s1["TAG1_TM"])
    times2 = list(s2["TAG1_TM"])

    time1 = times1[0]
    time2 = times2[0]
    if time1<time2:
        return -1
    if time1>time2:
        return 1
    return 0



l.sort(key = cmp_to_key(sort_df))

#判断站点是不是按照顺序排列的

for df in l:
    stops = list(df["TAG1_TS_NUM"])
    stops_ = copy.deepcopy(stops)
    stops.sort()
    if stops == stops_:
        continue
    else:
        print(stops_)
        print(stops)
        print("*********************************************")
'''


#输出整个两个月时间中上下车乘客很少的车站及其opal信息
stops_ = []
threshold = 10
for stopid,group_bystopid in opaldata.groupby("TAG1_TS_NUM"):
    if group_bystopid.shape[0] <= threshold:
        stops_.append(stopid)
        #print(group_bystopid)
        print(group_bystopid.shape[0])

print()
print(stops_)
print(len(stops_))

opaldata_ = opaldata["TAG1_TS_NUM"].isin([stops_])

print("************************")
print(opaldata[opaldata["TAG1_TS_NUM"].isin(stops_)])