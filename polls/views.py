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

def index(request):
  return HttpResponse("Hello, world. You're at the polls index.")
