from django.shortcuts import render
from django.contrib.auth.models import User,Group
from authentication.models import UserProfile,CapMember
from authentication.forms import UserForm,UserProfileForm
from datetime import datetime
from django.http import HttpResponseRedirect,JsonResponse,HttpResponseNotFound
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import hashlib
from django.core.mail import send_mail
from cap.models import Organisation
import constants
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
		response['page']='home'
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
	if utype == 'CAP_member':
		cusers=CapMember.objects.values_list('capmember', flat=True).filter(capadmin=request.user)
		users=User.objects.filter(pk__in=set(cusers))
	response['ousers']=users
	response['utype']=utype
	response['page']='onestage'
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
		if utype == 'CAP_member':
			rurl=rurl+str(request.user.id)+'/'
		url=constants.BASE_URL+rurl
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
					userp.phone=request.POST['telephone']
					userp.description=request.POST['description']
					userp.usertype=utype
					if request.FILES['picture']:
						userp.profilepicture=request.FILES['picture']
					else:
						userp.profilepicture='default.jpg'
					userp.lastLoginDate=datetime.now()
					userp.save()
					if utype == 'Organisation':
						org=Organisation()
						org.user=user
						org.name=request.POST['first_name']
						org.description=request.POST['description']
						if request.FILES['picture']:
							org.logo=request.FILES['picture']
						else:
							org.logo='default.jpg'
						org.address=request.POST['address']
						org.save()
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


def newusercap(request,utype,password,email,capadminid):
	print "newusercap"
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
					userp.phone=request.POST['telephone']
					userp.description=request.POST['description']
					userp.usertype=utype
					if request.FILES['picture']:
						userp.profilepicture=request.FILES['picture']
					else:
						userp.profilepicture='default.jpg'
					userp.lastLoginDate=datetime.now()
					userp.save()
					cap=CapMember()
					cap.capadmin=User.objects.get(id=capadminid)
					cap.capmember=user
					cap.save()
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
	response['capadminid']=capadminid
	response['capadmin']=User.objects.get(id=capadminid)
	return render(request,'site/registernewuser.html',response)


def viewprofile(request,utype,userid):
	response={}
	try:
		user=User.objects.get(id=userid)
	except:
		return HttpResponseNotFound('<h1>Not found</h1>')
	if user.userprofile.usertype == utype:
		if utype == 'Organisation':
			"""
			This is the part for the Organisation view
			Need to show the cost made by organization and the platforms its collabarating with
			"""
		elif utype == 'CAP':
			"""
			This is the part for the CAP view
			Need to show volunteers for the Campus ambassador of the college
			and the platforms conducted by them
			"""
		elif utype == 'Onestage':
			"""
			Need to show the Onestage main member
			Need to show the role and the description
			"""
		response['vuser']=user
		response['page']=utype.lower()
		return render(request,'site/viewprofile.html',response)
	else:
		return HttpResponseNotFound('<h1>Not found</h1>')











		

