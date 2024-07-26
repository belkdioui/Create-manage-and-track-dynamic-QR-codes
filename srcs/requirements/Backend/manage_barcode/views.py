from django.shortcuts import render, redirect
from django.http import JsonResponse
from manage_barcode.utils import utils_1
from manage_barcode.utils import EmailVerification
from .models import FormData
from email.mime.text import MIMEText
import hashlib
from django.db import IntegrityError
import smtplib
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    ctx = {}
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        password = request.POST.get('Password')
        cpassword = request.POST.get('conf_pass')
        data= {"fname": fname,"lname": lname, "email":email, "tel":tel, "password":password, "cpassword":cpassword }
        ctx['errors'] = utils_1.check_errors("sign_up", data)
        if(len(ctx['errors']) == 0):
            user = User.objects.create_user(email, email, password=password)
            user.save()
            db_user = FormData.objects.create(fname=fname, lname=lname, email=email, tel=tel, password=password)
            db_user.token = hashlib.sha256(password.encode("utf-8")).hexdigest()
            db_user.save()
            EmailVerification.send_email(request, db_user)
            return render(request, 'auth/login.html') # redirect to /
    return render(request, 'auth/signup.html', context=ctx)

def index(request):
    ctx= {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            logout_api(request)
            return redirect('/')
        print('222222222222')
        return render(request, 'home.html')


    return login_api(request)
    

def login_api(request):
    ctx= {}
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            if FormData.objects.get(email=email).activated == False:
                ctx['valide'] = 'false'
                return render(request, 'auth/login.html', context=ctx)
            login(request, user)
            return render(request, 'home.html')
        ctx['pass'] = 'Invalide password'
    return render(request, 'auth/login.html', context=ctx)


def logout_api(request):

    logout(request)
    return redirect('/')



        