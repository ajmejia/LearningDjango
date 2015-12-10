from django.shortcuts import render, get_object_or_404

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
from django.http import HttpResponse, Http404

from .models import Question
#---------------------------------------------------------------
#- For using the template facilities the import RequestConext
#- and loader is nedeed. The first class is used to import
#- the actual template (html file) into the template variable.
#- The second is used built the context object (html+request)
#- which is finally rendered with the method template.render.
#-
#- There's a shortcut to this, which consist in using the class
#- render from django.shortcuts. The implementation goes as
#- follows.
#---------------------------------------------------------------

def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[:5]   #- select latest 5 questions.
  context = {'latest_question_list': latest_question_list}
  return render(request, 'polls/index.html', context)                 #- renders the requested template
                                                                      #- with the defined context.

def detail(request, question_id):
  #- This block:
  #-    try:
  #-      question = Question.objects.get(pk=question_id)
  #-    except Question.DoesNotExist:
  #-      raise Http404('Question does not exist.')                   #- Handle the Question.DoesNotExist exception with a code 404.
  #- can just be rewritten as:
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
  return HttpResponse("You're looking at the results of question %s."%question_id)

def vote(request, question_id):
  return HttpResponse("You're voting on question %s."%question_id)
