from django.shortcuts import render
from cap.models import Platform

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
		name= request.POST['name']
		amount=request.POST['amount']
		logistics=request.POST['logistics']
		date=request.POST['date']
		description=request.POST['description']
		venue=request.POST['venue']
		organization=request.POST['organization']
		addedby=request.user
		platform=Platform(name=name,amount=amount,logistics=logistics,date=date,description=description,venue=venue,organisations=organization,addedby=addedby)
		platform.save()
	return render(request,'site/addplatform.html',response)

