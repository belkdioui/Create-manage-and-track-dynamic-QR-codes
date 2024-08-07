from .. models import FormData
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse

import os



def update_data(request):
    if not request.user.is_authenticated:
        return redirect('/')
    ctx = {}
    ctx['errors'] = []
    if request.method == "POST":
        user = request.user
        if user:
            db_user = FormData.objects.get(email=user.username)
            fname = request.POST.get('first_name')
            lname = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('pas')
            new_password = request.POST.get('npas')
            confirm_password = request.POST.get('cpas')
            if password and new_password and confirm_password:
                if authenticate(username=db_user.email, password=password) == None:
                    ctx['errors'].append("Invalide Password")
                if new_password != confirm_password:
                    ctx['errors'].append("Password is not the same as the confirmation password")
            if(len(ctx['errors']) != 0):
                db_user = FormData.objects.get(email=request.user.username)
                profile = db_user.path_avatar
                data = {'tel':db_user.tel, 'email':db_user.email, 'fname':db_user.fname.capitalize(), 'lname':db_user.lname.capitalize(), 'ticket':db_user.tickets.count(), 'balance':db_user.balance, 'avatar':profile}
                ctx['profile'] = data
                return render(request, 'pages/profile.html', ctx)
            if 'photo' in request.FILES:
                file = request.FILES['photo']
                filename = file.name  # Use the original filename
                filepath = os.path.join(settings.MEDIA_ROOT, 'manage_barcode/static/media/', filename)
                # Save the uploaded file
                with open(filepath, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                db_user.path_avatar = os.path.join('/static/media/', filename)

            if (fname != db_user.fname and fname != None):
                db_user.fname = fname
            if (lname != db_user.lname and lname != None):
                db_user.lname = lname
            if (email != db_user.email and email != None):
                user = User.objects.get(username=db_user.email)
                db_user.email = email
                user.email = email
            # update mot de pass
            user.set_password(new_password)
            user.save()
            db_user.save()
    return redirect('/profile/')

def delete_account(request):
    if request.method == "DELETE":
        try:
            user = FormData.objects.get(email=request.user.username)
            user.delete()
            print(f"he9 mxa{user.fname}")
            return JsonResponse({
                    'success' : 'Account Deleted'
                }, status=200)
        except FormData.DoesNotExist:
            return JsonResponse({
                'error' : 'Counkd not delete account'}, status=404)
    return JsonResponse({
                'error' : 'Method Not Allowed'}, status=405)