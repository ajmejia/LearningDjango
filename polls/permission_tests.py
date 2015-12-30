from django.contrib import messages
from django.core.exceptions import PermissionDenied

def user_account_ownership_required(func):
	def check_ownership(request, *args, **kwargs):
		if request.user.pk == int(kwargs.get("pk")):
			return func(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return check_ownership

def user_poll_ownership_required(func):
	def check_ownership(request, *args, **kwargs):
		if request.user.poll_set.filter(pk=kwargs.get("pk")).count() == 1:
			return func(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return check_ownership

def user_vote_required(func):
	def check_user_voted(request, *args, **kwargs):
		if request.user.choice_set.all().filter(for_poll_id=kwargs.get("pk")).count() == 1:
			return func(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return check_user_voted
