from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def student_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        # Check if the 'role' is in session and if it is 'student'
        if request.session.get('role') != 'http://hogwarts.edu/ontology.owl#Student':
            return HttpResponseForbidden("You do not have permission to view this page.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def professor_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('role') != 'http://hogwarts.edu/ontology.owl#Professor':
            return HttpResponseForbidden("You do not have permission to view this page.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def headmaster_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('role') != 'http://hogwarts.edu/ontology.owl#Headmaster':
            return HttpResponseForbidden("You do not have permission to view this page.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def logout_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('authenticated'):
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return _wrapped_view
