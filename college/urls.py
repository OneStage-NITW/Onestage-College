"""college URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from authentication import views as auth

urlpatterns = [
    url(r'^$',auth.index),
    url(r'^admin/', admin.site.urls),
    url(r'^login/',auth.loginuser),
    url(r'^logout/',auth.logoutuser),
    url(r'^home/',auth.home),  
    url(r'^manageonstage/(?P<utype>Onestage|CAP|Organization)/',auth.getusers), 
    url(r'^invitenewuser/',auth.inviteuser), 
    url(r'^newuser/(?P<utype>\w+)/(?P<password>\w+)/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/',auth.newuser),
    url(r'^viewprofile/(?P<utype>\w+)/(?P<userid>[A-Za-z0-9.-]+)/',auth.viewprofile),  
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
