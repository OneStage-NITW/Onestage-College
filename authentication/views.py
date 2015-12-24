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


@csrf_exempt
def register_2(request):	
	registered = False
	flag=0
	response={}
	response['success']=0
	if request.method == "POST":
		method=request.POST['method']
		profile=UserProfile()
		name=request.POST['name']
		email=request.POST['email']
		password=""
		if method == 'normal':
			password=request.POST['password']
		mobile_id=request.POST['mobile_id']
		try:
			user=User.objects.get(username=email)
		except User.DoesNotExist:
			user=User()
			flag=1
		if flag == 1:
			user.first_name=name
			user.username=email
			user.password=password
			user.set_password(user.password)
			user.is_active=True
			user.save()
			profile.user = user
			profile.mobile_id=mobile_id
			profile.lastLoginDate = datetime.now()
			profile.ipaddress=get_client_ip(request)
			profile.save()
			registered = True
			response['success']=1
			response['email']=email
			response['id']=user.id
		else:
			user.userprofile.mobile_id=mobile_id
			user.first_name=name
			user.userprofile.save()
			user.save()
			response['success']=1
			response['message']="User is already present"
			response['email']=user.username
			response['id']=user.id
	return JsonResponse(response)


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






		

