import datetime

from django.db import models
from django import forms
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode

# Create your models here.
#---------------------------------------------------------------
#- Models are the definitions of the data my application will
#- handle. Each model is a class (table in the database) and
#- each model will have some attributes (fileds in the table)
#- which will define the type of data and its behaviour.
#-
#- They will inherite from the Model class which defines a set
#- of properties and methods to handle the several datatypes.
#-
#- The code below will allow django to:
#-    * Create the database holding the app data.
#-    * Create the python handles to access that database.
#---------------------------------------------------------------
USERNAME_MAX_LENGTH = 10
PASSWORD_MIN_LENGTH = 7
PASSWORD_MAX_LENGTH = 20
EMAIL_MAX_LENGTH = 100

QUESTION_MAX_LENGTH = 200
CHOICE_MAX_LENGTH = 200
CHOICE_MIN_FIELDS = 2
CHOICE_MAX_FIELDS = 7

class Poll(models.Model):
	question = models.CharField(max_length=QUESTION_MAX_LENGTH)
	opened_by = models.ForeignKey(User)
	opened_on = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_on = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return force_unicode(self.question)

	def _get_choices_query(self):
		return self.choice_set.all()
		
	def get_choices(self, for_form=False):
		if for_form:
			return [(c.pk, c.choice) for c in self._get_choices_query()]
		else:
			return [c.choice for c in self._get_choices_query()]

	def get_total_votes(self):
		return sum([choice.votes for choice in self._get_choices_query()])

class Choice(models.Model):
	option = models.CharField(max_length=CHOICE_MAX_LENGTH)
	for_poll = models.ForeignKey(Poll)
	votes = models.IntegerField(default=0)
	voted_by = models.ManyToManyField(User)

	def __unicode__(self):
		return force_unicode(self.choice)

# =========================================================================================================================
# THIS BLOCK WILL BE REPLACED BY THE FORMS IN django.contrib.auth.forms ===================================================
#class SignupForm(forms.ModelForm):
#	confirm_password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, required=True, widget=forms.PasswordInput)

#	class Meta:
#		model = PollUser
#		fields = ("username", "email", "password", "confirm_password",)
#		widgets = {"password": forms.PasswordInput}

#	def clean(self):
#		super(SignupForm, self).clean()
#		data = self.cleaned_data.get("confirm_password")
#		password = self.cleaned_data.get("password")
#		if data and password and data != password:
#				raise forms.ValidationError("Passwords do not match.")

#	def save(self, commit=True):
#		user = super(SignupForm, self).save(commit=False)
#		user.set_password(self.cleaned_data["password"])
#		if commit:
#			user.save()
#		return user

#class LoginForm(forms.Form):
#	username = forms.CharField(max_length=USERNAME_MAX_LENGTH)
#	password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, widget=forms.PasswordInput)
	
#	def clean_username(self):
#		data = self.cleaned_data.get("username")
#		if data:
#			try:
#				user = PollUser.objects.get(username=data)
#			except PollUser.DoesNotExist:
#				raise forms.ValidationError("%s does not exist."%data)
#			return data			

#class UserAccountForm(forms.ModelForm):
#	password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, required=False, widget=forms.PasswordInput)
#	confirm_password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, required=False, widget=forms.PasswordInput)

#	class Meta:
#		model = PollUser
#		fields = ("first_name", "last_name", "username", "email", "password", "confirm_password",)

#	def clean(self):
#		super(UserAccountForm, self).clean()
#		data = self.cleaned_data.get("confirm_password")
#		password = self.cleaned_data.get("password")
#		if data and password and data != password:
#				raise forms.ValidationError("Passwords do not match.")
		
#	def save(self, commit=True):
#		user = super(UserAccountForm, self).save(commit=False)
#		password = self.cleaned_data.get("password")
#		if password: user.set_password(password)
#		if commit:
#			user.save()
#		return user
# =========================================================================================================================

class PollForm(forms.ModelForm):

	class Meta:
		model = Poll
		fields = ("question",)

class ChoiceForm(forms.ModelForm):

	class Meta:
		model = Choice
		fields = ("option",)

ChoiceFormset = forms.formset_factory(ChoiceForm, extra=0, min_num=2, validate_min=True)

class VoteForm(forms.Form):
	option_set = forms.ChoiceField(choices=[], widget=forms.RadioSelect)
