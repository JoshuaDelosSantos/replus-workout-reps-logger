"""
URL configuration for the base app

Author: Joshua Delos Santos
Date: 02/09/2024
"""

from django.urls import path
from . import views
from .views.home_view import HomeView
from .views.sessions_view import SessionsView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('sessions/', SessionsView.as_view(), name="sessions_view"),
]
