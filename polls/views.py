from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy

from django.views.generic import RedirectView, ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django import forms

from .models import PollUser, Choice, Question, SignupForm, LoginForm, QuestionForm, ChoiceForm

from django.contrib.auth import authenticate, login, logout

class SignupView(CreateView):
	template_name = "polls/signup.html"
	model = PollUser
	form_class = SignupForm

	def form_valid(self, form):
		self.object = form.save()
		username = form.cleaned_data["username"]
		password = form.cleaned_data["password"]

		polluser = authenticate(username=username, password=password)
		if polluser != None:
			if polluser.is_active:
				login(self.request, polluser)
				messages.add_message(self.request, messages.SUCCESS, "Welcome aboard, %s!"%username)
			else:
				messages.add_message(self.request, messages.ERROR, "Oops, it appears that your account started disabled.")
		else:
			messages.add_message(self.request, messages.ERROR, "Oh no! Something went wrong. Contact your favorite developer to fix this.")
			return redirect("polls:signup", permanent=False)

		return redirect("polls:index")

class LoginView(FormView):
	template_name = "polls/login.html"
	form_class = LoginForm
	
	def form_valid(self, form):
		username = form.cleaned_data["username"]
		password = form.cleaned_data["password"]
		
		polluser = authenticate(username=username, password=password)
		if polluser != None:
			if polluser.is_active:
				login(self.request, polluser)
				messages.add_message(self.request, messages.SUCCESS, "Welcome back, %s!"%username)
			else:
				messages.add_message(self.request, messages.ERROR, "Oops, it appears that your account has been disabled.")
		else:
			messages.add_message(self.request, messages.ERROR, "Invalid username/password, try again.")
			return redirect("polls:login", permanent=False)

		return redirect("polls:index")

class LogoutView(RedirectView):
	"""
	RedirectView: Method flowchart:
		1.dispatch()
		2.http_method_not_allowed()
		3.get_redirect_url()
	"""
	permanent = False
	pattern_name = "polls:index"
	
	def dispatch(self, request, *args, **kwargs):
		username = request.user.username
		logout(request)
		if not isinstance(request.user, PollUser):
			messages.add_message(request, messages.SUCCESS, "See you soon, %s!"%username)
		else:
			messages.add_message(request, messages.SUCCESS, "Sorry, we could not log you out.")
		return super(LogoutView, self).dispatch(request, *args, **kwargs)

class UserUpdate(UpdateView):
	model = PollUser
	form_class = SignupForm

class CreatePollView(CreateView):
	model = Question
	form_class = QuestionForm

class UpdatePollView(UpdateView):
	model = Question
	form_class = QuestionForm

class DeletePollView(DeleteView):
	model = Question

class IndexView(ListView):
	"""
	ListView: Method flowchart:
		1.dispatch()
		2.http_method_not_allowed()
		3.get_template_names()
		4.get_queryset()
		5.get_context_object_name()
		6.get_context_data()
		7.get()
		8.render_to_response()
	"""
	model = Question
	template_name = "polls/index.html"
	context_object_name = "poll_list"
	
	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context.update(polluser=self.request.user)
		return context

class VoteView(UpdateView):
	pass
class ResultsView(DetailView):
	pass
