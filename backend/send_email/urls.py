from django.urls import path

from .views import *

urlpatterns = [
    path('subscribe/', send_subscription_email, name='subscribe'),
    path('unsubscribe/', send_unsubscribe_email, name='unsubscribe'),
    path('send_one_email/', send_one_email, name='send_one_email'),

]
