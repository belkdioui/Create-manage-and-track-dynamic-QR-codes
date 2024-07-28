from django.contrib import admin
from django.urls import path
from . import views
from .utils import EmailVerification

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'), 
    path('logout/', views.logout_api, name='logout'),
    path('email_verification/<str:token>/', EmailVerification.verifie, name='verifie'),
    path('email_verification/', EmailVerification.forgot_password, name='forgot_password'),
    path('home/', views.get_data_home, name="get_data_home")
]
