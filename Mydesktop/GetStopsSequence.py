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
ROUTEsID1 = ['39','40','57','58','59']
#ROUTEID from left to right 
ROUTEsID2 = ['41','42','60','61','62']
#ROUTEID delete
ROUTEsID3 = ['43','44','49','50','51','54','69']

path = "/Users/gongcengyang/Desktop/BusBunching-master/Data/400Afterfilter.csv"
opaldata =  pd.read_csv(path)
opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'OPRTR_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_TS_NM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_TS_NM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]

#1. the earliest time of each routid each day
EarliestTime = {}
grouped_byday = opaldata.groupby("JS_STRT_DT_FK")

for name_byday,group_byday in grouped_byday:
    EarliestTime[name_byday] = {}
    #group_byday.sort_values(by=['TAG1_TM'],inplace=True)
    grouped_byROUTE_VAR = group_byday.groupby("ROUTE_VAR_ID")
    for name_byROUTE_VAR,group_byROUTE_VAR  in grouped_byROUTE_VAR:
        group_byROUTE_VAR.sort_values(by=['TAG1_TM'],inplace=True)

        EarliestTime[name_byday][name_bytrip] = 

#2. The bus ids of each ROUTE_VAR_ID

#3. draw stops map for each ROUTEs

