from celery import shared_task

from time import sleep
from django.core.mail import send_mail
from backend.settings import EMAIL_HOST_USER


@shared_task
def sleep_time(time):
    sleep(time)
    return 'Success'


@shared_task
def send_newsletter_email_task(user_email, subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
        )
    return 'Success'
