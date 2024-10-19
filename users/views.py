"""
Author: Joshua Delos Santos
Date: 17/10/2024
"""

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def register_view(request):
    """
    Handle user registration.
    Args:
        request (HttpRequest): The incoming request.
    Returns:
        HttpResponse: Renders the form or redirects after a successful registration.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('home')
    else:
        form = UserCreationForm()
        
    return render(request, 'users/register.html', {"form":form})


def login_view(request):
    """
    Handle user login.
    Args:
        request (HttpRequest): The incoming request.
    Returns:
        _type_: _description_
    """
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')    
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {"form":form})


def logout_view(request):
    """
    Handle user logout.

    Args:
        request (HttpRequest): The incoming request.
    """
    if request.method == "POST":
        logout(request)
        return redirect('home')