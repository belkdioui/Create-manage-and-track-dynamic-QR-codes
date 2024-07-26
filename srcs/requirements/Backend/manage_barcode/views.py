from django.shortcuts import render, redirect
from django.http import JsonResponse
from manage_barcode.utils import utils_1
from .models import FormData
import hashlib
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
            User.objects.create_user(username=email , password=password)
            user_auth = authenticate(username=email, password=password)
            if user_auth is not None:
                db_user = FormData.objects.create(fname=fname, lname=lname, email=email, tel=tel)
                verification_token(user_auth)
                send_email(request, db_user)
                return redirect('/')
    return render(request, 'auth/signup.html', context=ctx)

def index(request):
    ctx= {}
    if request.user.is_authenticated:
        is_email_verified(request)
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



import smtplib
import os

def send_email(request, db_user):
    # try:
    subject = "Email Verification"
    message = f"Hello {db_user.fname} {db_user.lname} click this link to verifie your email http://10.30.252.32:8000/email_verification/{db_user.token}"
    sender_email = os.environ.get('EMAIL_HOST_USER')
    recipient_list = [db_user.email]
    server = smtplib.SMTP('smtp.gmail.com', 587)
    try:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, os.environ.get('EMAIL_HOST_PASSWORD'))
            server.sendmail(sender_email, recipient_list, message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending email: {e}")
        return JsonResponse({'Error': f"Error sending email: {e}"})


def verifie(request, token):
    print('****************************')
    print(f'token = {token}')
    print('****************************')
    try:
        db_user = FormData.objects.get(email=request.user)
        my_token =  hashlib.sha256(db_user.email.encode('utf-8')).hexdigest()
        if my_token == token:
            db_user.activation = True
            db_user.token = ''
            db_user.save()
            user_auth = authenticate(username=db_user.email, password=db_user.password)
            if user_auth is not None:
                login(request, user_auth)
    except Exception:
        return
    return render(request, '/')

def verification_token(user):
    try:
        token = hashlib.sha256(user.email.encode('utf-8')).hexdigest()
        db_member = FormData.objects.get(email=user)
        db_member.token = token
        db_member.save()
    except Exception as e:
        print("--------------\nuser not found\n------------")

def is_email_verified(request):
    try:
        if (FormData.objects.get(email=request.user).activated == True):
            return
    except Exception as e:
        return render(request, '/', {'valide':'false'})
        