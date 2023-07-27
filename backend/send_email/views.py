from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import render_to_string
from django.conf import settings

from .forms import SendEmailForm, SendReviewForm
from .models import Contact
from .tasks import (
    send_newsletter_email_task,
    send_with_attachment_task,
)


@login_required
def send_subscription_email(request):
    try:
        if not Contact.objects.filter(user=request.user).exists():
            # contact_user = Contact.objects.filter(user=request.user, subscribed_mail=False).get()
            subject = 'You are subscribed to the newsletter!'
            message = 'You have subscribed to the newsletter!'
            send_newsletter_email_task.delay(request.user.email, subject, message)
            # contact_user.subscribed_mail = True
            contact_user = Contact()
            contact_user.user = request.user
            contact_user.subscribed_mail = request.user.email
            contact_user.save()
            response = 'You have subscribed to the newsletter!'
            return render(request, 'user/response.html', {'response': response})
        else:
            response = 'You already subscribed to the newsletter!'
            return render(request, 'user/response.html', {'response': response})
    except Exception:
        response = 'Error!'
        template = render(request, 'user/response.html', {'response': response})
        template.status_code = 404
        return template


@login_required
def send_unsubscribe_email(request):
    try:
        if Contact.objects.filter(user=request.user).exists():
            contact_user = Contact.objects.filter(user=request.user).get()
            subject = 'You have unsubscribed from the newsletter!'
            message = 'You have unsubscribed from the newsletter!'
            send_newsletter_email_task.delay(request.user.email, subject, message)
            contact_user.delete()
            response = 'You have unsubscribed from the newsletter!'
            return render(request, 'user/response.html', {'response': response})
        elif Contact.objects.filter(user=request.user, subscribed_mail=False).exists():
            response = 'You are not subscribed to the newsletter!'
            return render(request, 'user/response.html', {'response': response})
        else:
            response = 'Error! Re-log in.'
            template = render(request, 'user/response.html', {'response': response})
            template.status_code = 404
            return template
    except Exception:
        response = 'Error!'
        template = render(request, 'user/response.html', {'response': response})
        template.status_code = 404
        return template


@login_required
def send_one_email(request):
    try:
        subject = 'We sent you one email!'
        message = 'Message description...'
        send_newsletter_email_task.delay(request.user.email, subject, message)
        response = 'We sent you one email!'
        return render(request, 'user/response.html', {'response': response})
    except Exception:
        response = 'Error!'
        template = render(request, 'user/response.html', {'response': response})
        template.status_code = 404
        return template


def send_email_form(request):
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            send_newsletter_email_task.delay(
                request.user.email,
                form.cleaned_data["title"],
                form.cleaned_data["message"],
            )
            response = 'Thanks. You sent an email!'
            return render(request, 'user/response.html', {'response': response})
    else:
        form = SendEmailForm()
    return render(request, 'send_email/send_email_form.html', {'form': form})


def send_review_form(request):
    if request.method == 'POST':
        form = SendReviewForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['title']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            context = {
                'email': email,
                'message': message,
            }
            message = render_to_string('send_email/email_message.txt', context)
            send_newsletter_email_task.delay(email, subject, message)
            response = 'Thanks. You sent an email!'
            return render(request, 'user/response.html', {'response': response})
    else:
        form = SendReviewForm()
    return render(request, 'send_email/send_review_form.html', {'form': form})


def send_with_attachment(request):
    try:
        subject = 'Email with attachment'
        message = 'Description'
        file_path = f'{settings.MEDIA_ROOT}/email/file_for_email.txt'
        send_with_attachment_task.delay(request.user.email, subject, message, file_path)
        response = 'We sent you an email!'
        return render(request, 'user/response.html', {'response': response})
    except Exception:
        response = f'Error! {Exception}'
        template = render(request, 'user/response.html', {'response': response})
        template.status_code = 404
        return template

