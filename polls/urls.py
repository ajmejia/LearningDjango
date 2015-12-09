#---------------------------------------------------------------
#- In this file I will define the url patterns of my polls app.
#---------------------------------------------------------------
from django.conf.urls import url
from . import views

urlpatterns = [
               url(r"^$", views.index, name="index"),        #- setting the index view url
              ]
