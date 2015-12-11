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

from .models import Question

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



