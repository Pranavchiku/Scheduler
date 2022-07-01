from django.db import models

# Create your models here.
class BackEnd(models.Model):
    start=models.CharField(max_length=200)
    dur=models.CharField(max_length=200)
    timeleft=models.CharField(max_length=200)
    event=models.CharField(max_length=200)

class DiscordServer(models.Model):
    name=models.CharField(max_length=200)
    invitationLink=models.CharField(max_length=400)

class ContactUs(models.Model):
    username=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    description=models.TextField(max_length=500)
