from django.shortcuts import render
from django.contrib.auth.models import User,Group
from authentication.models import UserProfile
from authentication.forms import UserForm,UserProfileForm
from datetime import datetime
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
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

@csrf_exempt
def register(request):	
	registered = False
	response={}
	if request.method == "POST":
		method=request.POST['method']
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		print profile_form
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save(commit=False)
			user.set_password(user.password)
			user.is_active=True
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			# profile.mobile_id=mobile_id
			profile.lastLoginDate = datetime.now()
			profile.ipaddress=get_client_ip(request)
			profile.save()
			registered = True
			response['success']=1
		else:
			print user_form.errors, profile_form.errors
			response['success']=0
	return JsonResponse(response)

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
		# mobile_id=request.POST['mobile_id']
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
			# profile.mobile_id=mobile_id
			profile.lastLoginDate = datetime.now()
			profile.ipaddress=get_client_ip(request)
			profile.save()
			registered = True
			response['success']=1
			response['email']=email
			response['id']=user.id
		else:
			# user.userprofile.mobile_id=mobile_id
			user.first_name=name
			user.userprofile.save()
			user.save()
			response['success']=1
			response['message']="User is already present"
			response['email']=user.username
			response['id']=user.id
	return JsonResponse(response)