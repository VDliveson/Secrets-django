from django.contrib import admin
from django.urls import path, include
from . views import *

urlpatterns = [
    path('', home, name='home'),
    path('login', login_attempt, name='login'),
    path('logout', logout_attemp, name='logout'),
    path('register', register_attempt, name='register'),
    path('token', token_send, name='token_send'),
    path('success', success, name='success'),
    path('verify/<auth_token>', verify, name='verify'),
    path('error', error_page, name='error'),
    path('secret', secret, name='secret'),
]
