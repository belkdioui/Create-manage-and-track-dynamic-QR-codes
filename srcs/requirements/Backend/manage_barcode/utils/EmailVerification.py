from django.shortcuts import render, redirect
from django.http import JsonResponse
from .. models import FormData
from email.mime.text import MIMEText
from .utils_1 import check_errors
import smtplib
import os
import hashlib
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def send_email(request, db_user, reason):
    subject = "Email Verification"
    body = "Hello " + (str)(db_user.fname).capitalize() + ' ' + (str)(db_user.lname).capitalize() + f"click this link to verifie your email http://10.30.252.32:8000/{reason}/" + (str)(db_user.token)
    sender_email = os.environ.get('EMAIL_HOST_USER')
    recipient_list = [db_user.email]
    server = smtplib.SMTP('smtp.gmail.com', 587)
    message = MIMEText(body)
    message['From'] = sender_email
    message['To'] = recipient_list[0]
    message['Subject'] = subject
    print(f"------sendemail---\n{sender_email}")
    print(os.environ.get('EMAIL_HOST_PASSWORD'))
    try:
            server.ehlo()
            server.starttls()
            server.login(sender_email, os.environ.get('EMAIL_HOST_PASSWORD'))
            server.sendmail(sender_email, recipient_list, message.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
        return JsonResponse({'Error': f"Error sending email: {e}"})
    
    

def verifie(request, token):
    db_user = ''
    try:
        for data in FormData.objects.all():
            print(f"{data.token} token = {token}")
            if data.token == token:
                db_user = data
        if db_user != '':
            try:
                user = User.objects.get(username=db_user.email)
            except User.DoesNotExist:
                user = User.objects.create_user(db_user.email, db_user.email, db_user.password)
                user.save()
            print(f"hada authonticated################# ")
            db_user.activated = True
            if request.path.find("reset_password") != -1:
                print("passssssssssssssssssss")
                return render(request, 'auth/reset_password.html', {'verifie_password':'true'})
            db_user.token = ''
            db_user.save()
            print(f"#####{request.path}#######")
            return render(request, 'auth/login.html')
    except Exception as e:
                return JsonResponse({'Error': f"Error sending email: tamalek{e}"})
    return redirect('/')

def is_email_verified(request):
    if (FormData.objects.get(email=request.user).activated != True):
        return render(request, '/', {'valide':'false'})
    return render(request, 'home.html')

def save_new_password(request):
    ctx = {}
    if request.method == "POST":
        try:
            name = request.POST.get('email')
            new_password = request.POST.get('new_password')
            c_password = request.POST.get('c_password')
            data = {'password':new_password, 'cpassword':c_password}
            ctx['errors'] = check_errors("reset_password", data)
            try:
                FormData.objects.get(email=name)
            except FormData.DoesNotExist:
                ctx['errors']['email'] = 'Enter valide email'
            if(len(ctx['errors']) != 0):
                ctx['verifie_password'] = 'true'
                return render(request, 'auth/reset_password.html', context=ctx)
            user = User.objects.get(username=name)
            db_user = FormData.objects.get(email=user.username)
            user.set_password(new_password)
            user.save()
            db_user.token = ''
            db_user.save()
        except Exception as e:
            return JsonResponse({'Error': f"Error saving password: {e}"})
    return render(request, 'auth/login.html')

def forgot_password(request):
    ctx= {}
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            db_user = FormData.objects.get(email=email)
            db_user.token = hashlib.sha256((db_user.email + (str)(date.today())).encode("utf-8")).hexdigest()
            db_user.save()
            ctx['send'] = 'true'
            send_email(request, db_user, 'reset_password')
        except FormData.DoesNotExist:
            ctx['wrong_email'] = "true"
    ctx['verifie_email'] = 'true'
    return render(request, 'auth/reset_password.html', context=ctx)