from django.shortcuts import render
from django.http import JsonResponse
from manage_barcode.utils import utils_1
from .models import FormData

def signup(request):
    ctx = {}
    # if not request.user.is_authenticated:
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
            FormData.objects.create(fname=fname, lname=lname, email=email, tel=tel, password=password, cpassword=cpassword)
            return JsonResponse({'message': 'Data saved successfully'})
            #if good
                # create model ....
                # redirect to home

        
        
        
    return render(request, 'auth/signup.html', context=ctx)
    
    
    
    # return render(request, 'home.html')

def index(request):
    return render(request, 'auth/login.html')

    