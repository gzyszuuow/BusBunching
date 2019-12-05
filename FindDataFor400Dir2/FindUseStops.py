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


#ROUTEID from right to left
ROUTEsID1 = ['400-39','400-40','400-57','400-58','400-59']
#ROUTEID from left to right 
ROUTEsID2 = ['400-41','400-42','400-60','400-61','400-62']
#ROUTEID delete
ROUTEsID3 = ['400-43','400-44','400-49','400-50','400-51','400-54','400-69']

Stops_sequence = []

with open('C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\UsedStopsSequence_BusRout400.txt') as f:
    for line in f:
        odom = line.split()
        Stops_sequence.append(int(odom[0]))


busid = 400
path = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\"+str(busid)+".csv"
opaldata =  pd.read_csv(path)
#opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'OPRTR_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_TS_NM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_TS_NM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]
opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]

opaldata = opaldata[~opaldata["ROUTE_VAR_ID"].isin(ROUTEsID3)]
opaldata = opaldata[opaldata["RUN_DIR_CD"] == 2]
#opaldata = opaldata[opaldata["TAG1_TS_NUM"].isin(Stops_sequence) & opaldata["TAG2_TS_NUM"].isin(Stops_sequence)]
print(opaldata)

opaldata.to_csv("C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\400_Dir2.csv")

'''
#{stopid:{"tapon":,"tapoff":,},}
StopsNum = {}

for stopid in Stops_sequence:

    opaldata_part1 = opaldata[opaldata["TAG1_TS_NUM"] == stopid]
    opaldata_part2 = opaldata[opaldata["TAG2_TS_NUM"] == stopid]

    dic = {"Tapon":opaldata_part1.shape[0],"Tapoff":opaldata_part2.shape[0]}
    StopsNum[stopid] = dic

print(StopsNum)

print()
print()

num = 0
for stopid,dic in StopsNum.items():
    if dic["Tapon"]+dic["Tapoff"]>5000:
        print(stopid)
        print(dic)
        num+=1

print(num)

print()
print()
print()

for stopid in Stops_sequence:

    opaldata_part1 = opaldata[opaldata["TAG1_TS_NUM"] == stopid]
    opaldata_part2 = opaldata[opaldata["TAG2_TS_NUM"] == stopid]
    dic = {"Tapon":opaldata_part1.shape[0],"Tapoff":opaldata_part2.shape[0]}

    opaldata_ = opaldata[opaldata["TAG1_TS_NUM"] == stopid]
    opaldata_ = opaldata_[['TAG1_TM', 'TAG1_TS_NUM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]
    print(stopid)
    print(opaldata_.head(10))
    print(dic)
    print("-----------------------------------------")
    print()
'''