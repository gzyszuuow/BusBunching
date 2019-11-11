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

import numpy as np  
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#path = "C:\\Users\\zg148\\Desktop\\gzy\\BusBunching\\BusData\\2016-02-01.csv"
busid = 400
path = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\"+str(busid)+".csv"
opaldata =  pd.read_csv(path)

#drop the outliers
#opaldata = opaldata[~opaldata["TAG1_TS_NUM"].isin(["-1"])]
#opaldata = opaldata[~opaldata["TAG2_TS_NUM"].isin(["-1"])]

opaldata = opaldata[['ROUTE_ID', 'ROUTE_VAR_ID','BUS_ID', 'OPRTR_ID', 'RUN_DIR_CD', 'TRIP_ID', 'JS_STRT_DT_FK','TAG1_TM', 'TAG1_TS_NUM', 'TAG1_TS_NM', 'TAG1_LAT_VAL', 'TAG1_LONG_VAL','TAG2_TM', 'TAG2_TS_NUM', 'TAG2_TS_NM', 'TAG2_LAT_VAL','TAG2_LONG_VAL']]



'''
#the sequence of stops
StopsSequence = []
StopsTimeEachtrip = {}
opaldata = opaldata[["ROUTE_ID", 'ROUTE_VAR_ID','BUS_ID', "TRIP_ID","JS_STRT_DT_FK","TAG1_TM","TAG1_TS_NUM","TAG2_TM","TAG2_TS_NUM"]]
#opaldata = opaldata.head(1000)
grouped_byday = opaldata.groupby("JS_STRT_DT_FK")
num = 0
for name_byday,group_byday in grouped_byday:

    #group_byday.sort_values(by=['TAG1_TM'],inplace=True)
    grouped_bytrip = group_byday.groupby("TRIP_ID")

    for name_bytrip,group_bytrip in grouped_bytrip:
        StopsTimeEachtrip[num] = {}

        for index,row in group_bytrip.iterrows():
            tapontime = row["TAG1_TM"]
            tapoftime = row["TAG2_TM"]
            taponstop = row["TAG1_TS_NUM"]
            tapoffstop = row["TAG2_TS_NUM"]

            StopsTimeEachtrip[num][tapontime] = taponstop
            StopsTimeEachtrip[num][tapoftime] = tapoffstop
        num+=1

StopsTimeEachtrip_sorted = {}
#print(StopsTimeEachtrip)
for i,j in StopsTimeEachtrip.items():
    j_ = dict(sorted(j.items()))
    StopsTimeEachtrip_sorted[i] = j_


StopsTimeEachtrip_json = json.dumps(StopsTimeEachtrip_sorted)
path_json = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\StopsTimeEachtrip.json"
fileObject = open(path_json, 'w')
fileObject.write(StopsTimeEachtrip_json)
fileObject.close()
'''


'''
path  = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\StopsTimeEachtrip.json"

StopsTimeEachtrip = None
with open(path) as f:
    d = json.load(f)
    StopsTimeEachtrip = dict(d)

NumStopsofEachTrip = {}
for num, dic in StopsTimeEachtrip.items():
    NumStopsofEachTrip[int(num)] = len(dic.keys())

#print(NumStopsofEachTrip)
print(sum(NumStopsofEachTrip.values()))
print(len(NumStopsofEachTrip))
print(sum(NumStopsofEachTrip.values())/len(NumStopsofEachTrip))
print(max(NumStopsofEachTrip.values()))
print(min(NumStopsofEachTrip.values()))
'''

#trip -> gif


'''
fig = plt.figure()
def f(x, y):
    return np.sin(x) + np.cos(y)

x = np.linspace(0, 2 * np.pi, 120)
y = np.linspace(0, 2 * np.pi, 100).reshape(-1, 1)
# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are just animating one artist, the image, in
# each frame
ims = []
#for i in range(60):
for i in range(2):
    x += np.pi / 15.
    y += np.pi / 20.
    print(type(f(x,y)))
    print(f(x,y).shape)
    print()
    im = plt.imshow(f(x, y), animated=True)
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)

# ani.save('dynamic_images.mp4')

plt.show()
'''



import imageio
outfilename = "my.gif" # 转化的GIF图片名称
filenames = []
for i in range(39,43):
    filename = "C:\\Users\\zg148\\Desktop\\BusBunching\\Data\\400-"+str(i)+".png"
    filenames.append(filename)
frames = []
for image_name in filenames:
    im = imageio.imread(image_name)
    frames.append(im)

print(type(imageio.mimsave(outfilename, frames, 'GIF', duration=1)))

'''
import imageio
 
def create_gif(image_list, gif_name):
 
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    # Save them as frames into a gif 
    imageio.mimsave(gif_name, frames, 'GIF', duration = 0.1)
 
    return
 
def main():
    image_list = ['test_gif-0.png', 'test_gif-2.png', 'test_gif-4.png', 
                  'test_gif-6.png', 'test_gif-8.png', 'test_gif-10.png']
    gif_name = 'created_gif.gif'
    create_gif(image_list, gif_name)
'''

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
    

plt.subplot(121)
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

plt.subplot(122)
plt.scatter(PartXsMoreThreshold, PartYsMoreThreshold, alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
#plt.title("MoreThresold: "+str(len(PartStopIDsMoreThreshold))+" stops")
plt.title("Selected stops")
plt.xlim(xmin = 151.075,xmax = 151.30)
plt.ylim(ymin = -33.985 ,ymax = -33.84)

plt.show()

print(len(Xs))
print(len(PartXsMoreThreshold))
'''
