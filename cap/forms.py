from django import forms
from django.forms import widgets
from django.forms import ModelForm
from django.contrib.auth.models import User
from cap.models import Platform,Organisation
from django.contrib import admin


class PlaformForm(forms.ModelForm):
	organisations= forms.ModelMultipleChoiceField(queryset=Organisation.objects.all(),widget=forms.CheckboxSelectMultiple(),required=False)
	class Meta:
		model=Platform
		exclude=('addedby','date_added',)