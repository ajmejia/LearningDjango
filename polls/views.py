from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.views import generic
from django.utils import timezone
from django import forms

from .models import Choice, Question
from django.forms.utils import ErrorList
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
#---------------------------------------------------------------
#- This is the view file, where the contents of a web page is
#- defined. This site, for instance, will have the following
#- views:
#-    * signup
#-    * login
#-    * logout
#-    * index
#-    * detail
#-    * results
#-    * vote
#-
#- For using the template facilities the import RequestContext
#- and loader is nedeed. The first class is used to import
#- the actual template (html file) into the template variable.
#- The second is used built the context object (html+request)
#- which is finally rendered with the method template.render.
#-
#- There's a shortcut to this, which consist in using the class
#- render from django.shortcuts. The implementation goes as
#- follows.
#---------------------------------------------------------------
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
			raise forms.ValidationError('This username was already taken.')
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

class SignInForm(forms.Form):
	username = forms.CharField(max_length=USERNAME_MAX_LENGTH)
	password = forms.CharField(label='Password', min_length=PASSWORD_MIN_LENGTH, widget=forms.PasswordInput)


def signup(request):
	if request.method == 'GET':
		form = SignUpForm()
		return render(request, 'polls/signup.html', {'form': form})
	elif request.method == 'POST':
		form = SignUpForm(request.POST, error_class=SpanErrorList)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password1']
			
			new_user = User.objects.create_user(username, email, password)#, pk=username)
			new_user.save()
			
			new_user = authenticate(username=new_user.username, password=request.POST['password1'])
			if new_user.is_active: login(request, new_user)
			return redirect(reverse('polls:index'))#, context_instance=RequestContext(request, {'user': new_user, 'success_message': 'Welcome aboard!',}))
		else:
			return render(request, 'polls/signup.html', {'form': form})

def signin(request):
	if request.method == "GET":
		form = SignInForm()
		return render(request, 'polls/signin.html', {'form': form})
	elif request.method == "POST":
		form = SignInForm(request.POST, error_class=SpanErrorList)
		if form.is_valid():
			user = authenticate(username=request.POST['username'], password=request.POST['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect(reverse('polls:index'))#, context_instance=RequestContext(request, {'success_message': 'Welcome back!'}))
				else:
					return redirect(reverse('polls:index'))#, context_instance=RequestContext(request, {'error_message': 'Your account has been disabled from this site.'}))
			else:
				return redirect(reverse('polls:signin'))#, context_instance=RequestContext(request, {'error_message': 'Invalid username/password, try again.'}))

def signout(request):
	logout(request)
	return redirect(reverse('polls:index'), context_instance=RequestContext(request, {'success_message: See you soon!'}))


class IndexView(generic.ListView):
  template_name = 'polls/index.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
  model = Question
  template_name = 'polls/detail.html'

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
  model = Question
  template_name = 'polls/results.html'

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
  p = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = p.choice_set.get(pk=request.POST['choice'])         #- The request.POST is a dictionary-like object that maps the submitted
                                                                          #- data through the post method.
  except KeyError, Choice.DoesNotExist:
    return render(request, 'polls/detail.html', {
                  'question': p,
                  'error_message': "You didn't setect a choice.",         #- This there is no option selected upon submitting, a KeyError will be raised
                                                                          #- and the detail template will be rendered with a error message.
                  })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return redirect(reverse('polls:results', args=(p.id,)))               #- Since the page we want to redirect to has a variable url, I used the
                                                                          #- reverse method to give the view (instead of the url) and the variable
                                                                          #- part (p.id).


