"""
URL configuration for the users app

Author: Joshua Delos Santos
Date: 17/10/2024
"""

from django.urls import path
from .view.register_view import RegisterView 
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Map the URL to RegisterView
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]