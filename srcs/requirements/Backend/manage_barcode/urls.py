from django.contrib import admin
from django.urls import path
from . import views
from .utils import EmailVerification

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'), 
    path('logout/', views.logout_api, name='logout'),
    path('email_verification/<str:token>/', EmailVerification.verifie, name='verifie'),


    path('email_verification/', EmailVerification.forgot_password, name='forgot_password'),
    path('home/', views.get_data_home, name="get_data_home"),
    
    path('reset_password/<str:token>/', EmailVerification.verifie, name='verifie'),
    path('reset_password/', EmailVerification.forgot_password, name='forgot_password'),
    path('update_password/', EmailVerification.save_new_password, name='savepassword'),
]