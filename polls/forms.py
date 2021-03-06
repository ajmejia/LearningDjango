from django import forms
from django.forms.utils import ErrorList
from django.contrib.auth.models import User

USERNAME_MAX_LENGTH = 10
EMAIL_MAX_LENGTH = 50
PASSWORD_MIN_LENGTH = 7

class SpanErrorList(ErrorList):

	def __unicode__(self):
		return self.as_span()
		
	def as_span(self):
		if not self: return ""
		return " ".join([e for e in self])

class SignUpForm(forms.Form):

	username = forms.CharField(max_length=USERNAME_MAX_LENGTH)
	email = forms.EmailField(max_length=EMAIL_MAX_LENGTH)
	password1 = forms.CharField(label='Password', min_length=PASSWORD_MIN_LENGTH, widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', min_length=PASSWORD_MIN_LENGTH, widget=forms.PasswordInput)

	def clean_username(self):
		data = self.cleaned_data['username']
		try:
			user = User.objects.get(username=data)
			raise forms.ValidationError('This username is already taken.')
		except User.DoesNotExist:
			return data

	def clean_password2(self):
		try:
			data1 = self.cleaned_data['password1']
		except KeyError:
			raise forms.ValidationError('This field is required.')
		try:
			data2 = self.cleaned_data['password2']
		except KeyError:
			raise forms.ValidationError('This field is required.')

		if data1 and data2 and data1 != data2: raise forms.ValidationError('Passwords does not match.')
		return data2

	def clean_email(self):
		data = self.cleaned_data['email']
		try:
			user = User.objects.get(email=data)
			raise forms.ValidationError('This email is already in use.')
		except User.DoesNotExist:
			return data

class LogInForm(forms.Form):
	username = forms.CharField(max_length=USERNAME_MAX_LENGTH)
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

class ChoiceForm(forms.Form):	
	choice_text = forms.ChoiceField(choices=[], widget=forms.RadioSelect)
	
	def set_question_text(self, question):
		self.question_text = question.question_text

	def set_question_pk(self, question):
		self.question_pk = question.pk
