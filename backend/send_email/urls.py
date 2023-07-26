from django.urls import path

from .views import *

urlpatterns = [
    path('subscribe/', send_subscription_email, name='subscribe'),
    path('unsubscribe/', send_unsubscribe_email, name='unsubscribe'),
    path('send_one_email/', send_one_email, name='send_one_email'),
    path('send_email_form/', send_email_form, name='send_email_form'),
    path('send_review_form/', send_review_form, name='send_review_form'),
]
