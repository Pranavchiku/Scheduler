from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from scheduler import settings
from home import apitest
import requests
from datetime import *
from django.shortcuts import render,HttpResponse,redirect

@shared_task(bind=True)
def test_func(self):
    #operations
    for i in range(10):
        print(i)
    return "Done"


@shared_task(bind=True)
def send_mail_func(self):
    users=get_user_model().objects.all()
    for user in users:
        mail_subject="Hi! Celery Testing"
        message="Celery Testing is in progress, lets hope it works"
        to_email=user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return "Done"

@shared_task(bind=True)
def api_request(self):
    resp=requests.get("https://codeforces.com/api/contest.list").json()
    resp2=requests.get("https://kontests.net/api/v1/all").json()

    return [resp,resp2]

@shared_task(bind=True)
def full_apitest(self):
    resp=requests.get("https://codeforces.com/api/contest.list").json()
    resp2=requests.get("https://kontests.net/api/v1/all").json()

    start_time=[]
    duration=[]
    timeLeft=[]
    event=[]
    temp=[]
    urL=[]
    # print(resp['result'])
    for i in range(len(resp["result"])):
        event.append(str(resp["result"][i]["name"]))
        urL.append("https://codeforces.com/contests")
    #start time
    for i in range(len(resp["result"])):
        # start_time.append(str(datetime.fromtimestamp(resp["result"][i]["startTimeSeconds"]).strftime(" %d, %Y %I:%M:%S")))
        start_time.append(((resp["result"][i]["startTimeSeconds"])))
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
        then=resp["result"][i]["startTimeSeconds"]
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
        urL.append(resp2[i]["url"])


    n = len(timeLeft)
    for i in range(n):
        for j in range(0, n-i-1):
            if timeLeft[j] > timeLeft[j+1] :
                timeLeft[j], timeLeft[j+1] = timeLeft[j+1], timeLeft[j]
                duration[j], duration[j+1] = duration[j+1], duration[j]
                event[j], event[j+1] = event[j+1], event[j]
                start_time[j], start_time[j+1] = start_time[j+1], start_time[j]
                urL[j], urL[j+1] = urL[j+1], urL[j]
    i=0
    while(timeLeft[i]<0): i=i+1

    timeLeft=timeLeft[i:]
    duration=duration[i:]
    event=event[i:]
    start_time=start_time[i:]
    urL=urL[i:]
    # temp=temp[i:]

    for i in range(len(timeLeft)):
        temp.append(int(timeLeft[i]))
        timeLeft[i]=((timedelta(seconds=timeLeft[i])))
        duration[i]=((timedelta(seconds=duration[i])))
        start_time[i]=datetime.fromtimestamp(start_time[i]).strftime("%B %d, %Y %I:%M:%S")

    return ([temp,timeLeft,duration,start_time,event,urL])

@shared_task(bind=True)
def send_mail_reminder(self):
    h=full_apitest()
    temp=h[0]
    event=h[4]
    
    i=0
    mail_event=[]

    while(temp[i]<=3600 and temp[i]>=3580):
        mail_event.append(event[i])
        i=i+1
    
    users=get_user_model().objects.all()
    for a in range(len(mail_event)):
        for user in users:
            mail_subject="hey! Reminder for Contest"
            message="Hey " + user.username + "\n"+ "Here is the gentle reminder for " + mail_event[a] + " starts after an hour, Happy Coding!!"+"\n"+"PranavChiku-Admin " +"\n"+"Scheduler" 
            to_email=user.email
            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True,
            )
    return "done"

@shared_task(bind=True)
def send_mail_reminder_final(self):
    h=full_apitest()
    temp=h[0]
    event=h[4]
    urL=h[5]
    i=0
    mail_event=[] 

    while(temp[i]<=20 and temp[i]>=00):
        mail_event.append(event[i])
        i=i+1
    
    users=get_user_model().objects.all()
    for a in range(len(mail_event)):
        
        for user in users:
            mail_subject="Scheduler Reminder"
            message="Hey " + user.username + " " + mail_event[a] + " has started."+"\n"+"Link for the same attached \n"+urL[a]+"\n"+"Best Of Luck!! Happy Coding!!"+"\n"+"PranavChiku-Admin " +"\n"+"Scheduler" 
            to_email=user.email
            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True,
            )
        
        #v6
        payload={
            'content': "Hey @everyone " + mail_event[a] + " has started."+"\n"+"Link for the same attached \n"+urL[a]+"\n"+"Best Of Luck!! Happy Coding!!"+"\n"+"PranavChiku-Admin " +"\n"+"Scheduler"
        }

        header={
                "authorization": "NzYwNTEwOTg2NTQ4ODA1NjQy.YK5FNw.fMYRaL228PKlLwF_T9A9Am4fTp4 "
        }

        r=requests.post("https://discord.com/api/v9/channels/806880311769563170/messages",data=payload,headers=header)

        #gregor
        payload2={
            'content': "Hey @everyone " + mail_event[a] + " has started."+"\n"+"Link for the same attached \n"+urL[a]+"\n"+"Best Of Luck!! Happy Coding!!"+"\n"+"PranavChiku-Admin " +"\n"+"Scheduler"
        }

        header2={
                "authorization": "NzYwNTEwOTg2NTQ4ODA1NjQy.YK5FNw.fMYRaL228PKlLwF_T9A9Am4fTp4 "
        }

        r2=requests.post("https://discord.com/api/v9/channels/840602917429313537/messages",data=payload2,headers=header2)
    return redirect("home")

