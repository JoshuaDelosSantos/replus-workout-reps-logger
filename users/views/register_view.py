"""
Author: Joshua Delos Santos
Date: 28/10/2024
"""

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View

class RegisterView(View):
    """
    Handle user registration.
    """
    def get(self, request):
        """
        Handle GET requests: instantiate a blank version of the form.
        """
        form = UserCreationForm()
        return render(request, 'users/register.html', {"form": form})

    def post(self, request):
        """
        Handle POST requests: instantiate a form instance with the passed POST variables and then check if it's valid.
        """
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'users/register.html', {"form": form})