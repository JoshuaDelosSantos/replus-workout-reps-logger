"""
URL configuration for the base app

Author: Joshua Delos Santos
Date: 02/09/2024
"""

from django.urls import path
from . import views
from .views.home_view import HomeView
from .views.sessions_view import SessionsView
from .views.exercise_view import ExerciseView
from .views.lines_view import LinesView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('sessions/', SessionsView.as_view(), name="sessions"),
    path('sessions/<slug:session_slug>/', ExerciseView.as_view(), name='exercise'),
    path('sessions/<slug:session_slug>/<slug:exercise_slug>/', LinesView.as_view(), name='lines'),
]
