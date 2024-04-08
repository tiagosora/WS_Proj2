from django.urls import path, include
from . import views

urlpatterns = [
    # Testing index
    path('', views.index, name='index'),

    # path('dashboard/', views.dashboard, name='dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),

    path('accounts/', include('django.contrib.auth.urls')),

    # test
    # path('wizard/<str:wizard_id>/', views.wizard_detail, name='wizard_detail'),
    # path('test/', views.test, name="test"),

    # path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]