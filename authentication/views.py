from django.shortcuts import render
from django.contrib.auth.models import User,Group
from authentication.models import UserProfile
from authentication.forms import UserForm,UserProfileForm
from datetime import datetime
from django.http import HttpResponseRedirect,JsonResponse,HttpResponseNotFound
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import hashlib
from django.core.mail import send_mail
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

def getusers(request,utype):
	response={}
	users=User.objects.filter(userprofile__usertype=utype)
	response['ousers']=users
	response['utype']=utype
	return render(request,'site/onestageusers.html',response)


def inviteuser(request):
	response={}
	if request.method == 'POST':
		utype=request.POST['utype']
		email=request.POST['email']
		password=hashlib.sha224(email).hexdigest()
		user=User()
		user.username=email
		user.set_password(password)
		user.is_active=False
		user.save()
		rurl='newuser/'+utype+'/'+password+'/'+email+'/'
		url='http://127.0.0.1:8000/'+rurl
		message='Please click this link for registering: '+url
		send_mail('Invite for new user',message,'root@onestage.com',[email],fail_silently=False)
		response['success']=1
	return JsonResponse(response)

def newuser(request,utype,password,email):
	response={}
	if request.method == "POST":
		user=authenticate(username=email, password=password)
		if user is not None:
			if not user.is_active:
				print "User is registering"
				first_name=request.POST['first_name']
				password=request.POST['password']
				conpassword=request.POST['conpassword']
				if password == conpassword:
					user.set_password(password)
					user.first_name=first_name
					user.is_active=True
					user.save()
					userp=UserProfile()
					userp.user=user
					userp.collegeName=request.POST['collegeName']
					userp.usertype=utype
					if request.FILES['picture']:
						userp.profilepicture=request.FILES['picture']
					else:
						userp.profilepicture='default.jpg'
					userp.lastLoginDate=datetime.now()
					userp.save()
					return HttpResponseRedirect('/login')
				else:
					response['message']="Password not matching"
			else:
				response['message']='User already active'
		else:
			response['message']='User is not allowed to be registered'
	response['utype']=utype
	response['password']=password
	response['email']=email
	return render(request,'site/registernewuser.html',response)






		

