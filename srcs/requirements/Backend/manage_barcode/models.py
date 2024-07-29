# from djongo import models
from django.db import models

class FormData(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    tel = models.CharField(max_length=13)
    activated = models.BooleanField(default=False)
    token = models.CharField(max_length=100, blank=True, null=True)
    balance = models.IntegerField(default=500)

    def __str__(self):
        return f'{self.fname} {self.lname}'

class Tickets(models.Model):
    client = models.ForeignKey(FormData, on_delete=models.CASCADE, related_name='tickets')
    barcode = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.id} - {self.barcode}'

class reset_password(models.Model):
    token = models.CharField(max_length=100)
    signed_token = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.token}'