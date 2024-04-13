from django.urls import path, include
from . import views

urlpatterns = [
    # Testing index
    path('', views.index, name='index'),

    # path('dashboard/', views.dashboard, name='dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),

    path('headmaster/', views.headmaster_dashboard, name='headmaster_dashboard'),

    path('professor/', views.professor_dashboard, name='professor_dashboard'),

    path('accounts/', include('django.contrib.auth.urls')),

    # Register
    path('register/', views.register_view, name='register'),

    # Login
    path('login/', views.login_view, name='login'),

    # Logout
    path('logout/', views.logout_view, name='logout'),

]