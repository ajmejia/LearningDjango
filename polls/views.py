from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Choice, Question

# Create your views here.
#---------------------------------------------------------------
#- This is the view file, where the contents of a web page is
#- defined. This site, for instance, will have the following
#- views:
#-    * index
#-    * detail
#-    * results
#-    * vote
#-
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
  latest_question_list = Question.objects.order_by('-pub_date')[:5]      #- select latest 5 questions.
  context = {'latest_question_list': latest_question_list}
  return render(request, 'polls/index.html', context)                    #- renders the requested template
                                                                         #- with the defined context.

def detail(request, question_id):
  #- This block:
  #-    try:
  #-      question = Question.objects.get(pk=question_id)
  #-    except Question.DoesNotExist:
  #-      raise Http404('Question does not exist.')                      #- Handle the Question.DoesNotExist exception with a code 404.
  #- can just be rewritten as:
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
  p = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = p.choice_set.get(pk=request.POST['choice'])        #- The request.POST is a dictionary-like object that maps the submitted
                                                                         #- data through the post method.
  except KeyError, Choice.DoesNotExist:
    return render(request, 'polls/detail.html', {
                  'question': p,
                  'error_message': "You didn't setect a choice.",        #- This there is no option selected upon submitting, a KeyError will be raised
                                                                         #- and the detail template will be rendered with a error message.
                  })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))  #- Since the page we want to redirect to has a variable url, I used the
                                                                         #- reverse method to give the view (instead of the url) and the variable
                                                                         #- part (p.id).


