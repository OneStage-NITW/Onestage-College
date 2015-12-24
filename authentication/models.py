from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def get_image_path(instance,filename):
    return 'userprofile/user{0}.jpg'.format(instance.user.id)

class UserProfile(models.Model):
	TYPE_CHOICES = (
	    ('Organisation', 'Organisation'),
	    ('CAP', 'CAP'),
	    ('Onestage','Onestage')
	)
	user = models.OneToOneField(User)
	collegeName = models.CharField(max_length=128,default="NIT")
	signUpDate = models.DateField(auto_now=True)
	ipaddress = models.URLField(max_length=25)
	lastLoginDate = models.DateTimeField(blank=True)
	loggedIn=models.BooleanField(default=False)
	usertype=models.CharField(max_length=180,choices=TYPE_CHOICES,default='organisation')
	profilepicture=models.ImageField(upload_to=get_image_path, null=True,blank=True)
	role=models.CharField(max_length=180,null=True)
	description=models.CharField(max_length=180,null=True)
	phone=models.CharField(max_length=180,null=True)
	def __unicode__(self):
		return self.user.username