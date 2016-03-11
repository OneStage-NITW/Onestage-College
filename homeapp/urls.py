from django.conf.urls import include, url
from homeapp import views

urlpatterns = [
    
    url(r'^$', views.home),
    url(r'^platforms/$', views.platforms),
    url(r'^viewplatform/(?P<platformid>.+)$', views.renderplatform),
    url(r'^aboutus/$',views.aboutus),
    url(r'^mission/$',views.mission),
    url(r'^organisations/$',views.organisations),
    url(r'^campuses/$',views.campuses),
    url(r'^team/$',views.teampage),
    url(r'^sendfeedback/$',views.sendfeedback),
]

