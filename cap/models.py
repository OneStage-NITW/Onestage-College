from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

def get_image_path(instance,filename):
    return 'organisation{0}'.format(instance.name)

class Platform(models.Model):
	name = models.CharField(max_length=180)
	date_added=models.DateTimeField(auto_now=True)
	amount=models.CharField(max_length=180)
	logistics=models.TextField()
	date=models.DateField()
	description=models.TextField()
	venue=models.CharField(max_length=180)
	organisations=models.CharField(max_length=300)
	addedby=models.ForeignKey(User,related_name='platformadmin')
	def __unicode__(self):
		return self.name


class PlatformDetails(models.Model):
	platform=models.OneToOneField(Platform)
	amount_collected=models.CharField(max_length=180)
	feedback=models.TextField()
	no_of_people=models.CharField(max_length=180)
	def __unicode__(self):
		return self.platform.name

class Organisation(models.Model):
	name=models.CharField(max_length=180,unique=True)
	description=models.TextField()
	logo=models.ImageField(upload_to=get_image_path, null=True,blank=True)
	address=models.TextField()
	def __unicode__(self):
		return self.name


    


    


