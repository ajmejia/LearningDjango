from django.shortcuts import render

# Create your views here.
#---------------------------------------------------------------
#- This is the view file, where the contents of a web page is
#- defined. This site, for instance, will have the following
#- views:
#-    * index
#-    * detail
#-    * results
#-    * vote
#---------------------------------------------------------------
from django.http import HttpResponse
from .models import Question

def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[:5]   #- show latest 5 questions
  output = ', '.join([p.question_text for p in latest_question_list])
  return HttpResponse(output)

def detail(request, question_id):
  return HttpResponse("You're looking at question %s."%question_id)

def results(request, question_id):
  return HttpResponse("You're looking at the results of question %s."%question_id)

def vote(request, question_id):
  return HttpResponse("You're voting on question %s."%question_id)
