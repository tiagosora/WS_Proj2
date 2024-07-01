from app.decorators import (headmaster_required, logout_required,
                            professor_required, student_required)
from app.views_functions import (authentication_views, course_views, dashboard_views,
                       points_views, utility_views)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Authentication views

@logout_required
def authentication(request):
    return authentication_views.authentication(request)

@logout_required
def login_view(request):
    return authentication_views.login_view(request)

@logout_required
def register_view(request):
    return authentication_views.register_view(request)

@login_required(redirect_field_name="")
def logout_view(request):
    return authentication_views.logout_view(request)

# Utility views

@login_required
def index(request):
    return utility_views.back_to_dashboard(request)

@login_required
def back_to_dashboard(request):
    return utility_views.back_to_dashboard(request)

# Dashboard views

@student_required
def student_dashboard(request):
    return dashboard_views.student_dashboard(request)

@professor_required
def professor_dashboard(request):
    return dashboard_views.professor_dashboard(request)

@headmaster_required
def headmaster_dashboard(request):
    return dashboard_views.headmaster_dashboard(request)

def update_wizard(request):
    dashboard_views.update_wizard(request)
    return back_to_dashboard(request)

# Course views

@headmaster_required
def course_view(request):
    return course_views.course_view(request)

@require_http_methods(["POST"])
@headmaster_required
def remove_student(request):
    return course_views.remove_student(request)

@require_http_methods(["POST"])
@headmaster_required
def add_student(request):
    return course_views.add_student(request)

@require_http_methods(["POST"])
@headmaster_required
def remove_spell(request):
    return course_views.remove_spell(request)

@require_http_methods(["POST"])
@headmaster_required
def add_spell(request):
    return course_views.add_spell(request)

@require_http_methods(["POST"])
@headmaster_required
def change_professor(request):
    return course_views.change_professor(request)

@require_http_methods(["POST"])
@professor_required
def pass_student(request):
    return course_views.pass_student(request)

def points_banners(request):
    return points_views.points_banners(request)

def give_points(request):
    return points_views.give_points(request)

@csrf_exempt
@require_POST
def toggle_infering(request):
    return utility_views.toggle_infering(request)

def initialize_infering(request):
    return utility_views.initialize_infering(request)