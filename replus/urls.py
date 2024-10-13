"""
URL configuration for replus project.

Author: Joshua Delos Santos
Date: 02/09/2024
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))  # Include urls from the base app
]
