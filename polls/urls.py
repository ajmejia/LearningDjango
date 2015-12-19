#---------------------------------------------------------------
#- In this file I will define the url patterns of my polls app.
#---------------------------------------------------------------
from django.conf.urls import url

from . import views

urlpatterns = [
               url(r"^$", views.IndexView.as_view(), name="index"),
               url(r"^signup$", views.SignupView.as_view(), name="signup"),
               url(r"^login$", views.LoginView.as_view(), name="login"),
               url(r"^accounts/(?P<pk>[0-9]+)$", views.UserAccountView.as_view(), name="accounts"),
               url(r"^create-poll$", views.CreatePollView.as_view(), name="create-poll"),
               url(r"^logout$", views.LogoutView.as_view(), name="logout"),
               url(r"^(?P<pk>[0-9]+)/$", views.VotePollView.as_view(), name="vote"),
               url(r"^(?P<pk>[0-9]+)/results/$", views.ResultsPollView.as_view(), name="results"),
              ]
