from django.shortcuts import render
from cap.models import Platform,OrgMap
from cap.forms import PlaformForm, PlatformDetailsForm
from django.http import HttpResponseRedirect,JsonResponse,HttpResponseNotFound
from datetime import datetime
import zipfile
import os
import shutil


# Create your views here.

def viewplatforms(request):
	response={}
	p=Platform.objects.all()
	response['page']='platforms'
	if len(p) > 0:
		response['platforms']=p
	return render(request,'site/viewplatforms.html',response)

def viewcollegeplatforms(request):
	response={}
	p=Platform.objects.filter(addedby=request.user)
	response['page']='capplatforms'
	if len(p) > 0:
		response['platforms']=p
	response['date']=datetime.now().date()
	return render(request,'site/viewplatforms.html',response)


def addplatform(request):
	response={}
	if request.method == 'POST':
		form=PlaformForm(request.POST)
		if form.is_valid():
			post=form.save(commit=False)
			post.addedby=request.user
			post.lat=request.POST['latitude']
			post.longt=request.POST['longitude']
			post.save()
			form.save_m2m()
			if request.FILES['banner']:
				post.banner=request.FILES['banner']
			else:
				post.banner='default.jpg'
			post.save()
			plat=Platform.objects.get(id=post.id)
			for org in plat.organisations.all():
				omap=OrgMap()
				omap.org=org
				omap.platform=plat
				omap.save()
			return HttpResponseRedirect('/viewcollegeplatforms')
		else:
			print form.errors
			response['message']='Please check the form again'
	else:
		form=PlaformForm()
		response['form']=form
	return render(request,'site/addplatform.html',response)


def editplatform(request,pid):
	response={}
	plat=Platform.objects.get(id=pid)
	if request.method == 'POST':
		form=PlaformForm(request.POST,instance=plat)
		if form.is_valid():
			post=form.save(commit=False)
			post.addedby=request.user
			post.lat=request.POST['latitude']
			post.longt=request.POST['longitude']
			post.save()
			form.save_m2m()
			plat=Platform.objects.get(id=post.id)
			for org in plat.organisations.all():
				try:
					OrgMap.objects.get(org=org,platform=plat)
				except:
					omap=OrgMap()
					omap.org=org
					omap.platform=plat
					omap.save()
			return HttpResponseRedirect('/viewcollegeplatforms')
		else:
			print form.errors
			response['message']='Please check the form again'
	else:
		form=PlaformForm(instance=plat)
		response['form']=form
		response['platform']=plat
	return render(request,'site/editplatform.html',response)

def deleteplatform(request,pid):
	response={}
	if request.user.userprofile.usertype == 'CAP':
		plat=Platform.objects.get(id=pid)
		if plat.addedby == request.user:
			response['message']='Successfully deleted '+ plat.name
			plat.delete()
		else:
			response['message']='Not the user who added the platform'
	else:
		response['message']='User doesnot have the permission to delete'
	return HttpResponseRedirect('/viewcollegeplatforms')


def platformrequests(request,pid):
	response={}
	plat=Platform.objects.get(id=pid)
	organisations=OrgMap.objects.filter(platform=plat)
	response['organisations']=organisations
	#Add the request from cap members here
	return render(request,'site/platformrequests.html',response)


def organisationrequests(request):
	response={}
	print request.user.orguser
	orgs=OrgMap.objects.filter(org=request.user.orguser)
	response['organisations']=orgs
	response['page']='manageorganisation'
	return render(request,'site/vieworganisationsreq.html',response)


def orgstatus(request,orgid,confirm):
	if confirm == 'accept':
		org=OrgMap.objects.get(id=orgid)
		org.confirmed = True
		org.save()
	else:
		organ=OrgMap.objects.get(id=orgid)
		plat=organ.platform
		org=organ.org
		organ.delete()
		plat.organisations.remove(org)
		plat.save()
	return HttpResponseRedirect('/organisationrequests/')

def platformend(request):
	"""
	View for rendering once the platform is over
	"""

def platformupload(request):
	"""
	Uploading a zip file of pictures to view on the site directly
	"""

def auditplatform(request,pid):
	"""
	Audit: after the platform is over
	"""
	response={}
	platform=Platform.objects.get(id=pid)
	if request.method == 'POST':
		try:
			form=PlatformDetailsForm(request.POST,instance=platform.platformdetails)
		except:
			form=PlatformDetailsForm(request.POST)
		if form.is_valid():
			audit=form.save(commit=False)
			audit.platform=platform
			print audit
			if request.FILES['upload']:
				directory=os.path.join(os.path.dirname(__file__),'../static/plaforms').replace('\\','/')+'/'+request.user.userprofile.collegeName+'/'+str(platform.id)
				if not os.path.exists(directory):
					os.makedirs(directory)
				print "Check 1 done"
				z = zipfile.ZipFile(request.FILES['upload'], "r")
				count=0
				for name in z.namelist():
					source = z.open(name)
					targetname = os.path.join(os.path.dirname(__file__),'../static/plaforms').replace('\\','/')+'/'+request.user.userprofile.collegeName+'/'+str(platform.id)+'/'+str(count)+'.'+name.split('.')[1]
					target=file(targetname, "wb")
					with source, target:
						shutil.copyfileobj(source, target)
					count=count+1
				audit.picture_folder=directory
				audit.picture_number=count
			audit.save()
			response['message']="Added the audit details and images"
		else:
			print form.errors
			response['message']=form.errors
	try:
		form=PlatformDetailsForm(instance=platform.platformdetails)
		response['picture']='plaforms'+'/'+request.user.userprofile.collegeName+'/'+str(platform.id)
		response['piccount']=""
		for i in range(0,platform.platformdetails.picture_number):
			response['piccount']=response['piccount']+str(i)
	except:
		form=PlatformDetailsForm()
	response['form']=form
	response['platform']=platform
	return render(request,'site/auditplatform.html',response)







