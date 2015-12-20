from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
	TYPE_CHOICES = (
	    ('Organisation', 'Organisation'),
	    ('CAP', 'CAP'),
	)
	user = models.OneToOneField(User)
	collegeName = models.CharField(max_length=128,default="NIT")
	signUpDate = models.DateField(auto_now=True)
	ipaddress = models.URLField(max_length=25)
	lastLoginDate = models.DateTimeField(blank=True)
	loggedIn=models.BooleanField(default=False)
	usertype=models.CharField(max_length=180,choices=TYPE_CHOICES,default='organisation')
	def __unicode__(self):
		return self.user.username