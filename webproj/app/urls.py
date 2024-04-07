from django.urls import path, include
from . import views

urlpatterns = [
    # Testing index
    path('', views.index, name='index'),
    
    # Authentication
    path('accounts/', include('django.contrib.auth.urls')),
    
    #test
    path('wizard/<str:wizard_id>/', views.wizard_detail, name='wizard_detail'),
    path('test', views.test, name="test")
]
