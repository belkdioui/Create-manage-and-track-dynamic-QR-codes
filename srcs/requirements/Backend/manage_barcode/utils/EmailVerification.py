from django.shortcuts import render, redirect
from django.http import JsonResponse
from .. models import FormData, Tickets
from email.mime.text import MIMEText
from .utils_1 import check_errors
import smtplib
import os
import hashlib
import uuid
from django.conf import settings
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def send_email(request, db_user, reason):
    subject = "Email Verification"
    body = f"Hello {db_user.fname.capitalize()} {db_user.lname.capitalize()} click this link to verifie your email http://0.0.0.0:8000/{reason}/{db_user.token}"
    sender_email = os.environ.get('EMAIL_HOST_USER')
    recipient_list = [db_user.email]
    server = smtplib.SMTP('smtp.gmail.com', 587)
    message = MIMEText(body)
    message['From'] = sender_email
    message['To'] = recipient_list[0]
    message['Subject'] = subject
    server.ehlo()
    server.starttls()
    server.login(sender_email, os.environ.get('EMAIL_HOST_PASSWORD'))
    server.sendmail(sender_email, recipient_list, message.as_string())

def verifie_password(request, token):
    if request.user.is_authenticated:
        return redirect('/')
    ctx = {}
    ctx['errors'] = []
    try:
        FormData.objects.get(token=token)
        print('daze mnhnaaaa')
        print('daze mnhnaaaa')
        print('daze mnhnaaaa')
        return render(request, 'pages/reset_password.html', {'token':token})
    except FormData.DoesNotExist:
        ctx['errors'].append('Invalide token')
    except Exception:
        ctx['errors'].append('Error sending email')
    ctx['sendmail'] = "sendmail"
    return render(request, 'pages/reset_password.html', context=ctx)


def verifie_email(request, token):
    if request.user.is_authenticated:
        return redirect('/')
    ctx = {}
    ctx['errors'] = []
    try:
        db_user = FormData.objects.get(token=token)
        db_user.activated = True
        db_user.token = ''
        db_user.save()
        return redirect('/')
    except FormData.DoesNotExist:
        ctx['errors'].append('Invalide token')
    except Exception as e:
        ctx['errors'].append('Error sending email')

    return render(request, 'pages/resend_email.html', context=ctx)
    

def save_new_password(request, token):
    if request.user.is_authenticated:
        return redirect('/')
    ctx = {}
    if request.method == "POST":
        try:
            user_db = FormData.objects.get(token=token)
            
            new_password = request.POST.get('new_password')
            c_password = request.POST.get('c_password')
            print(new_password)
            print(c_password)
            print(token)
            data = {'password':new_password, 'cpassword':c_password}
            ctx['errors'] = check_errors("reset_password", data)

            if(len(ctx['errors'])):
                print("eeerrrrrrrrrrr")
                print("eeerrrrrrrrrrr")
                return render(request, 'pages/reset_password.html', context=ctx)

            user = User.objects.get(username=user_db.email)
            user.set_password(new_password)
            user.save()
            user_db.token = ''
            user_db.save()

        except User.DoesNotExist:
            ctx['errors'] = {'user_error':'Enter valid email'}
        except FormData.DoesNotExist:
            ctx['errors']= {'email':'Enter valid email'}
        except Exception as e:
            ctx['errors']={'exception':f"Error saving password: {e}"}
    return render(request, 'pages/login.html', context=ctx)

def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('/')

    ctx= {}
    if request.method == "POST":
        ctx['errors'] = []
        try:
            email = request.POST.get('email')
            db_user = FormData.objects.get(email=email)
            if not db_user.activated:
                ctx['errors'].append("unverified email")
                return render(request, 'pages/login.html', context=ctx)
            db_user.token = hashlib.sha256((db_user.email + (str)(date.today())).encode("utf-8")).hexdigest()
            db_user.save()
            send_email(request, db_user, 'reset_password')
            ctx['success'] = 'Check you email for verification link.'
            return render(request, 'pages/login.html', context=ctx)
        except FormData.DoesNotExist:
            ctx['errors'].append("This email is not registred.")
        except Exception:
            ctx['errors'].append("Error during sending email")
    ctx['sendmail'] = "sendmail"
    return render(request, 'pages/reset_password.html', context=ctx)


def reverify_email(request):
    if request.user.is_authenticated:
        return redirect('/')
    ctx= {}
    if request.method == "POST":
        ctx['errors'] = []
        try:
            email = request.POST.get('email')
            db_user = FormData.objects.get(email=email)
            db_user.token = hashlib.sha256((db_user.email + (str)(date.today())).encode("utf-8")).hexdigest()
            db_user.save()
            send_email(request, db_user, 'email_verification')
            ctx['success'] = 'Email has been sent.'
            return redirect ('/')
        except FormData.DoesNotExist:
            ctx['errors'].append("This email is not registred.")
        except Exception:
            ctx['errors'].append("Error during sending email")
    return render(request, 'pages/resend_email.html', context=ctx)