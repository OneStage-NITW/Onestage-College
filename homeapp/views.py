from django.shortcuts import render
from cap.models import *
from authentication.models import *
from django.contrib.auth.models import User

# Create your views here.


def home(request):
	return render(request,'homeapp/site/home.html',{})

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
	return render(request,'homeapp/site/platform.html',response)
