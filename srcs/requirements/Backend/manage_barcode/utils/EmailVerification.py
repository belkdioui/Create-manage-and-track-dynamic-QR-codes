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
    body = f"Hello {db_user.fname.capitalize()} {db_user.lname.capitalize()} click this link to verifie your email http://0.0.0.0:8000/{reason}/{db_user.token}"
    sender_email = os.environ.get('EMAIL_HOST_USER')
    recipient_list = [db_user.email]
    server = smtplib.SMTP('smtp.gmail.com', 587)
    message = MIMEText(body)
    message['From'] = sender_email
    message['To'] = recipient_list[0]
    message['Subject'] = subject
    print(f"------sendemail---\n{sender_email}")
    print(os.environ.get('EMAIL_HOST_PASSWORD'))
    server.ehlo()
    server.starttls()
    server.login(sender_email, os.environ.get('EMAIL_HOST_PASSWORD'))
    server.sendmail(sender_email, recipient_list, message.as_string())

def verifie(request, token):
    if request.user.is_authenticated:
        return redirect('/')
    ctx = {}
    try:
        db_user = FormData.objects.get(token=token)
        
        if request.path.find("reset_password") != -1:
            return render(request, 'pages/reset_password.html', {'verifie_password':'true', 'token': token})

        db_user.activated = True
        db_user.token = ''
        db_user.save()

        return redirect('/')
    
    except FormData.DoesNotExist:
        ctx['errors']['form_not_exist'] = 'Invalide token'
    except Exception as e:
            ctx['errors']['sending_mail'] = 'Error sending email'

    return render(request, 'pages/reset_password.html', context=ctx)
    

def save_new_password(request, token):
    if request.user.is_authenticated:
        return redirect('/')

    ctx = {}
    if request.method == "POST":
        try:
            user_db = FormData.objects.get(token=token)
            
            new_password = request.POST.get('new_password')
            c_password = request.POST.get('c_password')

            data = {'password':new_password, 'cpassword':c_password}
            ctx['errors'] = check_errors("reset_password", data)
            
            if(len(ctx['errors']) != 0):
                ctx['verifie_password'] = 'true'
                return render(request, 'pages/reset_password.html', context=ctx)

            user = User.objects.get(username=user_db.email)
            user.set_password(new_password)
            user.save()

            user_db.token = ''
            user_db.save()

        except User.DoesNotExist:
            ctx['errors']['user_error'] = 'Enter valid email'
        except FormData.DoesNotExist:
            ctx['errors']['email'] = 'Enter valid email'
        except Exception as e:
            ctx['errors']['exception'] = f"Error saving password: {e}"

        if(len(ctx['errors']) != 0):
            ctx['verifie_password'] = 'true'
            return render(request, 'pages/reset_password.html', context=ctx)
        
    return redirect('/')

def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('/')

    ctx= {}
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            db_user = FormData.objects.get(email=email)
            db_user.token = hashlib.sha256((db_user.email + (str)(date.today())).encode("utf-8")).hexdigest()
            db_user.save()
            send_email(request, db_user, 'reset_password')
            ctx['send'] = 'true'

        except FormData.DoesNotExist:
            ctx['wrong_email'] = "true"
        except Exception:
            ctx['email_error'] = "true"
    ctx['verifie_email'] = 'true'
    return render(request, 'pages/reset_password.html', context=ctx)


import uuid
from django.conf import settings


def update_data(request):
    if not request.user.is_authenticated:
        return redirect('/')
    ctx = {}
    if request.method == "POST":
        if 'photo' in request.FILES:
            file = request.FILES['photo']
        else:
            return redirect('/profile/')
        user = request.user
        print(file)
        print("1111111111")
        print(user.password)
        print(request.POST.get('pas'))
        # if file and user:
        #     db_user = FormData.objects.get(email=user.username)
        #     fname = request.POST.get('first_name')
        #     lname = request.POST.get('last_name')
        #     email = request.POST.get('email')
        #     password = request.POST.get('pas')
        #     if authenticate(db_user.email, password) == None:
        #         ctx["errors"]["password"] = "wrong password"
        #     new_password = request.POST.get('npas')
        #     confirm_password = request.POST.get('cpas')
        #     if new_password != confirm_password:
        #         ctx["errors"]["confirm_password"] = "password is not the same as the confirmation password"
        #     filename = file.name  # Use the original filename
        #     filepath = os.path.join(settings.MEDIA_ROOT, 'manage_barcode/static/media/', filename)
        #     # Save the uploaded file
        #     with open(filepath, 'wb+') as destination:
        #         for chunk in file.chunks():
        #             destination.write(chunk)

        #     # Store the relative path in the database (recommended)
        #     if (fname != db_user.fname):
        #         db_user.fname = fname
        #     if (lname != db_user.lname):
        #         db_user.lname = lname
        #     if (email != db_user.email):
        #         user = User.objects.get(username=db_user.email)
        #         db_user.email = email
        #         user.email = email
        #         user.save()
        #     # update mot de pass
        #     db_user.path_avatar = os.path.join('/static/media/', filename)
        #     db_user.save()
    return redirect('/profile/')

    