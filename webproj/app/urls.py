from django.urls import path, include
from . import views

urlpatterns = [
    # Testing index
    path('', views.index, name='index'),

    # path('dashboard/', views.dashboard, name='dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('professor/', views.professor_dashboard, name='professor_dashboard'),
    path('pass_student/', views.pass_student, name='pass_student'),

    path('headmaster/', views.headmaster_dashboard, name='headmaster_dashboard'),
    
    # COURSE PAGE
    path('course', views.course_view , name='course'),
    path('remove_student', views.remove_student, name='remove_student'),
    path('add_student', views.add_student, name='add_student'),
    path('remove_spell', views.remove_spell, name='remove_spell'),
    path('add_spell', views.add_spell, name='add_spell'),
    path('change_professor', views.change_professor, name='change_professor'),

    path('professor/', views.professor_dashboard, name='professor_dashboard'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('back_to_dashboard', views.back_to_dashboard, name='back_to_dashboard'),
    
    path('update_wizard', views.update_wizard, name="update_wizard"),

    # Register
    path('register/', views.register_view, name='register'),

    # Login
    path('login/', views.login_view, name='login'),

    # Logout
    path('logout/', views.logout_view, name='logout'),

]