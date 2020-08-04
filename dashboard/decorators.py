from django.shortcuts import redirect
from django.http import HttpResponse

def userNotAuthenticated(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('index')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def userAuthenticated(allowed_roles = []):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('Whoa there! You are not authorized to view this page ' + request.user.username + ' (' + str(request.user.groups.all()[0]) + ')')
		return wrapper_func
	return decorator