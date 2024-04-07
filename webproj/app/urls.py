from django.urls import path, include
from . import views

urlpatterns = [
    # Testing index
    path('', views.index, name='index'),

    # Authentication
    path('accounts/', include('django.contrib.auth.urls')),

    # test
    path('wizard/<str:wizard_id>/', views.wizard_detail, name='wizard_detail'),

    # path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

]
