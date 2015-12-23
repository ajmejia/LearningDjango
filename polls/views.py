from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy

from django.views.generic import RedirectView, ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django import forms

from .models import PollUser, Choice, Question, SignupForm, LoginForm, UserAccountForm, QuestionForm, ChoiceFormset

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
			messages.add_message(request, messages.SUCCESS, "Sorry, we could not log you out. Contact your favorite developer to fix this.")
		return super(LogoutView, self).dispatch(request, *args, **kwargs)

class UserAccountView(UpdateView):
	template_name = "polls/user_account.html"
	model = PollUser
	form_class = UserAccountForm

	def form_valid(self, form):
		self.object = form.save()

		messages.add_message(self.request, messages.SUCCESS, "Your account was updated.")
		return redirect("polls:index")

class CreatePollView(FormView):
	template_name = "polls/create_poll.html"

	def get(self, request):
		return render(request, self.template_name, context={"question_form": QuestionForm(), "choice_forms": ChoiceFormset()})

	def post(self, request):
		question_form = QuestionForm(request.POST)
		choice_forms = ChoiceFormset(request.POST)

		if question_form.is_valid() and choice_forms.is_valid():
			return self.form_valid((question_form, choice_forms))
		else:
			return self.form_invalid((question_form, choice_forms))

	def get_form(self):
		return QuestionForm(), ChoiceFormset()

	def form_invalid(self, forms):
		question_form, choice_forms = forms
		return render(self.request, self.template_name, context={"question_form": question_form, "choice_forms": choice_forms})

	def form_valid(self, forms):
		question_form, choice_forms = forms

		current_user = PollUser.objects.get(id=self.request.user.id)
		question = Question(question=question_form.cleaned_data["question"],
		                    created_on=timezone.now(),
		                    created_by=current_user,
		                   )
		question.save()
		choices = []
		for choice_form in choice_forms:
			choice = Choice(for_question_id=question.id, choice=choice_form.cleaned_data["choice"])
			choice.save()
			
		return redirect("polls:index")

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

class VotePollView(UpdateView):
	pass

class ResultsPollView(DetailView):
	pass
