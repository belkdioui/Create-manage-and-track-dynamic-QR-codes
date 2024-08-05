from django.contrib import admin
from django.urls import path
from . import views
from .utils import EmailVerification

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'), 
    path('home/', views.get_data_home, name="get_data_home"),
    path('buy-tickets/', views.buy_tickets, name="buy_tickets"),
    path('Schedules_Stops/', views.Schedules_Stops, name="Schedules_Stops"),


    path('logout/', views.logout_api, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    path('reset_password/', EmailVerification.forgot_password, name='forgot_password'),
    
    path('email_verification/<str:token>/', EmailVerification.verifie, name='verifie'),
    path('reset_password/<str:token>/', EmailVerification.verifie, name='verifie'),
    
    path('update_password/<str:token>/', EmailVerification.save_new_password, name='savepassword'),



    path('update_data/', EmailVerification.update_data, name='update_data'),

]