from django.shortcuts import render

# Create your views here.


def home(request):
	return render(request,'homeapp/site/home.html',{})

def rendercappage(request,capid):
	"""We will be redering the cap page here. working on it """
	