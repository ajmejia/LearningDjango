from django.test import TestCase

# Create your tests here.
#---------------------------------------------------------------
#- This file contains the automated tests I've created to expose
#- bugs in my apps.
#- The philosophy behind this is to create test cases where I
#- know my apps would fail eventually. These tests will run on
#- databases automatically created/destroyed during the tests
#- run.
#---------------------------------------------------------------
import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Question

def create_question(question_text, days):
  """
  Creates a question with the given question_text and the
  and a publication date with an offset of days from now.
  """
  time = timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_text=question_text, pub_date=time)

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


class QuestionDetailTests(TestCase):
  
  def test_detail_view_with_a_future_question(self):
    """Should return a 404 page."""
    future_question = create_question(question_text='Future question.', days=5)
    response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
    self.assertEqual(response.status_code, 404)

  def test_detail_view_with_a_past_question(self):
    """Past questions should should have a detail view."""
    past_question = create_question(question_text='Past question.', days=-5)
    response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
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



