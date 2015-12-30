from django.core.exceptions import PermissionDenied

def user_account_ownership_required(func):
	def check_ownership(request, *args, **kwargs):
		print request, args, kwargs
		if request.user.pk == int(kwargs.get("pk")):
			return func(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return check_ownership
