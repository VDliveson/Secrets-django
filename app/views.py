from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import uuid
from django.contrib import messages
from . models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'index.html')


def login_attempt(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method == 'POST'):
        password = request.POST.get('password')
        username = request.POST.get('username')

        try:
            if(username == ''):
                messages.success(request, 'Kindly enter a value')
                return redirect('/login')

            user_obj = User.objects.filter(username=username).first()
            if(user_obj is None):
                messages.success(request, 'User not found.Kindly register')
                return redirect('/login')

            profile_obj = Profile.objects.filter(user=user_obj).first()

            if not profile_obj.is_verified:
                messages.success(
                    request, 'Mail not verified.Kindly check your mail')
                return redirect('/login')

            user = authenticate(username=username, password=password)
            if user is None:
                messages.success(request, 'Wrong password')
                return redirect('/login')

            login(request, user)
            return redirect('/')

        except Exception as e:
            print(e)

    return render(request, 'login.html')


def logout_attemp(request):
    logout(request)
    return redirect('/')


def register_attempt(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            if(User.objects.filter(username=username).first()):
                messages.success(request, 'Username is already taken')
                return redirect('/register')

            if(User.objects.filter(email=email).first()):
                messages.success(request, 'Email is already registered')
                return redirect('/register')

            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(
                user=user_obj, auth_token=auth_token)
            profile_obj.save()
            # send_mail_registered(email, auth_token)
            print(auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request, 'register.html')


def token_send(request):
    return render(request, 'token.html')


def success(request):
    return render(request, 'success.html')


def send_mail_registered(email, token):
    subject = 'Verify your mail(localhost)'
    message = 'Hi paste the link to verify your account \n http://127.0.0.1:8000/verify/'+token
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if(profile_obj.is_verified == True):
                messages.success(request, 'Your account is already verified')
                return redirect('/login')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified')
            return redirect('/login')
        else:
            return redirect('/error')

    except Exception as e:
        print(e)
        return redirect('/')


def error_page(request):
    return render(request, 'error.html')


@login_required
def secret(request):
    return render(request, 'secret.html')
