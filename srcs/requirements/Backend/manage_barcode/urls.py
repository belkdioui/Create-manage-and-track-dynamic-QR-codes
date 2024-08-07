from django.contrib import admin
from django.urls import path
from . import views
from .utils import EmailVerification , Profile, Qrscanner

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'), 
    path('home/', views.get_data_home, name="get_data_home"),
    path('buy-tickets/', views.buy_tickets, name="buy_tickets"),
    path('Schedules_Stops/', views.Schedules_Stops, name="Schedules_Stops"),


    path('logout/', views.logout_api, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('resend_email/', EmailVerification.reverify_email, name='reverify_email'),
    path('reset_password/', EmailVerification.forgot_password, name='forgot_password'),
    
    
    path('reset_password/<str:token>/', EmailVerification.verifie_password, name='verifie'),
    path('email_verification/<str:token>/', EmailVerification.verifie_email, name='verifie_email'),
    path('update_password/<str:token>/', EmailVerification.save_new_password, name='savepassword'),


    path('delete_account/', Profile.delete_account, name='delete_account'),

    path('update_data/', Profile.update_data, name='update_data'),
    path('qr_scanner/', Qrscanner.qr_scanner, name='qr_scanner'),
    path('scanner/', Qrscanner.scanner, name='scanner'),
]
