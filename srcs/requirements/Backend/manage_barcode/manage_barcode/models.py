from djongo import models

class FormData(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
