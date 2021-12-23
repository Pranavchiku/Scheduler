from django.http import response
from django.shortcuts import render,HttpResponse,redirect
from datetime import *
from django.contrib.auth.models import User
from django.contrib.auth import logout,login
from django.contrib.auth import authenticate
from django.contrib import messages
import requests
from home.models import *
from home import apitest
import time
import schedule
import threading
from home.tasks import test_func,send_mail_func,full_apitest
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
import threading

class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

# Create your views here.
def index(request):
    h=full_apitest()
    temp=h[0]
    start_time=h[3]
    event=h[4]
    duration=h[2]
    timeleft=h[1]

    for i in range(len(event)):
        al=BackEnd.objects.all()
        if(event[i] not in al):
            x=BackEnd(start=str(start_time[i]),dur=str(duration[i]),timeleft=str(temp[i]),event=str(event[i]))
            x.save()

    final=[start_time,event,duration,timeleft]
    return render(request,"index.html",{"final":final,"variable":datetime.today(),"start_time":start_time,"event":event,"duration":duration,"timeleft":timeleft,"temp":temp})

def about(request):
    context={
        "variable":datetime.today()
    }
    return render(request,"about.html",context)

def loginPage(request):
    return render(request,"login.html")

def loginUser(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            return render(request,"login.html")
    else:
        return render(request,"login.html")

def logoutUser(request):
    logout(request)
    return redirect("/login")

def contacts(request):
    return render(request,"contacts.html")

def search(request):
    que=request.GET["query"]
    all=BackEnd.objects.filter(event__contains=que)
    return render(request,"search.html",{"all":all})


def signup(request):
    return render(request,"signup.html")
    
def handlesignup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if(pass1==pass2):
            #create the user


            myuser=User.objects.create_user(username=username,email=email,password=pass1)
            myuser.is_active=False
            myuser.save()

            current_site=get_current_site(request)
            email_subject="Activate your account"
            message=render_to_string('activate.html',
            {
                'user':myuser,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token':generate_token.make_token(myuser)
            }
            )
            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
            )
            EmailThread(email_message).start()
            messages.add_message(request, messages.SUCCESS,
                             'Check Your Mail to Activate your acount and then refresh')

            return redirect('home')
            # myuser.save()
            # messages.success(request,"Your account has been successfully created!")
            # return redirect("home")
        else:
            messages.error(request,"Password Not Matched")
            return redirect("signup")
    else:
        return HttpResponse("404- Not Found")

def send_ma(request):
    send_mail_func.delay()
    return HttpResponse("Sent response")

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.add_message(request,messages.INFO,"account activated succesfully")
            return redirect("home")
        return HttpResponse("Failed to verify")

def resources(request):
    return render(request,"resources.html")

def discordLink(request):
    if request.method=="POST":
        servername=request.POST['user/servername']
        link=request.POST['link']
        newserver=DiscordServer(name=servername,invitationLink=link)
        newserver.save()
        messages.add_message(request,messages.INFO,"Link submitted successfully, You may return to home page")
        return render(request,"resources.html")

def handleContacts(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        desc=request.POST['desc']
        newserver=ContactUs(username=username,email=email,description=desc)
        newserver.save()
        messages.add_message(request,messages.INFO,"Query submitted successfully, You may return to home page")
        return render(request,"contacts.html")