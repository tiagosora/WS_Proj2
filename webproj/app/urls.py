from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('student/', views.student_dashboard, name='student_dashboard'),
    path('professor/', views.professor_dashboard, name='professor_dashboard'),
    path('headmaster/', views.headmaster_dashboard, name='headmaster_dashboard'),
    path('course', views.course_view, name='course'),

    path('back_to_dashboard', views.back_to_dashboard, name='back_to_dashboard'),
    path('toggle_infering', views.toggle_infering, name='toggle_infering'),
    path('initialize_infering', views.initialize_infering, name='initialize_infering'),

    path('pass_student/', views.pass_student, name='pass_student'),
    path('remove_student', views.remove_student, name='remove_student'),
    path('add_student', views.add_student, name='add_student'),
    path('remove_spell', views.remove_spell, name='remove_spell'),
    path('add_spell', views.add_spell, name='add_spell'),
    path('change_professor', views.change_professor, name='change_professor'),
    path('update_wizard', views.update_wizard, name="update_wizard"),
    path('give_points', views.give_points, name='give_points'),
    path('points_banners', views.points_banners, name='points_banners'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
