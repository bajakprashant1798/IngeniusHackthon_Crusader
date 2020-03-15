import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import math
dataset = pd.read_csv("/content/drive/My Drive/Hackathon_2020/data.csv")

hrw = 0.75 
fs = 100
mov_avg = dataset['hart'].rolling(int(hrw*fs)).mean() #Calculate moving average

avg_hr = (np.mean(dataset.hart))
mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
mov_avg = [x*1.2 for x in mov_avg] 
dataset['hart_rollingmean'] = mov_avg 

window = []
peaklist = []
listpos = 0 
for datapoint in dataset.hart:
    rollingmean = dataset.hart_rollingmean[listpos] 
    if (datapoint < rollingmean) and (len(window) < 1): 
        listpos += 1
    elif (datapoint > rollingmean): 
        window.append(datapoint)
        listpos += 1
    else: 
        maximum = max(window)
        position_top = listpos - len(window) + (window.index(max(window))) 
        peaklist.append(position_top) #Add detected peak to list

        window = []
        listpos += 1
ybeat = [dataset.hart[x] for x in peaklist] 
RR_list = []
cnt = 0
while (cnt < (len(peaklist)-1)):
    RR_interval = (peaklist[cnt+1] - peaklist[cnt]) 
    ms_dist = ((RR_interval / fs) * 1000.0) 
    RR_list.append(ms_dist) 
    cnt += 1
bpm = 60000 / np.mean(RR_list)
print("Average Heart Beat is: %.01f" %bpm)
print(len(dataset))
plt.title("Detected peaks in signal")
#plt.xlim(0,2500)
plt.plot(dataset.hart, alpha=0.5, color='blue') #Plot semi-transparent HR
plt.plot(mov_avg, color ='green') #Plot moving average
plt.scatter(peaklist, ybeat, color='red') #Plot detected peaks
plt.show()
