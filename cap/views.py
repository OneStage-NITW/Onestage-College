from django.shortcuts import render
from cap.models import Platform,OrgMap
from cap.forms import PlaformForm
from django.http import HttpResponseRedirect,JsonResponse,HttpResponseNotFound


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




