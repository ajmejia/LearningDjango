#---------------------------------------------------------------
#- In this file I will define the url patterns of my polls app.
#---------------------------------------------------------------
from django.conf.urls import url

from . import views

urlpatterns = [
               url(r"^$", views.IndexView.as_view(), name='index'),
               url(r"^signup$", views.SignupView.as_view(), name='signup'),
               url(r"^login$", views.LoginView.as_view(), name='login'),
               url(r"^logout$", views.LogoutView.as_view(), name='logout'),
               url(r"^(?P<pk>[0-9]+)/$", views.VoteView.as_view(), name='vote'),
               url(r"^(?P<pk>[0-9]+)/results/$", views.ResultsView.as_view(), name='results'),
              ]
