from django.http import HttpResponse
from django.shortcuts import redirect
# this goes on to a  view function which allows only 
def admin_only(view_func):# users in the admin group to access
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group != 'admin':
			return redirect('home')

		if group == 'admin':
			return view_func(request, *args, **kwargs)

	return wrapper_function