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


path = "/Users/gongcengyang/Desktop/BusBunching-master/Data/400Afterfilter.csv"
opaldata =  pd.read_csv(path)

opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'OPRTR_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_TS_NM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_TS_NM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]

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
PartStopIDsMoreThreshold = PartStopIDsMoreThreshold[:3]
for stopid in PartStopIDsMoreThreshold:
    X = AllStopsBusRoute400[stopid]["X"]
    Y = AllStopsBusRoute400[stopid]["Y"]

    plt.xlim(xmin = 151.075,xmax = 151.30)
    plt.ylim(ymin = -33.985 ,ymax = -33.84)
    plt.scatter(X, Y, alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
    plt.show()



