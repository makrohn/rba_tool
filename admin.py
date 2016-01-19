from django.contrib import admin

# Register your models here.
from .models import System, Role

admin.site.register(Role)
admin.site.register(System)
