from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def student_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        # Check if the 'role' is in session and if it is 'student'
        if request.session.get('role') != 'student':
            return HttpResponseForbidden("You do not have permission to view this page.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def professor_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('role') != 'professor':
            return HttpResponseForbidden("You do not have permission to view this page.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def headmaster_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('role') != 'headmaster':
            return HttpResponseForbidden("You do not have permission to view this page.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def logout_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # If user is logged in (authenticated session), redirect to the index page
        if request.session.get('authenticated'):
            return redirect('index')
        # Otherwise, proceed with the view
        return view_func(request, *args, **kwargs)

    return _wrapped_view
