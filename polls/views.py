from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse

from django.views.generic import RedirectView, ListView, DetailView
from django.views.generic.edit import FormView
from django.utils import timezone

from .models import User, Choice, Question
from .forms import SpanErrorList, SignUpForm, LogInForm, ChoiceForm

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

# Create your views here.
#---------------------------------------------------------------
#- This is the view file, where the contents of a web page is
#- defined. This site, for instance, will have the following
#- views:
#-
#- index
#-   |____signup
#-   |____login
#-   |______create
#-   |________modify
#-   |________delete
#-   |______logout
#-   |______vote
#-            |____results
#-
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
class SignupView(FormView):
	template_name = 'polls/signup.html'
	form_class = SignUpForm
	success_url = 'polls:index'
	error_url = 'polls:index'

	def get(self, request, *args, **kwargs):
		if isinstance(request.user, User):
			messages.add_message(request, messages.ERROR, 'You are already logged in as %s'%request.user.username)
			return redirect(self.error_url, permanent=False)
		return super(LoginView, self).get(request, *args, **kwargs)

	def get_form_kwargs(self):
		if self.request.method == "POST":
			return dict(data=self.request.POST, error_class=SpanErrorList)
		else:
			return dict()

	def form_valid(self, form):
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password1']

		new_user = User.objects.create_user(username, email, password)#, pk=username)
		new_user.save()

		new_user = authenticate(username=new_user.username, password=self.request.POST['password1'])
		if new_user.is_active:
			login(self.request, new_user)

			messages.add_message(self.request, messages.SUCCESS, 'Welcome aboard!')
			return redirect(self.success_url, permanent=False)

class LoginView(FormView):
	template_name = 'polls/login.html'
	form_class = LogInForm
	success_url = 'polls:index'
	error_url = 'polls:index'

	def get(self, request, *args, **kwargs):
		if isinstance(request.user, User):
			messages.add_message(request, messages.ERROR, 'You are already logged in as %s'%request.user.username)
			return redirect(self.error_url, permanent=False)
		return super(LoginView, self).get(request, *args, **kwargs)

	def get_form_kwargs(self):
		if self.request.method == "POST":
			return dict(data=self.request.POST, error_class=SpanErrorList)
		else:
			return dict()
	
	def form_valid(self, form):
		user = authenticate(username=form.cleaned_data['username'],
		                    password=form.cleaned_data['password'])
		if user != None:
			if user.is_active:
				login(self.request, user)
				
				messages.add_message(self.request, messages.SUCCESS, 'Welcome back!')
				return redirect(self.success_url, permanent=False)
			else:
				messages.add_message(self.request, messages.ERROR, 'Sorry, your account has been disabled from this site.')
				return redirect(self.error_url, permanent=False)
		else:
			messages.add_message(self.request, messages.ERROR, 'Invalid username/password, try again.')
			return redirect('polls:login', permanent=False)

class LogoutView(RedirectView):
	permanent = False
	pattern_name = 'index'
	query_string = False

	def get_redirect_url(self, *args, **kwargs):
		try:
			logout(self.request)
			messages.add_message(self.request, messages.SUCCESS, 'See you soon!')
		except:
			messages.add_message(self.request, messages.ERROR, 'Could not logout current user.')
		finally:
			return reverse('polls:index')

class IndexView(ListView):
  template_name = 'polls/index.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class ResultsView(DetailView):
  model = Question
  template_name = 'polls/results.html'

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now())

class VoteView(FormView):
	template_name = 'polls/vote.html'
	form_class = ChoiceForm
	success_url = 'polls:results'
	error_url = 'polls:vote'

	def get(self, request, pk, *args, **kwargs):
		self.question = get_object_or_404(Question.objects.filter(pub_date__lte=timezone.now()), pk=pk)
		self.choices = self.question.choice_set.all()
		self.labels = [(i, c.choice_text) for i, c in enumerate(self.choices)]
		return super(VoteView, self).get(request, pk)
		
	def post(self, request, pk, *args, **kwargs):
		self.question = get_object_or_404(Question, pk=pk)
		self.choices = self.question.choice_set.all()
		self.labels = [(i, c.choice_text) for i, c in enumerate(self.choices)]
		return super(VoteView, self).post(request, pk)

	def get_form_kwargs(self):
		if self.request.method == "GET":
			return dict()
		else:
			return dict(data=self.request.POST, error_class=SpanErrorList)

	def get_form(self, *args, **kwargs):
		kwargs.update(self.get_form_kwargs())
		form = self.form_class(*args, **kwargs)
		form.fields['choice_text'].choices = self.labels
		form.set_question_text(self.question)
		form.set_question_pk(self.question)
		return form

	def form_valid(self, form):
		selected_choice = self.choices[int(form.cleaned_data['choice_text'])]
		selected_choice.votes += 1
		selected_choice.save()
		return redirect(reverse(self.success_url, kwargs={'pk': self.question.pk}), permanent=False)
