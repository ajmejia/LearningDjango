from django.test import TestCase
import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from .models import Question, User

# Create your tests here.
#---------------------------------------------------------------
#- This file contains the automated tests I've created to expose
#- bugs in my apps.
#- The philosophy behind this is to create test cases where I
#- know my apps would fail eventually. These tests will run on
#- databases automatically created/destroyed during the tests
#- run.
#---------------------------------------------------------------

USERNAME = 'name'
EMAIL = 'name@somewhere.com'
PASSWORD = '1234567'

def create_question(question_text, days):
  """
  Creates a question with the given question_text and
  and a publication date with an offset of days from now.
  """
  time = timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_text=question_text, pub_date=time)

class SignupViewTests(TestCase):
	
	def test_create_and_login_user(self):
		"""Can create & login user?"""
		response = self.client.post(reverse('polls:signup'), {'username': USERNAME, 'email': EMAIL,
		                                                      'password1': PASSWORD, 'password2': PASSWORD,
		                                                     }, follow=True
		                           )
		url, status = response.redirect_chain[0]
		self.assertEqual(url, 'http://testserver/polls/')
		self.assertEqual(status, 302)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, USERNAME)
		self.assertEqual(int(self.client.session['_auth_user_id']), User.objects.get(username=USERNAME).id)
		self.assertContains(response, 'Welcome aboard!')

	def test_signup_with_missing_username(self):
		"""Display the message: 'This field is required.'"""
		response = self.client.post(reverse('polls:signup'), {'email': EMAIL, 'password1': PASSWORD,
		                                                      'password2': PASSWORD,
		                                                     }, follow=True
		                           )
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'This field is required.')

	def test_signup_with_missing_email(self):
		"""Display the message: 'This field is required.'"""
		response = self.client.post(reverse('polls:signup'), {'username': USERNAME, 'password1': PASSWORD,
		                                                      'password2': PASSWORD,
		                                                     }, follow=True
		                           )
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'This field is required.')

	def test_signup_with_missing_password1(self):
		"""Display the message: 'This field is required.'"""
		response = self.client.post(reverse('polls:signup'), {'username': USERNAME, 'email': EMAIL,
		                                                      'password2': PASSWORD,
		                                                     }, follow=True
		                           )
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'This field is required.')

	def test_signup_with_missing_password2(self):
		"""Display the message: 'This field is required.'"""
		response = self.client.post(reverse('polls:signup'), {'username': USERNAME, 'email': EMAIL,
		                                                      'password1': PASSWORD,
		                                                     }, follow=True
		                           )
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'This field is required.')

	def test_signup_with_mismatching_passwords(self):
		"""Display the message: 'Passwords does not match.'"""
		response = self.client.post(reverse('polls:signup'), {'username': USERNAME, 'email': EMAIL,
		                                                      'password1': PASSWORD, 'password2': PASSWORD+"8",
		                                                     }, follow=True
		                           )
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Passwords does not match.')

	def test_signup_while_logged_in(self):
		"""Display the message: 'You are already logged in as'"""
		response = self.client.post(reverse('polls:signup'), {'username': USERNAME, 'email': EMAIL,
		                                                      'password1': PASSWORD, 'password2': PASSWORD,
		                                                     }, follow=True
		                           )
		self.assertEqual(int(self.client.session['_auth_user_id']), User.objects.get(username=USERNAME).id)
		response = self.client.get(reverse('polls:signup'), {'username': USERNAME, 'email': EMAIL,
		                                                      'password1': PASSWORD, 'password2': PASSWORD,
		                                                     }, follow=True
		                           )
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'You are already logged in as %s'%USERNAME)

	def test_signup_with_existing_username(self):
		"""Display the message: 'This username is already taken.'"""
		user = User.objects.create_user(username=USERNAME, email=EMAIL, password=PASSWORD)
		response = self.client.post(reverse('polls:signup'), {'username': USERNAME, 'email': "1"+EMAIL,
		                                                      'password1': PASSWORD, 'password2': PASSWORD,
		                                                     }, follow=True
		                           )
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'This username is already taken.')

	def test_signup_with_existing_email(self):
		"""Display the message: 'This email is already in use.'"""
		user = User.objects.create_user(username=USERNAME, email=EMAIL, password=PASSWORD)
		response = self.client.post(reverse('polls:signup'), {'username': "1"+USERNAME, 'email': EMAIL,
		                                                      'password1': PASSWORD, 'password2': PASSWORD,
		                                                     }, follow=True
		                           )
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'This email is already in use.')

class LoginViewTests(TestCase):

	def test_login_non_existing_user(self):
		"""Can't login NON EXISTING user"""
		response = self.client.post(reverse('polls:login'), {'username': USERNAME, 'password': PASSWORD},
		                            follow=True)
		url, status = response.redirect_chain[0]
		self.assertEqual(url, 'http://testserver/polls/login')
		self.assertEqual(status, 302)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Invalid username/password, try again.')
		
	def test_login_existing_user(self):
		"""Can login EXISTING user"""
		user = User.objects.create_user(username=USERNAME, email=EMAIL, password=PASSWORD)
		response = self.client.post(reverse('polls:login'), {'username': USERNAME, 'password': PASSWORD},
		                            follow=True)
		url, status = response.redirect_chain[0]
		self.assertEqual(url, 'http://testserver/polls/')
		self.assertEqual(status, 302)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Welcome back!')

	def test_login_with_missing_username_on_non_existing_user(self):
		"""Display the message: 'This field is required.'"""
		response = self.client.post(reverse('polls:login'), {'password': PASSWORD},
		                            follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'This field is required.')

	def test_login_with_missing_password_on_non_existing_user(self):
		"""Display the message: 'This field is required.'"""
		response = self.client.post(reverse('polls:login'), {'username': USERNAME},
		                            follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'This field is required.')

	def test_login_with_missing_username_on_existing_user(self):
		"""Display the message: 'This field is required.'"""
		user = User.objects.create_user(username=USERNAME, email=EMAIL, password=PASSWORD)
		response = self.client.post(reverse('polls:login'), {'password': PASSWORD},
		                            follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'This field is required.')

	def test_login_with_missing_password_on_existing_user(self):
		"""Display the message: 'This field is required.'"""
		user = User.objects.create_user(username=USERNAME, email=EMAIL, password=PASSWORD)
		response = self.client.post(reverse('polls:login'), {'username': USERNAME},
		                            follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'This field is required.')

	def test_login_with_incorrect_username(self):
		"""Display the message: 'Invalid username/password, try again.'"""
		user = User.objects.create_user(username=USERNAME, email=EMAIL, password=PASSWORD)
		response = self.client.post(reverse('polls:login'), {'username': USERNAME+'a', 'password': PASSWORD},
		                            follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Invalid username/password, try again.')
		
	def test_login_with_incorrect_password(self):
		"""Display the message: 'Invalid username/password, try again.'"""
		user = User.objects.create_user(username=USERNAME, email=EMAIL, password=PASSWORD)
		response = self.client.post(reverse('polls:login'), {'username': USERNAME, 'password': PASSWORD+'abc'},
		                            follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Invalid username/password, try again.')

	def test_login_with_deactivated_user(self):
		"""Display the message: 'Sorry, your account has been disabled from this site.'"""
		user = User.objects.create_user(username=USERNAME, email=EMAIL, password=PASSWORD)
		user.is_active = False
		user.save()
		response = self.client.post(reverse('polls:login'), {'username': USERNAME, 'password': PASSWORD},
		                            follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Sorry, your account has been disabled from this site.')

	def test_login_with_another_account_logged_in(self):
		"""Display the message: 'You are already logged in as'"""
		user1 = User.objects.create_user(username="1"+USERNAME, email="1"+EMAIL, password=PASSWORD)
		user2 = User.objects.create_user(username="2"+USERNAME, email="2"+EMAIL, password=PASSWORD)
		
		response = self.client.post(reverse('polls:login'), {'username': user1.username, 'password': PASSWORD},
		                            follow=True)
		self.assertEqual(int(self.client.session['_auth_user_id']), user1.id)

		response = self.client.get(reverse('polls:login'), follow=True)
		url, status = response.redirect_chain[0]
		self.assertEqual(url, 'http://testserver/polls/')
		self.assertEqual(status, 302)  
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'You are already logged in as %s'%user1.username)

	def test_login_with_same_account_logged_in(self):
		"""Display the message: 'You are already logged in as'"""
		user = User.objects.create_user(username=USERNAME, email=EMAIL, password=PASSWORD)

		response = self.client.post(reverse('polls:login'), {'username': user.username, 'password': PASSWORD},
		                            follow=True)
		self.assertEqual(int(self.client.session['_auth_user_id']), user.id)

		response = self.client.get(reverse('polls:login'), follow=True)
		url, status = response.redirect_chain[0]
		self.assertEqual(url, 'http://testserver/polls/')
		self.assertEqual(status, 302)  
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'You are already logged in as %s'%user.username)

class QuestionViewTests(TestCase):

  def test_index_view_with_no_questions(self):
    """If no questions exist, display an appropiate message."""
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)                             #- Check the page actually exist.
    self.assertContains(response, 'No polls are available')                 #- Check there's an human-friendly message/warning.
    self.assertQuerysetEqual(response.context['latest_question_list'], [])  #- Check there's no question in the poll jet.

  def test_index_view_with_a_past_question(self):
    """Past questions should be displayed on the index page."""
    create_question(question_text='Past question.', days=-30)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(response.context['latest_question_list'],
                             ['<Question: Past question.>']
                            )

  def test_index_with_a_future_question(self):
    """Future questions should NOT be displayed on index page."""
    create_question(question_text='Future question.', days=30)
    response = self.client.get(reverse('polls:index'))
    self.assertContains(response, 'No polls are available', status_code=200)
    self.assertQuerysetEqual(response.context['latest_question_list'], [])

  def test_index_view_with_future_question_and_past_question(self):
    """Even if both, past and future questions, only past should display in index."""
    create_question(question_text='Past question.', days=-30)
    create_question(question_text='Future question.', days=30)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(response.context['latest_question_list'],
                             ['<Question: Past question.>']
                            )

  def test_index_view_with_two_past_questions(self):
    """Multiple questions should be displayed."""
    create_question(question_text='Past question 1.', days=-30)
    create_question(question_text='Past question 2.', days=-5)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(response.context['latest_question_list'],
                             ['<Question: Past question 2.>',
                              '<Question: Past question 1.>']
                            )


class QuestionVoteTests(TestCase):
  
  def test_vote_view_with_a_future_question(self):
    """Should return a 404 page."""
    future_question = create_question(question_text='Future question.', days=5)
    response = self.client.get(reverse('polls:vote', args=(future_question.id,)))
    self.assertEqual(response.status_code, 404)

  def test_vote_view_with_a_past_question(self):
    """Past questions should should have a vote view."""
    past_question = create_question(question_text='Past question.', days=-5)
    response = self.client.get(reverse('polls:vote', args=(past_question.id,)))
    self.assertContains(response, past_question.question_text, status_code=200)


class QuestionResultsTests(TestCase):
  
  def test_results_view_with_a_future_question(self):
    """Should return a 404 page."""
    future_question = create_question('Future question.', 5)
    response = self.client.get(reverse('polls:results', args=(future_question.id,)))
    self.assertEqual(response.status_code, 404)

  def test_results_view_with_a_past_question(self):
    """Past questions should be rendered by the results view."""
    past_question = create_question('Past question.', -5)
    response = self.client.get(reverse('polls:results', args=(past_question.id,)))
    self.assertContains(response, past_question.question_text, status_code=200)


class QuestionModelTests(TestCase):

  def test_was_published_recently_with_future_question(self):
    """Should return False for Questions published in the future."""
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(pub_date=time)
    self.assertEqual(future_question.was_published_recently(), False)

  def test_was_published_recently_with_old_question(self):
    """
    Should return False for questions whose published date is older
    than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=30)
    old_question = Question(pub_date=time)
    self.assertEqual(old_question.was_published_recently(), False)

  def test_was_published_recently_with_recent_question(self):
    """Should return True for questions published within the last day."""
    time = timezone.now() - datetime.timedelta(hours=1)
    recent_question = Question(pub_date=time)
    self.assertEqual(recent_question.was_published_recently(), True)
