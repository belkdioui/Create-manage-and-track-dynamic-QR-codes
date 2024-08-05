from django.contrib import admin
from .models import FormData , Tickets , City , Bus , Station

# Register your models here.
admin.site.register(FormData)
admin.site.register(Tickets)
admin.site.register(City)
admin.site.register(Bus)
admin.site.register(Station)