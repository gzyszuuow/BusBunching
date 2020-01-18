import sqlite3
#from sqlite3 import Error
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

'''
#Figure 1
x1 = [1,2,3,4,5,6,7,8,8.5]
y1 = [1,2,2,3,3,4,4,5,5]


x2 = [6,7,8,9,10,11,12,13,13.5]
y2 = [1,2,2,3,3,4,4,5,5]

x3 = [10,10.5,11,11.5,12.5,13,14,15.5,16]
y3 = [1,2,2,3,3,4,4,5,5]
#plt.plot(x2,y2,linewidth=2)
x4 = [12,12.5,13,13.5,14,14.5,15,15.5,16]
y4 = [1,2,2,3,3,4,4,5,5]

x = [x1,x2,x3,x4]
y = [y1,y2,y3,y4]
for index in range(0,len(x)):
    if index == 2:
        l1 = plt.plot(x[index],y[index],color = "red",label = "Bunched Trips",linewidth = 3)
    elif index == 3:
        l1 = plt.plot(x[index],y[index],color = "red",linewidth = 3)
    elif index == 1:
        l2 = plt.plot(x[index],y[index],color = "blue",label = "Normal Trips",linewidth = 3)
    else:
        l2 = plt.plot(x[index],y[index],color = "blue",linewidth = 3)

#plt.scatter(15.5,5,marker = "X",c = "red",s = 200)
plt.yticks(np.arange(1, 6, 1))
plt.xlabel('Time',fontsize = 20,alpha = 3.0)
plt.ylabel('Stop Number',fontsize = 20,alpha = 3.0)
ax = plt.gca() # grab the current axis

plt.scatter(4,3,color = "blue",s = 200,marker = "X")
plt.scatter(5,3,color = "blue",s = 200,marker = "X")
plt.scatter(6,4,color = "blue",s = 200,marker = "X")
plt.scatter(11,4,color = "blue",s = 200,marker = "X")


ax.set_xticks([2,4,6,8,10,12,14]) # choose which x locations to have ticks 
ax.set_xticklabels(["10:01:00","10:03:00","10:04:00","10:05:00","10:06:00","10:07:00","10:08:00"],rotation=20,fontsize = 15)
plt.legend(loc='best',prop = {'size':15})

plt.show()
'''




'''
#evaluation
x1 = [1,2,3,4]

rmse_our_400 =   [0.09880,0.09425,0.09775,0.09186]
rmse_seq_400 =   [0.10368,0.09834,0.10177,0.09392]
rmse_gru_400 =   [0.10875,0.10537,0.10759,0.10366]
rmse_dnn_400 =   [0.15708,0.14804,0.15407,0.14153]
rmse_arima_400 = [0.18319,0.17419,0.17867,0.16599]
#rmse_avg_400 =   [0.28731,0.24892,0.27319,0.24345]

plt.subplot(121)
plt.plot(x1,rmse_our_400,"--",marker = "o",color = "blue",linewidth = 3)
plt.plot(x1,rmse_seq_400,"--",marker = "o",color = "red",linewidth = 3)
plt.plot(x1,rmse_gru_400,"--",marker = "o",color = "green",linewidth = 3)
plt.plot(x1,rmse_dnn_400,"--",marker = "o",color = "gray",linewidth = 3)
plt.plot(x1,rmse_arima_400,"--",marker = "o",color = "black",linewidth = 3)
#plt.plot(x1,rmse_avg_400,"--",marker = "o",color = "black",linewidth = 3)
plt.title("Bus 400",fontsize = 20,alpha = 3.0)
plt.xlabel('Time',alpha = 3.0)
plt.ylabel('RMSE',fontsize = 20,alpha = 3.0)
plt.ylim(0.06,0.185)
ax = plt.gca()
ax.set_xticks([1,2,3,4]) 
ax.set_xticklabels(["A.M. Peak","Daytime Inter-peak","P.M Peak","Night Inter-peak"],rotation=15,fontsize = 18)
#plt.legend(labels=['BB-seq2seq','GRU','DNN',"ARIMA","Avg"],  loc='best',fontsize = 15)

rmse_our_380 =   [0.06773,0.06397,0.06977,0.06681]
rmse_seq_380 =   [0.06992,0.06543,0.07234,0.06762]  
rmse_gru_380 =   [0.08411,0.08133,0.08146,0.08114]
rmse_dnn_380 =   [0.11647,0.11233,0.11826,0.11318]
rmse_arima_380 = [0.14734,0.13339,0.13916,0.13112]
#rmse_avg_380 =   [0.24820,0.22197,0.25835,0.23913]

plt.subplot(122)
plt.plot(x1,rmse_our_380,"--",marker = "o",color = "blue",linewidth = 3)
plt.plot(x1,rmse_seq_380,"--",marker = "o",color = "red",linewidth = 3)
plt.plot(x1,rmse_gru_380,"--",marker = "o",color = "green",linewidth = 3)
plt.plot(x1,rmse_dnn_380,"--",marker = "o",color = "gray",linewidth = 3)
plt.plot(x1,rmse_arima_380,"--",marker = "o",color = "black",linewidth = 3)
#plt.plot(x1,rmse_avg_380,"--",marker = "o",color = "black",linewidth = 3)
plt.title("Bus 380",fontsize = 20,alpha = 3.0)
plt.xlabel('Time',alpha = 3.0)
plt.ylabel('RMSE',fontsize = 20,alpha = 3.0)
ax = plt.gca()
ax.set_xticks([1,2,3,4]) 
ax.set_xticklabels(["A.M. Peak","Daytime Inter-peak","P.M Peak","Night Inter-peak"],rotation=15,fontsize = 18)
plt.legend(labels=['SD-seq2seq','seq2seq','GRU','DNN',"ARIMA"],  loc='best',fontsize = 15)

plt.ylim(0.06,0.185)

plt.show()
'''


rmse_our_400 =    [0.09880,0.09425,0.09775,0.09186]
rmse_demand_400 = [0.10970,0.10251,0.10746,0.10198] #
rmse_supply_400 = [0.12208,0.11025,0.12081,0.11650]
rmse_no_400 =     [0.14676,0.14188,0.14436,0.13655]

rmse_our_380 =    [0.06773,0.06397,0.06977,0.06681]
rmse_demand_380 = [0.07932,0.07334,0.07970,0.07783] #
rmse_supply_380 = [0.09982,0.09332,0.09890,0.09466]
rmse_no_380 =     [0.11249,0.11220,0.11246,0.11239]


x1 = [1,2,3,4]
plt.subplot(121)
plt.plot(x1,rmse_our_400,"--",marker = "o",color = "blue",linewidth = 3)
plt.plot(x1,rmse_demand_400,"--",marker = "o",color = "green",linewidth = 3)
plt.plot(x1,rmse_supply_400,"--",marker = "o",color = "red",linewidth = 3)
plt.plot(x1,rmse_no_400,"--",marker = "o",color = "black",linewidth = 3)
plt.title("Bus 400",fontsize = 20,alpha = 3.0)
plt.xlabel('Time',alpha = 3.0)
plt.ylabel('RMSE',fontsize = 20,alpha = 3.0)
plt.ylim(0.06,0.15)
ax = plt.gca()
ax.set_xticks([1,2,3,4]) 
ax.set_xticklabels(["A.M. Peak","Daytime Inter-peak","P.M Peak","Night Inter-peak"],rotation=15,fontsize = 18)
plt.legend(labels=['All Features','Demand Only','Supply Only',"Headway Only"],  loc='best',fontsize = 15)

plt.subplot(122)
plt.plot(x1,rmse_our_380,"--",marker = "o",color = "blue",linewidth = 3)
plt.plot(x1,rmse_demand_380,"--",marker = "o",color = "green",linewidth = 3)
plt.plot(x1,rmse_supply_380,"--",marker = "o",color = "red",linewidth = 3)
plt.plot(x1,rmse_no_380,"--",marker = "o",color = "black",linewidth = 3)
plt.title("Bus 380",fontsize = 20,alpha = 3.0)
plt.xlabel('Time',alpha = 3.0)
plt.ylabel('RMSE',fontsize = 20,alpha = 3.0)
plt.ylim(0.06,0.15)
ax = plt.gca()
ax.set_xticks([1,2,3,4]) 
ax.set_xticklabels(["A.M. Peak","Daytime Inter-peak","P.M Peak","Night Inter-peak"],rotation=15,fontsize = 18)
plt.legend(labels=['All Features','Demand Only','Supply Only',"Headway Only"],  loc='best',fontsize = 15)
plt.show()



'''
# Transfrom png to PDF
import glob
import fitz
import os

def pic2pdf():
    doc = fitz.open()
    for img in sorted(glob.glob("pic2pdf/*")):  # 读取图片，确保按文件名排序
        print(img)
        imgdoc = fitz.open(img)                 # 打开图片
        pdfbytes = imgdoc.convertToPDF()        # 使用图片创建单页的 PDF
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)                   # 将当前页插入文档
    if os.path.exists("allimages.pdf"):
        os.remove("allimages.pdf")
    doc.save("allimages.pdf")                   # 保存pdf文件
    doc.close()

if __name__ == '__main__':
    pic2pdf()
'''