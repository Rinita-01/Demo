from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps

def unauthenticated_user(view_funv):
    def wapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('myAccount')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


""" A custom decorator that redirects users to the login page. """
def custom_login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            print('User is not authenticated')
            return redirect('customer_login')
        return view_func(request, *args, **kwargs)
    return wrapped_view