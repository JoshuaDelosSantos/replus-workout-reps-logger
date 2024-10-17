"""
URL configuration for the users app

Author: Joshua Delos Santos
Date: 17/10/2024
"""

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register')
]