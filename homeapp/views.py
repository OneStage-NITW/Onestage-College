from django.shortcuts import render
from cap.models import *
from authentication.models import *
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import os

# Create your views here.


def home(request):
	return render(request,'homeappmaterial/site/home.djt',{'page':'home'})

def rendercappage(request,capid):
	"""We will be redering the cap page here. working on it """
	u=User.objects.get(id=capid)
	response={}
	response['cap']=u
	return render(request,'homeapp/site/cap.html',response)
	
def renderblog(request,blogid):
	"""Blog post rendering goes here"""


def rendergallery(request,platformid):
	p=Platform.objects.get(id=platformid)
	folder=p.platformdetails.picture_folder
	picture_number=p.platformdetails.picture_number
	response['picture']=folder
	response['piccount']=""
	for i in range(0,platform.platformdetails.picture_number):
		response['piccount']=response['piccount']+str(i)
	return render(request,'homeapp/site/gallery.html',response)


def renderplatform(request,platformid):
	p=Platform.objects.get(id=platformid)
	response={}
	response['platform']=p
	response['page']='platform'
	if p.platformdetails:
		l=[]
		index=p.platformdetails.picture_folder.find("plaforms")
		picturepath=p.platformdetails.picture_folder[index:len(p.platformdetails.picture_folder)+1]
		picturepath="/static/"+picturepath
		for i in range(0,p.platformdetails.picture_number):
			if os.path.isfile(p.platformdetails.picture_folder+"/"+str(i)+'.jpg'):
				l.append(picturepath+"/"+str(i)+".jpg")
			else:
				l.append(picturepath+"/"+str(i)+".png")
		response['numberarray']=l
	return render(request,'homeappmaterial/site/platformdesp.html',response)


def platforms(request):
	p=Platform.objects.all().order_by('-date')
	response={}
	response['platforms']=p
	response['page']='platforms'
	return render(request,'homeappmaterial/site/platforms.html',response)


def aboutus(request):
	return render(request,'homeappmaterial/site/aboutus.html',{'page': 'aboutus'})

def mission(request):
	return render(request,'homeappmaterial/site/mission.html',{'page': 'mission'})

def organisations(request):
	return render(request,'homeappmaterial/site/organisations.html',{'page': 'organisations'})

def campuses(request):
	return render(request,'homeappmaterial/site/campuses.html',{'page': 'campuses'})

def teampage(request):
	return render(request,'homeappmaterial/site/team.html',{'page': 'teampage'})


def sendfeedback(request):
	if request.method == 'POST':
		subject="Feedback: "+request.POST['firstname']+" : "+request.POST['email']
		body=request.POST['message']
		email = EmailMessage(subject, body, to=['vivekhtc25@gmail.com'])
		email.send()
	return HttpResponseRedirect('/index/')
