from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy

from django.views.generic import RedirectView, ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User, Choice, Poll, PollForm, ChoiceFormset, VoteForm

from django.contrib.auth import authenticate, login, logout

class SignupView(CreateView):
	template_name = "polls/signup.html"
	model = User
	form_class = UserCreationForm

	def form_valid(self, form):
		self.object = form.save()
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password1")

		user = authenticate(username=username, password=password)
		if user != None:
			if user.is_active:
				login(self.request, user)
				messages.add_message(self.request, messages.SUCCESS, "Welcome aboard, %s!"%username)
			else:
				messages.add_message(self.request, messages.ERROR, "Oops, it appears that your account started disabled.")
		else:
			messages.add_message(self.request, messages.ERROR, "Oh no! Something went wrong. Contact your favorite developer to fix this.")
			return redirect("polls:signup", permanent=False)

		return redirect("polls:index")
		
class UserAccountView(UpdateView):
	template_name = "polls/user_account.html"
	model = User
	form_class = UserChangeForm

	def form_valid(self, form):
		self.object = form.save()

		messages.add_message(self.request, messages.SUCCESS, "Your account was updated.")
		return redirect("polls:index")

# =========================================================================================================================
# REPLACE THIS BLOCK WITH THE VIEWS IN django.contrib.auth.views ==========================================================

#class LoginView(FormView):
#	template_name = "polls/login.html"
#	form_class = LoginForm
	
#	def form_valid(self, form):
#		username = form.cleaned_data["username"]
#		password = form.cleaned_data["password"]
		
#		polluser = authenticate(username=username, password=password)
#		if polluser != None:
#			if polluser.is_active:
#				login(self.request, polluser)
#				messages.add_message(self.request, messages.SUCCESS, "Welcome back, %s!"%username)
#			else:
#				messages.add_message(self.request, messages.ERROR, "Oops, it appears that your account has been disabled.")
#		else:
#			messages.add_message(self.request, messages.ERROR, "Invalid username/password, try again.")
#			return redirect("polls:login", permanent=False)

#		return redirect("polls:index")

#class LogoutView(RedirectView):
#	"""
#	RedirectView: Method flowchart:
#		1.dispatch()
#		2.http_method_not_allowed()
#		3.get_redirect_url()
#	"""
#	permanent = False
#	pattern_name = "polls:index"
	
#	def dispatch(self, request, *args, **kwargs):
#		username = request.user.username
#		logout(request)
#		if not isinstance(request.user, PollUser):
#			messages.add_message(request, messages.SUCCESS, "See you soon, %s!"%username)
#		else:
#			messages.add_message(request, messages.SUCCESS, "Sorry, we could not log you out. Contact your favorite developer to fix this.")
#		return super(LogoutView, self).dispatch(request, *args, **kwargs)
# =========================================================================================================================

class CreatePollView(FormView):
	template_name = "polls/create_poll.html"

	def get(self, request):
		return render(request, self.template_name, context={"question_form": PollForm(), "choice_forms": ChoiceFormset()})

	def post(self, request):
		question_form = PollForm(request.POST)
		choice_forms = ChoiceFormset(request.POST)

		if question_form.is_valid() and choice_forms.is_valid():
			return self.form_valid((question_form, choice_forms))
		else:
			return self.form_invalid((question_form, choice_forms))

	def get_form(self):
		return PollForm(), ChoiceFormset()

	def form_invalid(self, forms):
		question_form, choice_forms = forms
		return render(self.request, self.template_name, context={"question_form": question_form, "choice_forms": choice_forms})

	def form_valid(self, forms):
		question_form, choice_forms = forms

		current_user = User.objects.get(id=self.request.user.id)
		question = Poll(question=question_form.cleaned_data["question"],
		                    created_on=timezone.now(),
		                    created_by=current_user,
		                   )
		question.save()
		choices = []
		for choice_form in choice_forms:
			choice = Choice(for_question_id=question.id, choice=choice_form.cleaned_data["choice"])
			choice.save()
			
		return redirect("polls:index")

class UpdatePollView(FormView):
	template_name = "polls/update_poll.html"

	def dispatch(self, request, *args, **kwargs):
		self.question = Poll.objects.get(pk=kwargs.pop("pk"))
		
		self.initial_question = {"question": self.question.question}
		self.choices = self.question.choice_set.all()
		self.initial_choices_values = [c.choice for c in self.choices]
		self.num_choices = self.choices.count()
		
		self.initial_formset = [{"form-TOTAL_FORMS": self.num_choices,
		                         "form-INITIAL_FORMS": self.num_choices,
		                         "form-MIN_NUM_FORMS": 2,
		                         "form-MAX_NUM_FORMS": 1000}]

		self.initial_choices = []
		for i in xrange(self.num_choices):
			self.initial_choices.append(dict(choice=self.choices[i].choice))
			self.initial_formset.append({"form-"+str(i)+"-choice": self.choices[i].choice})

		return super(UpdatePollView, self).dispatch(request, *args, **kwargs)

	def get(self, request):
		question_form = PollForm(initial=self.initial_question)
		choice_forms = ChoiceFormset(initial=self.initial_choices)
		
		return render(request, self.template_name, context={"question_form": question_form,
		                                                    "choice_forms": choice_forms,
		                                                    "poll": self.question})

	def post(self, request):
		question_form = PollForm(data=request.POST, initial=self.initial_question)
		choice_forms = ChoiceFormset(data=request.POST, initial=self.initial_formset)
		
		if question_form.is_valid() and choice_forms.is_valid():
			return self.form_valid((question_form, choice_forms))
		else:
			return self.form_invalid((question_form, choice_forms))

	def form_invalid(self, forms):
		question_form, choice_forms = forms
		return render(self.request, self.template_name, context={"question_form": question_form, "choice_forms": choice_forms})

	def form_valid(self, forms):
		question_form, choice_forms = forms

		if question_form.has_changed():
			self.question.question = question_form.cleaned_data["question"]
			self.question.save()

		current_choices = [d["choice"] for d in choice_forms.cleaned_data]
		current_choices_num = choice_forms.total_form_count()

		if choice_forms.has_changed():
			if self.num_choices == current_choices_num:
				for i, choice_form in enumerate(choice_forms):
					if choice_form.has_changed():
						self.choices[i].choice = choice_form.cleaned_data["choice"]
						self.choices[i].save()
			else:
				diff_num = current_choices_num - self.num_choices
				
				if diff_num < 0:
					i = 0
					while diff_num < 0:
						del_choice = self.choices[i]
						if not del_choice.choice in current_choices:
							del_choice.delete()
							diff_num += 1
						i += 1
					for i, choice_form in enumerate(choice_forms):
						if not choice_form.cleaned_data["choice"] in self.initial_choices_values:
							self.choices[i].choice = choice_form.cleaned_data["choice"]
							self.choices[i].save()
				else:
					for i, choice_form in enumerate(choice_forms):
						if choice_form.has_changed():
							try:
								self.choices[i].choice = choice_form.cleaned_data["choice"]
								self.choices[i].save()
							except IndexError:
								new_choice = Choice(for_question_id=self.question.id, choice=choice_form.cleaned_data["choice"])
								new_choice.save()
			
		return redirect("polls:index")

class DeletePollView(RedirectView):
	permanent = False
	pattern_name = "polls:index"
	
	def dispatch(self, request, *args, **kwargs):
		question = Poll.objects.get(pk=kwargs.pop("pk"))
		question.delete()
		return super(DeletePollView, self).dispatch(request, *args, **kwargs)

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
	model = Poll
	template_name = "polls/index.html"
	context_object_name = "poll_list"
	
	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context.update(polluser=self.request.user)
		return context

class VotePollView(FormView):
	template_name = "polls/vote.html"
	form_class = VoteForm

	def dispatch(self, request, *args, **kwargs):
		self.question = Poll.objects.get(pk=kwargs.pop("pk"))
		self.choices = self.question.get_choices(for_form=True)

		return super(VotePollView, self).dispatch(request, *args, **kwargs)

	def get_form(self):
		form = super(VotePollView, self).get_form()
		form.fields["choice_set"].choices = self.choices
		return form

	def get_context_data(self, **kwargs):
		kwargs.update(poll=self.question)
		return super(VotePollView, self).get_context_data(**kwargs)

	def form_valid(self, form):
		selected_choice = self.question.choice_set.get(pk=form.cleaned_data.get('choice_set'))
		selected_choice.votes += 1
		selected_choice.save()
		return redirect("polls:index")

class ResultsPollView(DetailView):
	template_name = "polls/results.html"
	model = Poll
