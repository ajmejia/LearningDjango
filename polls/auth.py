from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def user_account_ownership_required(func):
	def check_ownership(request, *args, **kwargs):
		if request.user.pk == int(kwargs.get("pk")) or request.user.is_superuser:
			return func(request, *args, **kwargs)
		else:
			messages.add_message(request, messages.ERROR, "You cannot change others' account.")
			return redirect("polls:index", permanent=False)
	return check_ownership

def user_poll_ownership_required(func):
	def check_ownership(request, *args, **kwargs):
		if request.user.poll_set.filter(pk=kwargs.get("pk")).count() == 1 or request.user.is_superuser:
			return func(request, *args, **kwargs)
		else:
			messages.add_message(request, messages.ERROR, "You cannot change/delete others' polls.")
			return redirect("polls:index", permanent=False)
	return check_ownership

def user_vote_required(func):
	def check_user_voted(request, *args, **kwargs):
		if request.user.choice_set.all().filter(for_poll_id=kwargs.get("pk")).count() == 1 or request.user.is_superuser:
			return func(request, *args, **kwargs)
		else:
			messages.add_message(request, messages.ERROR, "Make your vote first.")
			return redirect("polls:vote", permanent=False, *args, **kwargs)
	return check_user_voted

def poll_no_votes_required(func):
	def check_no_votes(request, *args, **kwargs):
		if request.user.poll_set.get(pk=kwargs.get("pk")).choice_set.filter(votes__gt=0).count() == 0 or request.user.is_superuser:
			return func(request, *args, **kwargs)
		else:
			messages.add_message(request, messages.ERROR, "The poll has already started.")
			return redirect("polls:index", permanent=False)
	return check_no_votes
