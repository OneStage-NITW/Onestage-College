from django.contrib import admin
from .models import Platform,PlatformDetails,Organisation,Volunteers,OrgMap,PlatformMap
# Register your models here.

admin.site.register(Platform)
admin.site.register(PlatformDetails)
admin.site.register(Organisation)
admin.site.register(OrgMap)
admin.site.register(PlatformMap)
admin.site.register(Volunteers)