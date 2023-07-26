import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'send-spam-every-month': {
        'task': 'send_email.tasks.send_beat_email',
        'schedule': crontab(0, 0, day_of_month='2')
    }
}

app.conf.beat_schedule = {
    'send-spam-every-minute': {
        'task': 'send_email.tasks.send_beat_email_task',
        'schedule': crontab(minute='*/1')
    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
