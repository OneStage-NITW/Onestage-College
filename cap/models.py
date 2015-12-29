from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

def get_image_path(instance,filename):
    return 'organisation{0}'.format(instance.name)

def get_image_path2(instance,filename):
    return 'platform{0}'.format(instance.name)

class Organisation(models.Model):
	user=models.OneToOneField(User,related_name='orguser')
	name=models.CharField(max_length=180,unique=True)
	description=models.TextField()
	logo=models.ImageField(upload_to=get_image_path, null=True,blank=True)
	address=models.TextField()
	def __unicode__(self):
		return self.name

class Platform(models.Model):
	name = models.CharField(max_length=180)
	date_added=models.DateTimeField(auto_now=True)
	amount=models.CharField(max_length=180)
	logistics=models.TextField()
	date=models.DateField()
	description=models.TextField()
	venue=models.CharField(max_length=180)
	organisations=models.ManyToManyField(Organisation,related_name="platform_orgs",blank=True)
	addedby=models.ForeignKey(User,related_name='platformadmin')
	banner=models.ImageField(upload_to=get_image_path2,blank=True)
	def __unicode__(self):
		return self.name


class PlatformDetails(models.Model):
	platform=models.OneToOneField(Platform)
	amount_collected=models.CharField(max_length=180)
	feedback=models.TextField()
	no_of_people=models.CharField(max_length=180)
	def __unicode__(self):
		return self.platform.name

class Volunteers(models.Model):
	college=models.ForeignKey(User,related_name='collegeadmin')
	vol=models.ForeignKey(User,related_name='volunteer')
	def __unicode__(self):
		return self.college.first_name+" : "+self.vol.first_name


    


    


