"""
Author: Joshua Delos Santos
Date: 28/10/2024
"""

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.views import View

class LoginView(View):
    """
    Handle user login.
    """
    def get(self, request):
        """
        Handle GET requests: instantiate a blank version of the form.
        """
        form = AuthenticationForm()
        return render(request, 'users/login.html', {"form": form})

    def post(self, request):
        """
        Handle POST requests: instantiate a form instance with the passed POST variables and then check if it's valid.
        """
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('sessions')
        return render(request, 'users/login.html', {"form": form})