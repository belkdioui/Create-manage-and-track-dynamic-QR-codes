from django.shortcuts import render, redirect
from django.http import JsonResponse
from manage_barcode.utils import utils_1 ,EmailVerification, generate_qr_code
from .models import FormData, Tickets, City, Station, Bus
import hashlib
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import smtplib
import os
from datetime import date
import json
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
        data= {"fname": fname,"lname": lname, "email":email, "tel":tel, "password":password, "cpassword":cpassword}
        ctx['errors'] = utils_1.check_errors("sign_up", data)
        if(len(ctx['errors']) == 0):
            try:
                user = User.objects.create_user(username=email, email=email, password=password)
                user.save()
                db_user = FormData.objects.create(fname=fname, lname=lname, email=email, tel=tel)
                db_user.token = hashlib.sha256((email + (str)(date.today())).encode("utf-8")).hexdigest()
                db_user.save()
                EmailVerification.send_email(request, db_user, 'email_verification')
                ctx['success'] = 'Check you email for verification link.'
                return render(request, 'pages/login.html' ,ctx)
            except Exception as e:
                ctx['errors']['email_error'] = f"Error email"
    return render(request, 'pages/signup.html', context=ctx)



def get_data_home(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.user.is_authenticated and request.user.is_superuser:
        logout_api(request)
        return redirect('/')
    
    ctx={}
    db_user = FormData.objects.get(email=request.user.username)
    number_of_tickets = db_user.tickets.count()
    if(number_of_tickets):
        generate_qr_code.generate_qr_code_from_id(db_user.tickets.first())
    ctx = {
        'db_user' : db_user,
        'count_ticket' : number_of_tickets,
    }
    return render(request, 'pages/home.html', ctx)



def buy_tickets(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.user.is_authenticated and request.user.is_superuser:
        logout_api(request)
        return redirect('/')
    
    ctx={}
    if(request.method == 'POST'):
        try:
            data = json.loads(request.body)
            tickets = int(data.get('tickets_t', 0))
            balance = int(data.get('total_c', 0))
            db_user = FormData.objects.get(email=request.user.username)
            if(db_user.balance >= balance):
                db_user.balance -= balance
                db_user.save()
                for _ in range(tickets):
                    try:
                        ticket = Tickets.objects.create(client=db_user)
                        barcode = f"busbladi: {ticket.id}{db_user.fname}"
                        ticket.barcode = barcode
                        ticket.save()
                    except Exception as e:
                        return JsonResponse({'error': f"Error creating ticket: {e}"}, status=400)
            else:
                return JsonResponse({'error': "Insufficient balance"}, status=400)
        except Exception as e:
            return JsonResponse({'error': f"Unexpected error: {e}"}, status=400)
        ctx = {
        'balance': db_user.balance,
        'count_ticket': db_user.tickets.count()
    }
        return JsonResponse(ctx, status=200)
    elif(request.method == 'GET'):
        db_user = FormData.objects.get(email=request.user.username)
        ctx = {
            'db_user' : db_user,
            'count_ticket' : db_user.tickets.count()
        }
    return render(request, 'pages/buy-tickets.html', ctx)


def Schedules_Stops(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.user.is_authenticated and request.user.is_superuser:
        logout_api(request)
        return redirect('/')
    context=[]
    if request.method == 'GET':
        cities = City.objects.all()
        city = City.objects.first()
        bus = Bus.objects.filter(city=city).first()
        first_one = Station.objects.filter(bus=bus).first()
        last_one = Station.objects.filter(bus=bus).last()
        context = {'cities': cities, 'city': city, 'bus': bus, 'first_st': first_one, 'last_st':last_one, 'err':False}
    elif (request.method == 'POST'):
        city_post = request.POST.get('city')
        bus_post = request.POST.get('bus')
        cities = City.objects.all()
        city = City.objects.get(name=city_post)
        if (city):
            bus = Bus.objects.get(city=city, name=bus_post)
            if(bus):
                first_one = Station.objects.filter(bus=bus).first()
                last_one = Station.objects.filter(bus=bus).last()
                context = {'cities': cities, 'city': city, 'bus': bus, 'first_st': first_one, 'last_st':last_one, 'err':False}
            else:
                bus = Bus.objects.filter(city=city).first()
                first_one = Station.objects.filter(bus=bus).first()
                last_one = Station.objects.filter(bus=bus).last()
                context = {'cities': cities, 'city': city, 'bus': bus, 'first_st': first_one, 'last_st':last_one, 'err': True}

        else:
            city = City.objects.first()
            bus = Bus.objects.filter(city=city).first()
            first_one = Station.objects.filter(bus=bus).first()
            last_one = Station.objects.filter(bus=bus).last()
            context = {'cities': cities, 'city': city, 'bus': bus, 'first_st': first_one, 'last_st':last_one, 'err':True}

    return render(request, 'pages/Schedules_Stops.html', context)


def index(request):
    ctx= {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            logout_api(request)
            return redirect('/')
        return redirect('/home/')
    return login_api(request)


def login_api(request):
    ctx= {}
    if request.method == "POST":
        ctx['errors'] = []
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            if FormData.objects.get(email=email).activated == True:
                login(request, user)
                return redirect('/home/')
            ctx['errors'].append('Account Disabled, please check your email')
            ctx['account_disabled'] = 'true'
        else:
            ctx['errors'].append('Invalide email or password')
    return render(request, 'pages/login.html', context=ctx)


def logout_api(request):
    logout(request)
    return redirect('/')


from django.conf import settings

def profile(request):
    if request.user.is_superuser:
        logout_api(request)
    elif request.user.is_authenticated:
        try:
            db_user = FormData.objects.get(email=request.user.username)
            profile = db_user.path_avatar
            data = {'tel':db_user.tel, 'email':db_user.email, 'fname':db_user.fname.capitalize(), 'lname':db_user.lname.capitalize(), 'ticket':db_user.tickets.count(), 'balance':db_user.balance, 'avatar':profile}
        except Exception as e:
            return JsonResponse({'Error': f"Error sending email: {e}"})
        return render(request, 'pages/profile.html', {'profile':data})
    return redirect('/')
