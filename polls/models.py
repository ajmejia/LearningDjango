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

class PollUser(User):
#	username = forms.CharField(max_length=USERNAME_MAX_LENGTH)
#	email = forms.EmailField(max_length=EMAIL_MAX_LENGTH)
#	password = forms.CharField(min_length=PASSWORD_MIN_LENGTH)

	def __unicode__(self):
		return force_unicode(self.username)

	def get_absolute_url(self):
		return reverse("polls:index")

class Question(models.Model):
	question = models.CharField(max_length=QUESTION_MAX_LENGTH)
	created_on = models.DateTimeField("date published")
	created_by = models.ForeignKey(PollUser)

	def __unicode__(self):
		return force_unicode(self.question)

class Choice(models.Model):
	for_question = models.ForeignKey(Question, verbose_name="choice for question")
	choice = models.CharField(max_length=CHOICE_MAX_LENGTH)
	votes = models.IntegerField(default=0)

	def __unicode__(self):
		return force_unicode(self.choice)

class SignupForm(forms.ModelForm):
	confirm_password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, required=True, widget=forms.PasswordInput)

	class Meta:
		model = PollUser
		fields = ("username", "email", "password", "confirm_password",)
		widgets = {"password": forms.PasswordInput}

	def clean_confirm_password(self):
		data = self.cleaned_data.get("confirm_password")
		password = self.cleaned_data.get("password")
		if data and password and data != password:
				raise forms.ValidationError("Passwords do not match.")
		return data
		
	def save(self, commit=True):
		user = super(SignupForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user

class LoginForm(forms.Form):
	username = forms.CharField(max_length=USERNAME_MAX_LENGTH)
	password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, widget=forms.PasswordInput)
	
	def clean_username(self):
		data = self.cleaned_data.get("username")
		if data:
			try:
				user = PollUser.objects.get(username=data)
			except PollUser.DoesNotExist:
				raise forms.ValidationError("%s does not exist."%data)
			return data			

class UserAccountForm(forms.ModelForm):
	confirm_password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, required=True, widget=forms.PasswordInput)

	class Meta:
		model = PollUser
		fields = ("first_name", "last_name", "username", "email", "password", "confirm_password",)
		widgets = {"password": forms.PasswordInput}

	def clean_confirm_password(self):
		data = self.cleaned_data.get("confirm_password")
		password = self.cleaned_data.get("password")
		if data and password and data != password:
				raise forms.ValidationError("Passwords do not match.")
		return data
		
	def save(self, commit=True):
		user = super(UserAccountForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user

class PollForm(forms.ModelForm):
	choice1 = forms.CharField(max_length=CHOICE_MAX_LENGTH, required=True, label="Choice 1")
	choice2 = forms.CharField(max_length=CHOICE_MAX_LENGTH, required=True, label="Choice 2")

	class Meta:
		model = Question
		fields = ("question", "choice1", "choice2")

	def save(self, request, commit=True):
		current_user = PollUser.objects.get(pk=request.user.pk)
		question = Question(question=self.cleaned_data["question"], created_on=timezone.now(), created_by=current_user)
		question.save()

		ch1 = Choice(for_question_id=question.pk, choice=self.cleaned_data["choice1"])
		ch2 = Choice(for_question_id=question.pk, choice=self.cleaned_data["choice2"])
		question.choice_set.add(ch1)
		question.choice_set.add(ch2)
		if commit:
			question.save(force_update=True)
		return question

class ChoiceForm(forms.ModelForm):

	class Meta:
		model = Choice
		fields = ("choice",)
