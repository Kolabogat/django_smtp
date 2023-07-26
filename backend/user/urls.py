from django.urls import path

from .views import *

urlpatterns = [
    path('', user_profile, name='user_profile'),
    path('user_response/', user_response, name='user_response'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
