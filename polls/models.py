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

	class Meta:
		permissions = (("vote", "Can vote on polls"),
		               ("view_results", "Can watch results"))

	def __unicode__(self):
		return force_unicode(self.question)
		
	def get_choices(self, for_form=False):
		if for_form:
			return [(c.pk, c.option) for c in self.choice_set.all()]
		else:
			return [c.option for c in self.choice_set.all()]

	def get_total_votes(self):
		return sum([choice.votes for choice in self.choice_set.all()])

	def get_voters(self):
		return [user.id for user in choice.voted_by.all() for choice in self.choice_set.all()]

	def get_voters_id(self):
		return [user.id for user in choice.voted_by.all() for choice in self.choice_set.all()]

class Choice(models.Model):
	option = models.CharField(max_length=CHOICE_MAX_LENGTH)
	for_poll = models.ForeignKey(Poll)
	votes = models.IntegerField(default=0)
	voted_by = models.ManyToManyField(User)

	def __unicode__(self):
		return force_unicode(self.option)

class UserChangeForm(forms.ModelForm):
	password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, required=False, widget=forms.PasswordInput, help_text="Leave this field blank to keep the current password.")
	confirm_password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, required=False, widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ("first_name", "last_name", "username", "email", "password", "confirm_password",)

	def clean(self):
		super(UserChangeForm, self).clean()
		data = self.cleaned_data.get("confirm_password")
		password = self.cleaned_data.get("password")
		if data and password and data != password:
				raise forms.ValidationError("Passwords do not match.")
		
	def save(self, commit=True):
		user = super(UserChangeForm, self).save(commit=False)
		password = self.cleaned_data.get("password")
		if password: user.set_password(password)
		if commit:
			user.save()
		return user

class PollForm(forms.ModelForm):

	class Meta:
		model = Poll
		fields = ("question",)

class ChoiceForm(forms.ModelForm):

	class Meta:
		model = Choice
		fields = ("option",)

ChoiceFormset = forms.formset_factory(ChoiceForm, extra=0, min_num=CHOICE_MIN_FIELDS, max_num=CHOICE_MAX_FIELDS, validate_min=True, validate_max=True)

class VoteForm(forms.Form):
	option_set = forms.ChoiceField(choices=[], widget=forms.RadioSelect)
