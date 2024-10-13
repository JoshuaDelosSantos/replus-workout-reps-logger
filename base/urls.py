"""
URL configuration for the base app

Author: Joshua Delos Santos
Date: 02/09/2024
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('session/', views.sessions, name="session"),
    path('statistics/', views.statistics, name="statistics"),
    path('profile/', views.profile, name="profile"),
    path('exercise/', views.exercise, name="exercise"),
    path('contact/', views.contact, name="contact")
]
