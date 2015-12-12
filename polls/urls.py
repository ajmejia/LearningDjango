#---------------------------------------------------------------
#- In this file I will define the url patterns of my polls app.
#---------------------------------------------------------------
from django.conf.urls import url

from . import views

urlpatterns = [
               #url(r"^$", views.index, name="index"),                  #- Setting the index view url.
               #url(r"^(?P<question_id>[0-9]+)/$", views.detail,
               #    name="detail"),                                     #- This is how the view it's gonna
               #                                                        #- the url of a question detail.
               #url(r"^(?P<question_id>[0-9]+)/results$", views.results,
               #    name="results"),
               url(r"^$", views.IndexView.as_view(), name='index'),
               url(r"^signup$", views.signup, name='signup'),
               url(r"^signin$", views.signin, name='signin'),
               url(r"^(?P<pk>[0-9]+)/$", views.DetailView.as_view(), name='detail'),
               url(r"^(?P<pk>[0-9]+)/results/$", views.ResultsView.as_view(), name='results'),
               url(r"^(?P<question_id>[0-9]+)/vote$", views.vote, name='vote'),
              ]
