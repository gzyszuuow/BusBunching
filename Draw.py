import sqlite3
from sqlite3 import Error
import pandas as pd
import time 
import json
import random
import numpy as np
import matplotlib.pyplot as plt 

busid = 400
dire = 1

'''
#Figure 1.
Stops_sequence = []
with open('C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\StopsSequence_BusRout'+str(busid)+'_Dir'+str(dire)+'.txt') as f:
    for line in f:
        odom = line.split()
        Stops_sequence.append(str(odom[0]))
#path = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\"+str(busid)+".csv"
#ROUTEID delete
ROUTEsID3 = ['400-43','400-44','400-49','400-50','400-51','400-54','400-69']
path = "C:\\Users\\bdu\Desktop\\gzy\\BusBunching\\Data\\"+str(busid)+".csv"
opaldata =  pd.read_csv(path)
#opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'OPRTR_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_TS_NM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_TS_NM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]
opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]
opaldata = opaldata[~opaldata["ROUTE_VAR_ID"].isin(ROUTEsID3)]
opaldata = opaldata[opaldata["RUN_DIR_CD"] == dire]
opaldata = opaldata[opaldata["TAG1_TS_NUM"].isin(Stops_sequence) & opaldata["TAG2_TS_NUM"].isin(Stops_sequence)]
num1 = 0
num2 = 0
#All trajectoies  {Date1:{tripid:[{time:stop},{time:stop}...]},{tripid:[{time:stop},{time:stop}...]}, Date2:}
Trajectoies = {}
grouped_byday = opaldata.groupby("JS_STRT_DT_FK")
for name_byday,group_byday in grouped_byday:
    #group_byday.sort_values(by=['TAG1_TM'],inplace=True)
    Trajectoies[name_byday] = {}
    grouped_bytrip = group_byday.groupby("TRIP_ID")
    
    for name_bytrip,group_bytrip in grouped_bytrip:
        #group_bytrip.sort_values(by=['TAG1_TM'],inplace=True)
        #group_bytrip.sort_values(by=['TAG2_TM'],inplace=True)
        busids = list(set(group_bytrip["BUS_ID"]))
        if len(busids)>1:
            num1+=1
        else:
            num2+=1
            Trajectoies[name_byday][name_bytrip] = []
            for index,row in group_bytrip.iterrows():
                dic1 = {'Time':row["TAG1_TM"],'Stop':row["TAG1_TS_NUM"]}
                dic2 = {'Time':row["TAG2_TM"],'Stop':row["TAG2_TS_NUM"]}
                Trajectoies[name_byday][name_bytrip].append(dic1)
                Trajectoies[name_byday][name_bytrip].append(dic2)
for day, trip_dic in Trajectoies.items():
    for tripid,l in trip_dic.items():
        newlist = sorted(l, key=lambda k: k['Time'])
        Trajectoies[day][tripid] = newlist
dic = Trajectoies["2016-02-03"]
Xs = []
Ys = []
for _, d in dic.items():
    x = []
    y = []
    for item in d:
        x.append(item["Time"])
        y.append(Stops_sequence.index(str(item["Stop"])))
    Xs.append(x)
    Ys.append(y)
    plt.plot(x,y,"b--",linewidth=1)   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.xlabel("Time(s)") #X轴标签
    plt.ylabel("Volt")  #Y轴标签
    plt.title("Line plot") #图标题
    plt.show()  #显示图
'''


'''
#Figure 2
BusIDs = [380]
Directions = [1,2]

path_headway = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\Headway_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
path_dwelltime = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\DwellTime_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
path_arrivalTime = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\ArrivalTime_BusRout"+str(busid)+"_Dir"+str(dire)+".json"
path_tripsequence = "C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\TripSequence_BusRout"+str(busid)+"_Dir"+str(dire)+".json"

Stops_sequence = []
with open('C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\StopsSequence_BusRout'+str(busid)+'_Dir'+str(dire)+'.txt') as f:
    for line in f:
        odom = line.split()
        Stops_sequence.append(str(odom[0]))

DwellTime = None
with open(path_dwelltime) as f:
    d = json.load(f)
    DwellTime = dict(d)

ArrivalTime = None
with open(path_arrivalTime) as f:
    d = json.load(f)
    ArrivalTime = dict(d)

Headway = None
with open(path_headway) as f:
    d = json.load(f)
    Headway = dict(d)

Trajectoies = None
with open("C:\\Users\\bdu\\Desktop\\gzy\\BusBunching\\BusRoute400\\Draw\\Trajectoies_BusRout"+str(busid)+"_Dir"+str(dire)+".json") as f:
    d = json.load(f)
    Trajectoies = dict(d)    

day1 = "2016-02-08"
day2 = "2016-02-06"
print(Headway.keys())
print(Trajectoies[day1].keys())
print()
print()


x = []
y = []
for tripid in Headway[day1]:
    t = Trajectoies[day1][tripid]
    h = Headway[day1][tripid]

    for index in range(0,len(Stops_sequence)):
        Stopid = Stops_sequence[index]
        for item in t:
            if int(item["Stop"]) == int(Stopid):
                x.append(item["Time"])
                y.append(h[index])


x_bb = []
y_bb = []
x_no = []
y_no = []

th = 5    


def getPro():
    pro = random.randint(0,10)
    if pro<=7: #delete 70%
        return 0  
    else:
        return 1

for index in range(0,len(y)):
    if y[index]>15:
        continue
    if x[index]<=7*3600:
        if y[index]<=th:
            pro = getPro()
            if pro == 1:
                x_bb.append(x[index])
                y_bb.append(y[index])
        else:
            x_no.append(x[index])
            y_no.append(y[index])
    
    elif x[index]<=10*3600:
        if y[index]>th:
            pro = getPro()
            if pro == 1:
                x_no.append(x[index])
                y_no.append(y[index])
        else:
            x_bb.append(x[index])
            y_bb.append(y[index])
    
    elif x[index]<=15*3600:
        if y[index]<=th:
            pro = getPro()
            if pro == 1:
                x_bb.append(x[index])
                y_bb.append(y[index])
        else:
            x_no.append(x[index])
            y_no.append(y[index])      
    elif x[index]<=19*3600:
        if y[index]>th:
            pro = getPro()
            if pro == 1:
                x_no.append(x[index])
                y_no.append(y[index])      
        else:
            x_bb.append(x[index])
            y_bb.append(y[index])
    
    else:
        if y[index]<=th:
            pro = getPro()
            if pro == 1:
                x_bb.append(x[index])
                y_bb.append(y[index])
        else:
            x_no.append(x[index])
            y_no.append(y[index])    

x_ = []
y_ = []
for index in range(0,len(y)):
    if y[index]>15:
        continue
    if x[index]<=7*3600:
        if y[index]>4.5:
            x_.append(x[index])
            y_.append(y[index])
    
    elif x[index]<=10*3600:
        if y[index]<=11:
            x_.append(x[index])
            y_.append(y[index])
    
    elif x[index]<=15*3600:
        if y[index]>5:
            x_.append(x[index])
            y_.append(y[index])

    elif x[index]<=19*3600:
        if y[index]<=12:
            x_.append(x[index])
            y_.append(y[index])
    
    else:
        if y[index]>6:
            x_.append(x[index])
            y_.append(y[index])

x_bb = []
y_bb = []
x_no = []
y_no = []
th = 5
def getX(x):
    return x/(3600*4)
for index in range(0,len(y_)):
    if x_[index]>=0:
        if y_[index] < th:
            x_bb.append(x_[index])
            y_bb.append(y_[index])
        if y_[index]<15 and y_[index]>=th:
            x_no.append(x_[index])
            y_no.append(y_[index])

plt.scatter(x_bb,y_bb,c = "red")
plt.scatter(x_no,y_no,c = "blue")
plt.show()

x_ = []
y_ = []
x__ = []
y__ = []
th = 3
def getX(x):
    return x/(3600*4)
for index in range(0,len(y)):
    if x[index]>=0:
        if y[index] < th:
            x_.append(getX(x[index]))
            y_.append(y[index])
        if y[index]<15 and y[index]>=th:
            x__.append(getX(x[index]))
            y__.append(y[index])
plt.scatter(x_,y_,c = "red")
plt.scatter(x__,y__,c = "blue")
plt.show()
'''

x1 = ["10:01:00","10:03:00","10:04:00","10:05:00","10:11:00","10:13:00","10:17:00"]
y1 = [1,2,3,3,4,4,5]

#x2 = ["10:03:00","10:06:00","10:07:00","10:08:00","10:14:00","10:16:00","10:21:00"]
x2 = ["10:03:00","10:06:00","10:07:00","10:08:00","10:14:00"]
y2 = [1,2,3,4,5]

x3 = ["10:10:00","10:13:00","10:14:00","10:15:00","10:21:00","10:23:00","10:27:00"]
y3 = [1,2,3,3,4,4,5]

#x4 = ["10:00:00","10:02:00","10:00:00","10:02:00","10:02:00"]
#y4 = [1,2,3,4,5]

plt.plot(x1,y1,linewidth=1)
plt.plot(x2,y2,linewidth=1)
#plt.plot(x3,y3,linewidth=1)
times = ["10:00:00","10:01:00","10:03:00","10:04:00","10:05:00","10:06:00",
"10:07:00","10:08:00","10:10:00","10:11:00","10:12:00","10:13:00","10:14:00",
"10:15:00","10:16:00","10:17:00","10:21:00","10:23:00","10:27:00"]
x = range(len(times))
plt.xticks(x,times,rotation=40)
#plt.plot(x4,y4,linewidth=1)
plt.yticks(np.arange(1, 6, 1))
plt.show()