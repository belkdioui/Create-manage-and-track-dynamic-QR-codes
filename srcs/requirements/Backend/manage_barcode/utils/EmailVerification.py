from django.shortcuts import render, redirect
from django.http import JsonResponse
from .. models import FormData
from email.mime.text import MIMEText
import smtplib
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
def send_email(request, db_user):
    subject = "Email Verification"
    body = "Hello " + (str)(db_user.fname).capitalize() + ' ' + (str)(db_user.lname).capitalize() + "click this link to verifie your email http://10.30.252.32:8000/email_verification/" + (str)(db_user.token)
    sender_email = os.environ.get('EMAIL_HOST_USER')
    recipient_list = [db_user.email]
    server = smtplib.SMTP('smtp.gmail.com', 587)
    message = MIMEText(body)
    message['From'] = sender_email
    message['To'] = recipient_list[0]
    message['Subject'] = subject
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
            print(f"hada authonticated################# ")
            try:
                user = User.objects.get(username=db_user.email)
            except User.DoesNotExist:
                user = User.objects.create_user(db_user.email, db_user.email, db_user.password)
                user.save()
            user_auth = authenticate(username=db_user.email, password=db_user.password)
            login(request, user_auth)
            db_user.activated = True
            db_user.token = ''
            db_user.save()
    except Exception as e:
                return JsonResponse({'Error': f"Error sending email: tamalek{e}"})
    return redirect('/')
def is_email_verified(request):
    if (FormData.objects.get(email=request.user).activated == True):
        return
    else:
        return render(request, '/', {'valide':'false'})
def forgot_password(request):
    ctx= {}
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            FormData.objects.get(email=email)
            ctx['reset_password'] = "true"
        except FormData.DoesNotExist:
            ctx['wrong_email'] = "true"
    return render(request, 'auth/email_verification.html', context=ctx)