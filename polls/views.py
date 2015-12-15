from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.urlresolvers import reverse, reverse_lazy

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
class SignupView(FormView):
	template_name = 'polls/signup.html'
	form_class = SignUpForm
	success_url = 'polls:index'

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
			return redirect(self.success_url)

class LoginView(FormView):
	template_name = 'polls/login.html'
	form_class = LogInForm
	success_url = 'polls:index'
	error_url = 'polls:index'

	def get_form_kwargs(self):
		if self.request.method == "POST":
			return dict(data=self.request.POST, error_class=SpanErrorList)
		else:
			return dict()
	
	def form_valid(self, form):
		user = authenticate(username=self.request.POST['username'], password=self.request.POST['password'])
		if user != None:
			if user.is_active:
				login(self.request, user)
				
				messages.add_message(self.request, messages.SUCCESS, 'Welcome back!')
				return redirect(self.success_url)
			else:
				messages.add_message(self.request, messages.ERROR, 'Sorry, your account has been disabled from this site.')
				return redirect(self.error_url)
		else:
			messages.add_message(self.request, messages.ERROR, 'Invalid username/password, try again.')
			return redirect('polls:login')

class LogoutView(RedirectView):
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

class DetailView(DetailView):
  model = Question
  template_name = 'polls/detail.html'

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(DetailView):
  model = Question
  template_name = 'polls/results.html'

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now())

class VoteView(FormView):

	def __init__(self, *args, **kwargs):
		super(VoteView, self).__init__(*args, **kwargs)

		self.template_name = 'polls/vote.html'
		self.form_class = ChoiceForm
		self.success_url = 'polls:results'
		self.error_url = 'polls:vote'

		self.question = get_object_or_404(Question, pk=2)                # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< OJO!!
		self.choices = self.question.choice_set.all()
		self.labels = [c.choice_text for c in self.choices]
		
	def get(self, self.request):
		return render(self.request, self.template_name, {'question': self.question})

	def get_form_kwargs(self):
		kwargs = super(VoteView, self).get_form_kwargs()
		kwargs.update({'choices': self.labels})
		print kwargs
		if self.request.method == "GET":
			return dict(data={}, choices=self.labels)
		else:
			return dict(data=self.request.POST, error_class=SpanErrorList, choices=self.labels)

	def form_valid(self, form):
		try:
			selected_choice = self.question.choice_set.get(pk=self.request.POST['choice'])
		except KeyError, selected_choice.DoesNotExist:
			messages.add_message(self.request, messages.ERROR, 'You must select one option to vote.')
			return redirect(reverse(self.error_url, kwargs={'form': form, 'pk': self.question.pk}))

		selected_choice.votes += 1
		selected_choice.save()
		return redirect(reverse(self.success_url, kwargs={'form': form, 'pk': self.question.pk}))

#def vote(request, question_id):
#  p = get_object_or_404(Question, pk=question_id)
#  try:
#    selected_choice = p.choice_set.get(pk=request.POST['choice'])         #- The request.POST is a dictionary-like object that maps the submitted
#                                                                          #- data through the post method.
#  except KeyError, Choice.DoesNotExist:
#    return render(request, 'polls/detail.html', {
#                  'question': p,
#                  'error_message': "You didn't setect a choice.",         #- This there is no option selected upon submitting, a KeyError will be raised
#                                                                          #- and the detail template will be rendered with a error message.
#                  })
#  else:
#    selected_choice.votes += 1
#    selected_choice.save()
#    return redirect(reverse('polls:results', args=(p.id,)))               #- Since the page we want to redirect to has a variable url, I used the
                                                                          #- reverse method to give the view (instead of the url) and the variable
                                                                          #- part (p.id).


