from celery import shared_task

from time import sleep
from django.core.mail import send_mail
from backend.settings import EMAIL_HOST_USER


@shared_task
def sleep_time(time):
    sleep(time)
    return 'Success'


@shared_task
def send_email_task(user_email):
    send_mail(
        subject='You are subscribed to the newsletter!',
        message='You are subscribed to the newsletter!',
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
        )
    return 'Success'