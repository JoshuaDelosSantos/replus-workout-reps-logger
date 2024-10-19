"""
Author: Joshua Delos Santos
Date: 17/10/2024
"""

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def register(request):
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
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
        
    return render(request, 'users/register.html', {"form":form})


def login(request):
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
            return redirect('home')    
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {"form":form})