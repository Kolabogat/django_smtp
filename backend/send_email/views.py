from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from .forms import SendEmailForm
from .models import Contact
from .tasks import (
    send_newsletter_email_task,
)


@login_required
def send_subscription_email(request):
    try:
        if Contact.objects.filter(user=request.user, subscribed_mail=False).exists():
            contact_user = Contact.objects.filter(user=request.user, subscribed_mail=False).get()
            subject = 'You are subscribed to the newsletter!'
            message = 'You have subscribed to the newsletter!'
            send_newsletter_email_task.delay(request.user.email, subject, message)
            contact_user.subscribed_mail = True
            contact_user.save()
            response = 'You have subscribed to the newsletter!'
            return render(request, 'user/response.html', {'response': response})
        elif Contact.objects.filter(user=request.user, subscribed_mail=True).exists():
            response = 'You already subscribed to the newsletter!'
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
def send_unsubscribe_email(request):
    try:
        if Contact.objects.filter(user=request.user, subscribed_mail=True).exists():
            contact_user = Contact.objects.filter(user=request.user, subscribed_mail=True).get()
            subject = 'You have unsubscribed from the newsletter!'
            message = 'You have unsubscribed from the newsletter!'
            send_newsletter_email_task.delay(request.user.email, subject, message)
            contact_user.subscribed_mail = False
            contact_user.save()
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
