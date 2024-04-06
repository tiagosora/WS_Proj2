from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    # Testing index
    path('', views.index, name='index'),
    
    # Login
    path('login/', LoginView.as_view(template_name='app/login.html'),name='login'),
]