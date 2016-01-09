from django.conf.urls import include, url
from homeapp import views

urlpatterns = [
    
    url(r'^$', views.home),
]

