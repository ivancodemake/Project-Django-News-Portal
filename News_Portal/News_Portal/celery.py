import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Portal.settings')


app = Celery('News_Portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.enable_utc = False
app.conf.timezone = "Asia/Almaty"

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'spam_weekly': {
        'task': 'News.tasks.weekly_sends',
        'schedule': crontab(hour='8', minute='0', day_of_week='monday')
    },
}




