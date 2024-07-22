from djongo import models

class FormData(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    tel = models.CharField(max_length=10)
    password = models.EmailField(max_length=100)
    cpassword = models.EmailField(max_length=100)

    def __str__(self):
        return f'{self.fname}'