from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from backend.settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model
from send_email.models import Contact

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
        for contact in Contact.objects.all():
            send_mail(
                subject='Periodic message!',
                message='This message is sent periodically. '
                        'If you do not want to receive the newsletter, '
                        'unsubscribe from the newsletter.',
                from_email=EMAIL_HOST_USER,
                recipient_list=[contact.subscribed_mail],
                fail_silently=False,
            )
        return 'Success'
    except Exception:
        return 'Error'


@shared_task
def send_with_attachment_task(user_email, subject, message, file_path):
    try:
        email = EmailMessage(
            subject,
            message,
            EMAIL_HOST_USER,
            [user_email]
        )
        email.attach_file(file_path)
        email.send(fail_silently=False,)
        return 'Success'
    except Exception:
        return 'Error'
