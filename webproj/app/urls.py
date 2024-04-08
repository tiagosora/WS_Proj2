from django.urls import path, include
from . import views

urlpatterns = [
    # Testing index
    path('', views.index, name='index'),

    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    
    path('student/', views.student_dashboard, name='student_dashboard'),
    
    # test
    path('wizard/<str:wizard_id>/', views.wizard_detail, name='wizard_detail'),
    #path('test/', views.test, name="test"),

    path('accounts/', include('django.contrib.auth.urls')),
]