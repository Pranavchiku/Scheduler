from __future__ import absolute_import,unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','scheduler.settings')

app=Celery('scheduler')
app.conf.enable_utc=False

app.conf.update(timezone='Asia/kolkata',
)

# app.config_from_object('settings', namespace='CELERY')
app.config_from_object(settings, namespace='CELERY')

# celery beat settings
app.conf.beat_schedule={
    'send-mail-every-day-at-8':{
        'task':'home.tasks.send_mail_func',
        'schedule':crontab(hour=23, minute=48), #24 hours format
        # 'args':(2)
    },
    'send-api-request':{
        'task':'home.tasks.full_apitest',
        'schedule':1
    },
    'send-reminder-mail':{
        'task':'home.tasks.send_mail_reminder',
        'schedule':1
    },
    'send-reminder-mail-final':{
        'task':'home.tasks.send_mail_reminder_final',
        'schedule':1
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')