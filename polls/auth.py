from django.shortcuts import redirect
from django.contrib import messages

from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from django.utils.decorators import available_attrs
from django.utils.six.moves.urllib.parse import urlparse
from django.contrib.auth.views import redirect_to_login

from .models import Poll

def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME, message=None):
	def decorator(view_func):
		@wraps(view_func, assigned=available_attrs(view_func))
		def _wrapped_view(request, *args, **kwargs):
			if test_func(request.user):
				return view_func(request, *args, **kwargs)

			if message:
				messages.add_message(request, messages.ERROR, message)

			path = request.build_absolute_uri()
			resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
			login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
			current_scheme, current_netloc = urlparse(path)[:2]

			if ((not login_scheme or login_scheme == current_scheme) and (not login_netloc or login_netloc == current_netloc)):
				path = request.get_full_path()
			return redirect_to_login(path, resolved_login_url, redirect_field_name)
		return _wrapped_view
	return decorator
    
def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None, message=None):
	actual_decorator = user_passes_test(lambda u: u.is_authenticated(), login_url=login_url, redirect_field_name=redirect_field_name, message=message)
	if function:
		return actual_decorator(function)
	return actual_decorator
    
def permission_required(perm, login_url=None, raise_exception=False, message=None):
	def check_perms(user):
		if not isinstance(perm, (list, tuple)):
			perms = (perm, )
		else:
			perms = perm
		if user.has_perms(perms):
			return True
		if message:
			messages.add_message(request, messages.ERROR, message)
		if raise_exception:
			raise PermissionDenied
		return False
	return user_passes_test(check_perms, login_url=login_url)

def user_account_ownership_required(func):
	def check_ownership(request, *args, **kwargs):
		if request.user.is_superuser or request.user.pk == int(kwargs.get("pk")):
			return func(request, *args, **kwargs)
		else:
			messages.add_message(request, messages.ERROR, "You cannot change others' account.")
			return redirect("polls:index", permanent=False)
	return check_ownership

def user_poll_ownership_required(func):
	def check_ownership(request, *args, **kwargs):
		if request.user.is_superuser or request.user.poll_set.filter(pk=kwargs.get("pk")).count() == 1:
			return func(request, *args, **kwargs)
		else:
			messages.add_message(request, messages.ERROR, "You cannot change/delete others' polls.")
			return redirect("polls:index", permanent=False)
	return check_ownership

def user_vote_required(func):
	def check_user_voted(request, *args, **kwargs):
		if request.user.is_superuser or request.user.choice_set.all().filter(for_poll_id=kwargs.get("pk")).count() == 1:
			return func(request, *args, **kwargs)
		else:
			messages.add_message(request, messages.ERROR, "Make your vote first.")
			return redirect("polls:vote", permanent=False, *args, **kwargs)
	return check_user_voted

def poll_no_votes_required(func):
	def check_no_votes(request, *args, **kwargs):
		if request.user.is_superuser or request.user.poll_set.get(pk=kwargs.get("pk")).choice_set.filter(votes__gt=0).count() == 0:
			return func(request, *args, **kwargs)
		else:
			messages.add_message(request, messages.ERROR, "The poll has already started.")
			return redirect("polls:index", permanent=False)
	return check_no_votes

def user_no_vote_required(func):
	def check_user_no_voted(request, *args, **kwargs):
		if request.user.is_superuser or Poll.objects.get(pk=kwargs.get("pk")).choice_set.filter(voted_by__id=request.user.pk).count() == 0:
			return func(request, *args, **kwargs)
		else:
			messages.add_message(request, messages.WARNING, "You already voted here.")
			return redirect("polls:results", permanent=False, *args, **kwargs)
	return check_user_no_voted
