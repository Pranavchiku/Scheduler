import json
import requests
from datetime import *
import time

def bubbleSort(arr,duration,event,start_time):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
                duration[j], duration[j+1] = duration[j+1], duration[j]
                event[j], event[j+1] = event[j+1], event[j]
                start_time[j], start_time[j+1] = start_time[j+1], start_time[j]

resp2=requests.get("https://kontests.net/api/v1/kick_start").json()

start_time=[]
duration=[]
timeLeft=[]
event=[]

for i in range(len(resp2)):
    d = datetime.fromisoformat(resp2[i]["start_time"][:-1])
    d.strftime('%Y-%m-%d %H:%M:%S')
    start_time.append((d.timestamp()))
    # x=(timedelta(seconds=int(float(resp2[i]["duration"]))))
    duration.append(int(float(resp2[i]["duration"])))
    then=d.timestamp()
    now1=datetime.now()
    n=datetime.timestamp(now1)
    timeLeft.append(then-n)
    event.append(resp2[i]["name"])

bubbleSort(timeLeft,duration,event,start_time)
i=0
while(timeLeft[i]<0): i=i+1

timeLeft=timeLeft[i:]
duration=duration[i:]
event=event[i:]
start_time=start_time[i:]

for i in range(len(timeLeft)):
    timeLeft[i]=((timedelta(seconds=timeLeft[i])))
    duration[i]=((timedelta(seconds=duration[i])))
    start_time[i]=datetime.fromtimestamp(start_time[i])

