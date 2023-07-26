from django.http import HttpResponse
from django.shortcuts import render
from .tasks import sleep_time, send_email_task


def index(request):
    send_email_task.delay('')
    return HttpResponse('Hello!')

