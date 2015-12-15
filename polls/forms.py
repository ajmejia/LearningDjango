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
		data1 = self.cleaned_data['password1']
		data2 = self.cleaned_data['password2']
		if data1 and data2 and data1 != data2: raise forms.ValidationError('Passwords do not match.')
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
	
	def __init__(self, *args, **kwargs):
		self.choices = kwargs.pop('choices')
		self.choices = zip(range(1, len(self.choices)+1), self.choices)
		super(ChoiceForm, self).__init__(*args, **kwargs)

		self.choice_text = forms.ChoiceField(choices=self.choices, widget=forms.RadioSelect)
		
