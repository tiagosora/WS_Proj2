from django.urls import path
from . import views

urlpatterns = [
    # Testing index
    path('', views.index, name='index'),
    
    # Authentication
    path('authentication/', views.authentication, name='authentication'),
    
    # Dashboards
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('professor/', views.professor_dashboard, name='professor_dashboard'),
    path('headmaster/', views.headmaster_dashboard, name='headmaster_dashboard'),
]