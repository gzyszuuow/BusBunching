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


#busids = [326,327,386,387,369,397,399,412]
busids = [326,327,386,387]

for busid in busids:

    path = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusData\\"+str(busid)+".csv"
    #path = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusData\\2016-02-01.csv"
    opaldata =  pd.read_csv(path)
    opaldata = opaldata[["ROUTE_ID","BUS_ID","TRIP_ID","JS_STRT_DT_FK","TAG1_TM","TAG1_TS_NUM","TAG2_TM","TAG2_TS_NUM"]]

    #drop the outliers
    opaldata = opaldata[~opaldata["TAG1_TS_NUM"].isin([-1])]
    opaldata = opaldata[~opaldata["TAG2_TS_NUM"].isin([-1])]


    grouped_byday = opaldata.groupby("JS_STRT_DT_FK")

    for name_byday,group_byday in grouped_byday:
        #a json file per day
        dataperday_json = {}

        group_byday.sort_values(by=['TAG1_TM'],inplace=True)

        tripnum_perday = 0

        grouped_bytrip = group_byday.groupby("TRIP_ID")
        for name_bytrip,group_bytrip in grouped_bytrip:
            taponNum_pertrip = {}
            tapoffNum_pertrip = {}

            dwellTime = {}

            #tap on
            grouped_bytapon = group_bytrip.groupby("TAG1_TS_NUM")
            for station_idtapon,grouppertrip_bytapon in grouped_bytapon:
                taponNum_pertrip[station_idtapon] = grouppertrip_bytapon.shape[0]
                
            #tap off
            grouped_bytapoff = group_bytrip.groupby("TAG2_TS_NUM")
            for station_idtapoff,grouppertrip_bytapoff in grouped_bytapoff:
                tapoffNum_pertrip[station_idtapoff] = grouppertrip_bytapoff.shape[0]

            #all stops in the trip 
            trip_allstops = list(set(list(group_bytrip["TAG1_TS_NUM"])+list(group_bytrip["TAG2_TS_NUM"])))
            #all stops passengers tap on
            trip_tapon_stops = list(set(list(group_bytrip["TAG1_TS_NUM"])))
            #all stops passengers tap off
            trip_tapoff_stops = list(set(list(group_bytrip["TAG2_TS_NUM"])))


            for stop in trip_allstops:
                #passengers tapon and tapoff at this stop
                if (stop in trip_tapon_stops) and (stop in trip_tapoff_stops):
                    #print("passengers tapon and tapoff at this stop")
                    #print(stop)
                    #passengers_Atstop = group_bytrip[(group_bytrip['TAG1_TS_NUM'] == stop) | (group_bytrip['TAG2_TS_NUM']==stop)]
                    #print(passengers_Atstop)
                    #print()

                    passengers_Atstop = group_bytrip[(group_bytrip['TAG1_TS_NUM'] == stop) | (group_bytrip['TAG2_TS_NUM']==stop)]
                    # find the first tapoff passenger time
                    df1 = passengers_Atstop[(passengers_Atstop["TAG2_TS_NUM"] == stop)]
                    time1 = list(df1["TAG1_TM"])[0]
                    # find the last tapon passenger time
                    df2 = passengers_Atstop[(passengers_Atstop["TAG1_TS_NUM"] == stop)]
                    time2 = list(df1["TAG2_TM"])[len(list(df1["TAG2_TM"]))-1]

                    dwellTime[stop] = time2 - time1

                #passengers only tapon at this stop
                elif stop in trip_tapon_stops:
                    #print(stop)
                    #print("passengers only tapon at this stop")
                    #passengers_Atstop = group_bytrip[(group_bytrip['TAG1_TS_NUM'] == stop)]
                    #print(passengers_Atstop)
                    #print()

                    passengers_Atstop = group_bytrip[(group_bytrip['TAG1_TS_NUM'] == stop)]
                    # if only one passenger return 0 else return (last tapon time)-(first tapon time)
                    if passengers_Atstop.shape[0] <= 1:
                        dwellTime[stop] = 0
                    else:
                        time1 = list(passengers_Atstop["TAG1_TM"])[0]
                        time2 = list(passengers_Atstop["TAG1_TM"])[len(list(passengers_Atstop["TAG1_TM"]))-1]
                        dwellTime[stop] = time2 - time1


                ##passengers only tapoff at this stop
                else:
                    #print(stop)
                    #print("passengers only tapoff at this stop")
                    #passengers_Atstop = group_bytrip[(group_bytrip['TAG2_TS_NUM'] == stop)]
                    #print(passengers_Atstop)
                    #print()

                    passengers_Atstop = group_bytrip[(group_bytrip['TAG2_TS_NUM'] == stop)]
                    # if only one passenger return 0 else return (last tapoff time)-(first tapoff time)
                    if passengers_Atstop.shape[0] <= 1:
                        dwellTime[stop] = 0
                    else:
                        time1 = list(passengers_Atstop["TAG2_TM"])[0]
                        time2 = list(passengers_Atstop["TAG2_TM"])[len(list(passengers_Atstop["TAG2_TM"]))-1]
                        dwellTime[stop] = time2 - time1

            datapertrip = {"tapon":taponNum_pertrip,"tapoff":tapoffNum_pertrip,"dwellTime":dwellTime}

            dataperday_json[tripnum_perday] = datapertrip


            tripnum_perday+=1

        
        dataperday_json = json.dumps(dataperday_json)
        print(dataperday_json)
        path_json = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusData\\huhao\\"+str(busid)+"-"+str(name_byday)+".json"
        fileObject = open(path_json, 'w')
        fileObject.write(dataperday_json)
        fileObject.close()


        print("----------------------------")



