from celery import shared_task

from time import sleep
from django.core.mail import send_mail
from backend.settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model
User = get_user_model()


@shared_task
def send_newsletter_email_task(user_email, subject, message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,
            )
        return 'Success'
    except Exception:
        return 'Error'


@shared_task
def send_beat_email_task():
    try:
        users = User.objects.filter(user_contact__subscribed_mail=True)
        for user in users:
            send_mail(
                subject='Periodic message!',
                message='This message is sent periodically. '
                        'If you do not want to receive the newsletter, '
                        'unsubscribe from the newsletter.',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
        return 'Success'
    except Exception:
        return 'Error'
