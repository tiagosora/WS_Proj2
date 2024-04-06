from django.urls import path
from . import views

urlpatterns = [
    # Testing index
    path('', views.index, name='index'),
    
    # Authentication
    path('authentication/', views.authentication, name='authentication'),
]