from django.urls import path, include
from . import views

urlpatterns = [
    # Testing index
    path('', views.index, name='index'),

    # Authentication
    path('accounts/', include('django.contrib.auth.urls')),

    # Register
    path('register/', views.register_view, name='register'),

    # Login
    path('login/', views.login_view, name='login'),

    # Logout
    path('logout/', views.logout_view, name='logout'),

]
