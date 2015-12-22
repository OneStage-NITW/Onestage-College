from django.shortcuts import render
from django.contrib.auth.models import User,Group
from authentication.models import UserProfile
from authentication.forms import UserForm,UserProfileForm
from datetime import datetime
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import hashlib
# Create your views here.


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	else:
		return HttpResponseRedirect('/home')

def home(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	else:
		response={}
		response['user']=request.user
		response['userprofile']=request.user.userprofile
		if request.user.groups.filter(name='Onestage').count() == 1:
			response['onestage']=1
		if request.user.is_superuser:
			response['superuser']=1
		elif request.user.groups.filter(name='Organisation').count() == 1:
			response['organisation']=1
		elif request.user.groups.filter(name='CAP').count() == 1:
			response['cap']=1
		return render(request,'site/main.html',response)

def loginuser(request):
	response={}
	if request.method=="POST":
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				user.lastLoginDate=datetime.now()
				user.userprofile.loggedIn=True
				user.save()
				return HttpResponseRedirect('/home')
			else:
				response['message']="Invalid user"
		else:
			response['message']="User name or password wrong"
	return render(request,'site/login.html',response)

def logoutuser(request):
	logout(request)
	return HttpResponseRedirect('/login')

def newuser(request):
	email=request.GET['email']
	password=request.GET['password']
	group=request.GET['group']
	user=User.objects.get(username=email,password=password)
	if user is not None:
		response['user']=user
		return render(request,'site/newuser.html',response)
	else:
		return HttpResponseNotFound('<h1>Page not found</h1>')

def getonestageusers(request):
	response={}
	if request.user.groups.filter(name='Onestage').count() == 1:
		users=User.objects.filter(groups__name='onestage')
		response['ousers']=users
		return render(request,'site/onestageusers.html',response)
	else:
		return HttpResponseNotFound('<h1>Page not found</h1>')

