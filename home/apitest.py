import json
import requests
from datetime import *
import time
from home.tasks import api_request

def request_api():
    resp=requests.get("https://codeforces.com/api/contest.list").json()

    resp2=requests.get("https://kontests.net/api/v1/all").json()
    return [resp,resp2]

def bubbleSort(arr,duration,event,start_time):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
                duration[j], duration[j+1] = duration[j+1], duration[j]
                event[j], event[j+1] = event[j+1], event[j]
                start_time[j], start_time[j+1] = start_time[j+1], start_time[j]
                # temp[j], temp[j+1] = temp[j+1], temp[j]


def solve():
    # resp=request_api()[0]
    # resp2=request_api()[1]

    resp=api_request()[0]
    resp2=api_request()[1]


    start_time=[]
    duration=[]
    timeLeft=[]
    event=[]
    temp=[]
    # print(resp['result'])
    for i in range(len(resp["result"])):
        event.append(str(resp["result"][i]["name"]))
    #start time
    for i in range(len(resp["result"])):
        # start_time.append(str(datetime.fromtimestamp(resp["result"][i]["startTimeSeconds"]).strftime(" %d, %Y %I:%M:%S")))
        start_time.append(((resp["result"][i]["startTimeSeconds"]))+19800)
        # print(start_time[i])
        # temp.append(start_time[i])


    #duration
    for i in range(len(resp["result"])):
        # duration.append(str(timedelta(seconds=resp["result"][i]["durationSeconds"])))
        duration.append(resp["result"][i]["durationSeconds"])

    #timeLeft
    for i in range(len(resp["result"])):
        # then=datetime.fromtimestamp(resp["result"][i]["startTimeSeconds"])
        # now=datetime.now()
        then=resp["result"][i]["startTimeSeconds"]+19800
        now1=datetime.now()
        n=datetime.timestamp(now1)
        timeLeft.append((then-n))


    #Rest all
    for i in range(len(resp2)):
        d = datetime.fromisoformat(resp2[i]["start_time"][:19])+timedelta(0, 19800)
        d.strftime('%B %d, %Y %I:%M:%S')
        # print(d)
        # print(d.timestamp())
        
        start_time.append((d.timestamp()))
        # print(start_time[i])
        # temp.append(start_time[i])
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
    # temp=temp[i:]

    for i in range(len(timeLeft)):
        temp.append(int(timeLeft[i]))
        timeLeft[i]=((timedelta(seconds=timeLeft[i])))
        duration[i]=((timedelta(seconds=duration[i])))
        start_time[i]=datetime.fromtimestamp(start_time[i]).strftime("%B %d, %Y %I:%M:%S")

    return([temp,timeLeft,duration,start_time,event])

h=solve()
temp=h[0]
timeLeft=h[1]
duration=h[2]
start_time=h[3]
event=h[4]