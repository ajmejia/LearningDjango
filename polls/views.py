from django.shortcuts import render, redirect, get_object_or_404

from django.utils import timezone
from django.utils.decorators import method_decorator

from django.views.generic import RedirectView, ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import UserCreationForm

from .models import CHOICE_MIN_FIELDS, CHOICE_MAX_FIELDS
from .models import User, Choice, Poll, UserChangeForm, PollForm, ChoiceFormset, VoteForm
from .auth import *

class SignupView(CreateView):
	template_name = "polls/signup.html"
	model = User
	form_class = UserCreationForm

	def form_valid(self, form):
		self.object = form.save()
		
		polls_permissions = Permission.objects.filter(content_type__app_label="polls")
		for polls_perm in polls_permissions: self.object.user_permissions.add(polls_perm)

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

		return redirect("polls:index", permanent=False)
		
class UserAccountView(UpdateView):
	template_name = "polls/user_account.html"
	model = User
	form_class = UserChangeForm

	@method_decorator(login_required(message="You need to be logged in before updating your account."))
	@method_decorator(user_account_ownership_required)
	def dispatch(self, request, *args, **kwargs):
		return super(UserAccountView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		self.object = form.save()

		messages.add_message(self.request, messages.SUCCESS, "Your account was updated.")
		return redirect("polls:index", permanent=False)

class CreatePollView(FormView):
	template_name = "polls/create_poll.html"

	@method_decorator(login_required(message="You need to be logged in before opening a new poll."))
	@method_decorator(permission_required(["polls.add_poll", "polls.add_choice"], raise_exception=True))
	def distpatch(self, request, *args, **kwargs):
		return super(CreatePollView, self).dispatch(request, *args, **kwargs)

	def get(self, request):
		return render(request, self.template_name, context={"question_form": PollForm(), "choice_forms": ChoiceFormset()})

	def post(self, request):
		question_form = PollForm(request.POST)
		choice_forms = ChoiceFormset(request.POST)

		if question_form.is_valid() and choice_forms.is_valid():
			return self.form_valid((question_form, choice_forms))
		else:
			return self.form_invalid((question_form, choice_forms))

	def form_invalid(self, forms):
		question_form, choice_forms = forms
		return render(self.request, self.template_name, context={"question_form": question_form, "choice_forms": choice_forms})

	def form_valid(self, forms):
		question_form, choice_forms = forms

		current_user = User.objects.get(id=self.request.user.id)
		question = Poll(question=question_form.cleaned_data["question"], opened_by=current_user)
		question.save()
		choices = []
		for choice_form in choice_forms:
			choice = Choice(for_poll_id=question.id, option=choice_form.cleaned_data["option"])
			choice.save()
			
		return redirect("polls:index", permanent=False)

class UpdatePollView(FormView):
	template_name = "polls/update_poll.html"

	@method_decorator(login_required(message="You need to be logged in before updating your polls."))
	@method_decorator(user_poll_ownership_required)
	@method_decorator(poll_no_votes_required)
	def dispatch(self, request, *args, **kwargs):
		self.question = Poll.objects.get(pk=kwargs.pop("pk"))
		
		self.initial_question = {"question": self.question.question}
		self.choices = self.question.choice_set.all()
		self.initial_choices_values = [c.option for c in self.choices]
		self.num_choices = self.choices.count()
		
		self.initial_formset = [{"form-TOTAL_FORMS": self.num_choices,
		                         "form-INITIAL_FORMS": self.num_choices,
		                         "form-MIN_NUM_FORMS": CHOICE_MIN_FIELDS,
		                         "form-MAX_NUM_FORMS": CHOICE_MAX_FIELDS}]

		self.initial_choices = []
		for i in xrange(self.num_choices):
			self.initial_choices.append(dict(option=self.choices[i].option))
			self.initial_formset.append({"form-"+str(i)+"-choice": self.choices[i].option})

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

		current_choices = [d["option"] for d in choice_forms.cleaned_data]
		current_choices_num = choice_forms.total_form_count()

		if choice_forms.has_changed():
			if self.num_choices == current_choices_num:
				for i, choice_form in enumerate(choice_forms):
					if choice_form.has_changed():
						self.choices[i].option = choice_form.cleaned_data["option"]
						self.choices[i].save()
			else:
				diff_num = current_choices_num - self.num_choices
				
				if diff_num < 0:
					i = 0
					while diff_num < 0:
						del_choice = self.choices[i]
						if not del_choice.option in current_choices:
							del_choice.delete()
							diff_num += 1
						i += 1
					for i, choice_form in enumerate(choice_forms):
						if not choice_form.cleaned_data["option"] in self.initial_choices_values:
							self.choices[i].option = choice_form.cleaned_data["option"]
							self.choices[i].save()
				else:
					for i, choice_form in enumerate(choice_forms):
						if choice_form.has_changed():
							try:
								self.choices[i].option = choice_form.cleaned_data["option"]
								self.choices[i].save()
							except IndexError:
								new_choice = Choice(for_poll_id=self.question.id, option=choice_form.cleaned_data["option"])
								new_choice.save()
			
		return redirect("polls:index", permanent=False)

class DeletePollView(RedirectView):
	permanent = False
	pattern_name = "polls:index"

	@method_decorator(login_required(message="You need to be logged in before deleting any poll."))
	@method_decorator(user_poll_ownership_required)
	@method_decorator(poll_no_votes_required)
	def dispatch(self, request, *args, **kwargs):
		question = Poll.objects.get(pk=kwargs.pop("pk"))
		question.delete()
		return super(DeletePollView, self).dispatch(request, *args, **kwargs)

class IndexView(ListView):
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

	@method_decorator(login_required(message="You need to be logged in before voting in any poll."))
	@method_decorator(permission_required("polls.vote", raise_exception=True))
	@method_decorator(user_no_vote_required)
	def dispatch(self, request, *args, **kwargs):
		self.question = Poll.objects.get(pk=kwargs.pop("pk"))
		self.choices = self.question.get_choices(for_form=True)

		return super(VotePollView, self).dispatch(request, *args, **kwargs)

	def get_form(self):
		form = super(VotePollView, self).get_form()
		form.fields["option_set"].choices = self.choices
		return form

	def get_context_data(self, **kwargs):
		kwargs.update(poll=self.question)
		return super(VotePollView, self).get_context_data(**kwargs)

	def form_valid(self, form):
		selected_choice = self.question.choice_set.get(pk=form.cleaned_data.get("option_set"))
		selected_choice.voted_by.add(self.request.user)
		selected_choice.votes = selected_choice.voted_by.count()
		selected_choice.save()
		return redirect("polls:results", permanent=False, pk=self.question.pk)

class ResultsPollView(DetailView):
	template_name = "polls/results.html"
	model = Poll

	@method_decorator(login_required(message="You need to be logged in before you can view any results."))
	@method_decorator(permission_required("polls.view_results", raise_exception=True))
	@method_decorator(user_vote_required)
	def dispatch(self, request, *args, **kwargs):
		return super(ResultsPollView, self).dispatch(request, *args, **kwargs)
