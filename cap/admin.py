from django.contrib import admin
from .models import Platform,PlatformDetails,Organisation
# Register your models here.

admin.site.register(Platform)
admin.site.register(PlatformDetails)
admin.site.register(Organisation)