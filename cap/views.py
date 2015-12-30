from django.shortcuts import render
from cap.models import Platform
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
			if request.FILES['banner']:
				post.banner=request.FILES['banner']
			else:
				post.banner='default.jpg'
			post.save()
			return HttpResponseRedirect('/viewcollegeplatforms')
		else:
			print form.errors
			response['message']='Please check the form again'
	else:
		form=PlaformForm()
		response['form']=form
	return render(request,'site/addplatform.html',response)

