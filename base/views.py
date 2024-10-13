"""
Author: Joshua Delos Santos
Date: 02/09/2024
"""

from django.shortcuts import render
from django.http import HttpResponse

# Sample exercises in a user session.
session = [
    {'name': 'Barbel squats', 'reps': 5, 'weight': 45},
    {'name': 'Barbel press', 'reps': 5, 'weight': 45},
    {'name': 'Barbel curls', 'reps': 5, 'weight': 45}
]

def home(request):
    """Return the homepage."""
    return  render(request, 'base/home.html')

def sessions(request):
    """Return user session page."""
    context = {'session': session}  # Sample context
    return render(request, 'session.html', context)

def statistics(request):
    """Return user satatistics page."""
    return render(request, 'statistics.html')

def profile(request):
    """Return user profile page."""
    return render(request, 'profile.html')

def exercise(request):
    """Return user exercise page."""
    return render(request, 'exercise.html')

def contact(request):
    """Return contact page."""
    return render(request, 'contact.html')