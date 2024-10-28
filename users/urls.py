"""
URL configuration for the users app

Author: Joshua Delos Santos
Date: 17/10/2024
"""

from django.urls import path
from .views.register_view import RegisterView 
from .views.login_view import LoginView 
from .views.logout_view import LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]