from django.shortcuts import render, redirect
from django.http import JsonResponse
from manage_barcode.utils import utils_1
from .models import FormData
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
                login(request, user_auth)
                FormData.objects.create(fname=fname, lname=lname, email=email, tel=tel)
                return redirect('/')
            
    return render(request, 'auth/signup.html', context=ctx)

def index(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    return login_api(request)
    
    
    
def login_api(request):
   
    ctx= {}
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return render(request, 'home.html')    
        ctx['pass'] = 'Invalide password'
    return render(request, 'auth/login.html', context=ctx)


def logout_api(request):

    logout(request)
    return redirect('/')