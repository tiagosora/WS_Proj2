
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name=''),
    path('wizard/<str:wizard_id>/', views.wizard_detail, name='wizard_detail'),
]
