from django.shortcuts import render, redirect
from django.http import JsonResponse
from manage_barcode.utils import utils_1 ,EmailVerification, generate_qr_code
from .models import FormData, Tickets
import hashlib

from django.db import IntegrityError
import smtplib
import os
from datetime import date

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
            db_user = FormData.objects.create(fname=fname, lname=lname, email=email, tel=tel)
            db_user.token = hashlib.sha256((email + (str)(date.today())).encode("utf-8")).hexdigest()
            db_user.save()
            EmailVerification.send_email(request, db_user, 'email_verification')
            return render(request, 'auth/login.html')
    return render(request, 'auth/signup.html', context=ctx)


def index(request):
    ctx= {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            logout_api(request)
            return redirect('/')
        return redirect('/home/')

    return login_api(request)

def get_data_home(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.user.is_authenticated and request.user.is_superuser:
        logout_api(request)
        return redirect('/')
    
    ctx={}
    db_user = FormData.objects.get(email=request.user.username)
    number_of_tickets = db_user.tickets.count()
    print(f'N Ticket: {number_of_tickets}')
    if(number_of_tickets):
        generate_qr_code.generate_qr_code_from_id(db_user.tickets.first().id, db_user.email)
    ctx = {
        'db_user' : db_user,
        'count_ticket' : number_of_tickets,
    }
    return render(request, 'home.html', ctx)

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
            return redirect('/home/')
        try:
            FormData.objects.get(email=email)
            ctx['pass'] = 'Invalide password'
        except FormData.DoesNotExist:
            ctx['email'] = 'Invalide email'
    return render(request, 'auth/login.html', context=ctx)


def logout_api(request):

    logout(request)
    return redirect('/')


def profile(request):
    if request.user.is_authenticated:
        try:
            db_user = FormData.objects.get(email=request.user)
            data = {'tel':db_user.tel, 'email':db_user.email, 'fname':db_user.fname, 'lname':db_user.lname}
        except Exception as e:
            return JsonResponse({'Error': f"Error sending email: {e}"})
        return render(request, 'profile.html', data)
    return redirect('/')
        